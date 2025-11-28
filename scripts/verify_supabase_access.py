"""
Verify RLS policies and test service_role access after policy updates
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

print("🔌 Connecting to Supabase with service_role key...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
print(" Connected!\n")

# Core tables to test
core_tables = [
    'candidates',
    'job_postings',
    'applications',
    'resumes',
    'resume_versions',
    'companies',
    'user_preferences'
]

print("=" * 80)
print(" TESTING SERVICE_ROLE ACCESS TO CORE TABLES")
print("=" * 80)
print()

accessible_tables = []
blocked_tables = []

for table in core_tables:
    try:
        # Try to query with service_role key
        response = supabase.table(table).select("*").limit(1).execute()
        
        # Try to get count
        count_response = supabase.table(table).select("*", count="exact").limit(0).execute()
        count = count_response.count if hasattr(count_response, 'count') else 'unknown'
        
        print(f" {table}")
        print(f"   Status: ACCESSIBLE")
        print(f"   Records: {count}")
        
        if response.data:
            cols = list(response.data[0].keys())
            print(f"   Columns ({len(cols)}): {', '.join(cols[:8])}")
            if len(cols) > 8:
                print(f"                {'...' + str(len(cols) - 8) + ' more'}")
        else:
            print(f"   (empty table)")
        
        accessible_tables.append(table)
        print()
        
    except Exception as e:
        error_msg = str(e)
        print(f" {table}")
        print(f"   Status: BLOCKED")
        print(f"   Error: {error_msg[:200]}")
        blocked_tables.append(table)
        print()

print("=" * 80)
print(" SUMMARY")
print("=" * 80)
print(f" Accessible: {len(accessible_tables)}/{len(core_tables)}")
if accessible_tables:
    for t in accessible_tables:
        print(f"   • {t}")

if blocked_tables:
    print(f"\n Still blocked: {len(blocked_tables)}")
    for t in blocked_tables:
        print(f"   • {t}")
    print()
    print("  If tables are still blocked, the RLS policies may need PostgREST cache refresh.")
    print("   Try: Restart PostgREST in Supabase dashboard or wait a few minutes.")
else:
    print("\n All core tables are now accessible with service_role!")
    print()
    print(" Next steps:")
    print("   1. Update database/config.py to use Supabase connection")
    print("   2. Update SQLAlchemy models to match Supabase schema")
    print("   3. Test API endpoints with real data")
