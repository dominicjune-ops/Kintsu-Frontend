"""
Verify tables were created in Supabase
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

print("=" * 80)
print("VERIFYING PHASE 1 TABLES")
print("=" * 80)

tables_to_check = [
    'user_preferences',
    'candidates', 
    'job_postings',
    'applications'
]

for table in tables_to_check:
    print(f"\nChecking table: {table}")
    try:
        result = supabase.table(table).select('*').limit(0).execute()
        print(f" {table} exists!")
    except Exception as e:
        print(f" {table} does NOT exist or has error: {str(e)}")

print("\n" + "=" * 80)
print("Note: If tables show as not existing, the Supabase API cache")
print("needs to be refreshed. This can take 1-2 minutes after running SQL.")
print("=" * 80)
