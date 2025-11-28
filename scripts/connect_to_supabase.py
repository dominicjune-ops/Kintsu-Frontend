"""
Connect to Supabase and list all tables with actual data
Uses Supabase Python SDK with your credentials
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

print("🔐 Supabase Connection Info:")
print(f"   URL: {SUPABASE_URL}")
print(f"   Service Key: {' Found' if SUPABASE_SERVICE_ROLE_KEY else ' Missing'}")
print()

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print(" Missing Supabase credentials!")
    exit(1)

# Connect to Supabase
print("🔌 Connecting to Supabase...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
print(" Connected!\n")

# Tables to check (from your Airtable POC)
tables_to_check = [
    'candidates',
    'job_postings', 
    'applications',
    'profiles',
    'subscription_plans',
    'user_subscriptions',
    'saved_searches',
    'user_preferences'
]

print("=" * 80)
print(" SUPABASE SCHEMA INSPECTION")
print("=" * 80)
print()

existing_tables = []
table_info = {}

for table_name in tables_to_check:
    try:
        print(f"Checking table: {table_name}...")
        
        # Try to query the table (limit 3 rows to check structure)
        result = supabase.table(table_name).select('*').limit(3).execute()
        
        if result.data is not None:
            row_count = len(result.data)
            existing_tables.append(table_name)
            
            # Get column names from first row
            columns = []
            if row_count > 0:
                columns = list(result.data[0].keys())
            
            table_info[table_name] = {
                'exists': True,
                'sample_count': row_count,
                'columns': columns,
                'sample_data': result.data
            }
            
            print(f"    {table_name}: {row_count} sample rows, {len(columns)} columns")
        else:
            print(f"     {table_name}: Table exists but no data")
            table_info[table_name] = {
                'exists': True,
                'sample_count': 0,
                'columns': [],
                'sample_data': []
            }
            existing_tables.append(table_name)
            
    except Exception as e:
        error_msg = str(e)
        print(f"    {table_name}: {error_msg[:100]}")
        table_info[table_name] = {
            'exists': False,
            'error': error_msg
        }

print()
print("=" * 80)
print(f" SUMMARY: Found {len(existing_tables)} tables")
print("=" * 80)
print()

for table_name in existing_tables:
    info = table_info[table_name]
    print(f"\n╔═══ {table_name.upper()} {'═' * (70 - len(table_name))}")
    print(f"║ Sample rows: {info['sample_count']}")
    print(f"║ Columns ({len(info['columns'])}): {', '.join(info['columns'][:10])}")
    if len(info['columns']) > 10:
        print(f"║           ... and {len(info['columns']) - 10} more")
    
    # Show sample data structure
    if info['sample_data'] and len(info['sample_data']) > 0:
        print(f"║")
        print(f"║ Sample record structure:")
        sample = info['sample_data'][0]
        for key, value in list(sample.items())[:8]:
            value_str = str(value)[:50] if value else 'NULL'
            print(f"║   • {key}: {value_str}")
        if len(sample) > 8:
            print(f"║   ... and {len(sample) - 8} more fields")
    print()

# Missing tables
missing_tables = [t for t in tables_to_check if t not in existing_tables]
if missing_tables:
    print("\n  MISSING TABLES (may need to be created):")
    for table in missing_tables:
        error = table_info[table].get('error', 'Unknown error')
        print(f"   • {table}: {error[:100]}")

print("\n" + "=" * 80)
print(" Inspection complete!")
print("=" * 80)

# Export detailed info to JSON
output_file = "supabase_schema_info.json"
with open(output_file, 'w') as f:
    json.dump(table_info, f, indent=2, default=str)
print(f"\n📄 Detailed schema saved to: {output_file}")
