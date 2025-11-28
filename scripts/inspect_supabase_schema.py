"""
Quick Supabase Schema Inspector
Connect to Supabase and list all tables with their columns
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print(" Error: Missing Supabase credentials in .env")
    print(f"SUPABASE_URL: {'' if SUPABASE_URL else ''}")
    print(f"SUPABASE_SERVICE_ROLE_KEY: {'' if SUPABASE_SERVICE_ROLE_KEY else ''}")
    exit(1)

# Connect to Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

print(" Inspecting Supabase Schema...\n")
print(f"Connected to: {SUPABASE_URL}\n")

# Query to get all tables in public schema
query = """
SELECT 
    table_name,
    (
        SELECT json_agg(
            json_build_object(
                'column_name', column_name,
                'data_type', data_type,
                'is_nullable', is_nullable,
                'column_default', column_default
            )
        )
        FROM information_schema.columns c
        WHERE c.table_schema = t.table_schema
        AND c.table_name = t.table_name
        ORDER BY ordinal_position
    ) as columns
FROM information_schema.tables t
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
ORDER BY table_name;
"""

try:
    # Execute raw SQL query
    result = supabase.rpc('exec_sql', {'query': query}).execute()
    
    if result.data:
        tables = result.data
        print(f" Found {len(tables)} tables:\n")
        
        for table in tables:
            table_name = table['table_name']
            columns = table.get('columns', [])
            
            print(f"╔═══ {table_name.upper()} {'═' * (50 - len(table_name))}")
            print(f"║ Columns: {len(columns) if columns else 0}")
            
            if columns:
                for col in columns:
                    nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                    default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
                    print(f"║   - {col['column_name']}: {col['data_type']} {nullable}{default}")
            print()
    else:
        print("  No tables found or unable to query schema")
        print("Let's try a simpler approach - listing table names:\n")
        
        # Fallback: Try to query each known table
        known_tables = [
            'profiles', 'candidates', 'job_postings', 'applications',
            'subscription_plans', 'user_subscriptions', 'saved_searches',
            'user_preferences', 'resumes', 'cover_letters'
        ]
        
        existing_tables = []
        for table in known_tables:
            try:
                result = supabase.table(table).select('*').limit(0).execute()
                existing_tables.append(table)
                print(f" {table}")
            except Exception as e:
                print(f" {table} - {str(e)[:50]}")
        
        print(f"\n Found {len(existing_tables)} existing tables")

except Exception as e:
    print(f" Error querying schema: {e}")
    print("\nAttempting fallback approach...\n")
    
    # Fallback: Try to query specific tables from Airtable POC
    tables_to_check = [
        'profiles',
        'candidates', 
        'job_postings',
        'applications',
        'resumes',
        'subscription_plans',
        'user_subscriptions'
    ]
    
    for table in tables_to_check:
        try:
            # Try to select from table (limit 1 to check if it exists)
            result = supabase.table(table).select('*').limit(1).execute()
            count = len(result.data) if result.data else 0
            print(f" {table:<25} ({count} sample records)")
        except Exception as e:
            error_msg = str(e)[:80]
            print(f" {table:<25} - {error_msg}")

print("\n Schema inspection complete!")
