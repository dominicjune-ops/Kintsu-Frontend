"""
Quick check for company membership model
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_ROLE_KEY')
)

print(" Checking company membership model...\n")

# Check if company_users table exists
try:
    result = supabase.table('company_users').select("*").limit(1).execute()
    print(" company_users table EXISTS")
    print(f"   Structure: {result.data[0].keys() if result.data else 'empty table'}")
except Exception as e:
    if 'not found' in str(e).lower() or 'pgrst205' in str(e).lower():
        print(" company_users table DOES NOT EXIST")
    else:
        print(f"  company_users: {e}")

print()

# Check companies table structure
try:
    result = supabase.table('companies').select("*").limit(1).execute()
    print(" companies table EXISTS")
    if result.data:
        print(f"   Columns: {', '.join(result.data[0].keys())}")
    else:
        print("   (empty table)")
except Exception as e:
    print(f"  companies: {e}")

print()

# Check job_postings for company relationship
try:
    result = supabase.table('job_postings').select("*").limit(1).execute()
    print(" job_postings table EXISTS")
    if result.data:
        cols = list(result.data[0].keys())
        company_cols = [c for c in cols if 'company' in c.lower()]
        print(f"   Company-related columns: {', '.join(company_cols) if company_cols else 'none found'}")
    else:
        print("   (empty table)")
except Exception as e:
    print(f"  job_postings: {e}")
