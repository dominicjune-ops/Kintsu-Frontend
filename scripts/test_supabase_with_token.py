"""
Test Supabase connection with API token
This will check what tables exist and test basic operations
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_API_TOKEN = os.getenv('SUPABASE_API_TOKEN')  # Your API token
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# Try with API token first, fallback to service role key
api_key = SUPABASE_API_TOKEN or SUPABASE_SERVICE_ROLE_KEY

if not SUPABASE_URL or not api_key:
    print(" Missing Supabase credentials!")
    print(f"   SUPABASE_URL: {'' if SUPABASE_URL else ''}")
    print(f"   SUPABASE_API_TOKEN: {'' if SUPABASE_API_TOKEN else ''}")
    print(f"   SUPABASE_SERVICE_ROLE_KEY: {'' if SUPABASE_SERVICE_ROLE_KEY else ''}")
    exit(1)

print("🔐 Supabase Connection Info:")
print(f"   URL: {SUPABASE_URL}")
print(f"   Using: {'API Token' if SUPABASE_API_TOKEN else 'Service Role Key'}")
print()

print("🔌 Connecting to Supabase...")
try:
    supabase: Client = create_client(SUPABASE_URL, api_key)
    print(" Connected!\n")
except Exception as e:
    print(f" Connection failed: {e}")
    exit(1)

# Tables to check
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
print(" CHECKING EXISTING TABLES")
print("=" * 80)
print()

found_tables = []
missing_tables = []

for table in tables_to_check:
    print(f"Checking table: {table}...")
    try:
        # Try to query the table (limit 0 to just check if it exists)
        response = supabase.table(table).select("*").limit(0).execute()
        
        # If we get here, table exists
        print(f"    {table}: EXISTS")
        found_tables.append(table)
        
        # Try to count records
        try:
            count_response = supabase.table(table).select("*", count="exact").limit(0).execute()
            count = count_response.count if hasattr(count_response, 'count') else 'unknown'
            print(f"      Records: {count}")
        except:
            print(f"      Records: (count not available)")
            
    except Exception as e:
        error_msg = str(e)
        if 'permission denied' in error_msg.lower():
            print(f"     {table}: EXISTS but permission denied")
            found_tables.append(table)
        elif 'not found' in error_msg.lower() or 'does not exist' in error_msg.lower():
            print(f"    {table}: DOES NOT EXIST")
            missing_tables.append(table)
        else:
            print(f"    {table}: ERROR - {error_msg}")
            missing_tables.append(table)
    print()

print("=" * 80)
print(" SUMMARY")
print("=" * 80)
print(f" Found {len(found_tables)} tables: {', '.join(found_tables) if found_tables else 'None'}")
print(f" Missing {len(missing_tables)} tables: {', '.join(missing_tables) if missing_tables else 'None'}")
print()

if missing_tables:
    print("=" * 80)
    print(" NEXT STEPS")
    print("=" * 80)
    print()
    print("Some tables are missing. You need to create them by:")
    print()
    print("Option 1: Use Supabase SQL Editor")
    print("   1. Go to: https://supabase.com/dashboard/project/ktitfajlacjysacdsfxf/sql")
    print("   2. Run these SQL files in order:")
    for table in missing_tables:
        if table in ['candidates', 'job_postings', 'applications']:
            print(f"      - create_{table}_table.sql")
    print("      - create_triggers.sql")
    print()
    print("Option 2: I can do it programmatically")
    print("   Share your database password and I'll run the migrations")
    print()
else:
    print(" All core tables exist! Ready to use the API.")
    print()
    print("Next: Update database models to use Supabase table names")
