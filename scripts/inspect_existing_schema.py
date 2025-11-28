"""
Inspect existing Supabase schema to understand current structure
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print(" Missing Supabase credentials!")
    exit(1)

print("🔌 Connecting to Supabase...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
print(" Connected!\n")

# Try to get schema information using direct SQL queries
# These tables were hinted at by error messages
suggested_tables = [
    'resumes',
    'resume_versions',
    'automation_logs',
    'job_search_results',
    'candidates',
    'job_postings',
    'applications',
    'user_preferences'
]

print("=" * 80)
print(" CHECKING SUGGESTED TABLES FROM SUPABASE")
print("=" * 80)
print()

found_tables = []

for table in suggested_tables:
    try:
        # Use the PostgREST API to check if table exists
        response = supabase.table(table).select("*").limit(1).execute()
        
        # If we get here without error, table exists and is accessible
        record_count = len(response.data)
        print(f" {table}")
        print(f"   Status: ACCESSIBLE")
        print(f"   Sample records: {record_count}")
        
        if record_count > 0:
            # Show first record structure
            first_record = response.data[0]
            print(f"   Columns: {', '.join(first_record.keys())}")
            
        found_tables.append(table)
        print()
        
    except Exception as e:
        error_msg = str(e)
        if 'permission denied' in error_msg.lower():
            print(f"  {table}")
            print(f"   Status: EXISTS but RLS blocking access")
            print(f"   Error: {error_msg}")
            found_tables.append(table)
        elif 'not found' in error_msg.lower() or 'pgrst205' in error_msg.lower():
            print(f" {table}")
            print(f"   Status: DOES NOT EXIST")
        else:
            print(f"❓ {table}")
            print(f"   Status: UNKNOWN ERROR")
            print(f"   Error: {error_msg}")
        print()

print("=" * 80)
print(" SUMMARY")
print("=" * 80)
print(f"Found {len(found_tables)} tables")
print()

if found_tables:
    print("Tables that exist (some may need RLS policy updates):")
    for table in found_tables:
        print(f"   • {table}")
    print()
    print("=" * 80)
    print(" NEXT STEP")
    print("=" * 80)
    print()
    print("Run this SQL to fix RLS policies:")
    print("1. Open: https://supabase.com/dashboard/project/ktitfajlacjysacdsfxf/sql")
    print("2. Copy/paste contents of: fix_rls_policies.sql")
    print("3. Click 'RUN'")
    print()
    print("This will allow your service_role key to access all tables.")
