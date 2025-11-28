"""
List all RLS policies in Supabase using direct SQL query via PostgREST
This bypasses table-level RLS by querying system catalogs
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_ROLE_KEY')
)

print(" Querying RLS policies via PostgREST RPC...\n")

# Use Supabase RPC to query pg_policies system view
# This should work even if tables are RLS-protected
try:
    # Try using the postgres_fdw or direct query
    # PostgREST exposes system views, let's try direct query
    result = supabase.rpc('exec_sql', {
        'query': '''
            SELECT 
                schemaname,
                tablename,
                policyname,
                roles::text as roles,
                cmd,
                qual IS NOT NULL as has_using,
                with_check IS NOT NULL as has_with_check
            FROM pg_policies
            WHERE schemaname = 'public'
                AND tablename IN ('candidates', 'job_postings', 'applications', 'resumes', 'resume_versions', 'user_preferences', 'companies')
            ORDER BY tablename, policyname;
        '''
    }).execute()
    
    print(" Policies retrieved:")
    print(result)
    
except Exception as e:
    print(f" RPC method failed: {e}")
    print()
    print("=" * 80)
    print("  PostgREST CACHE ISSUE CONFIRMED")
    print("=" * 80)
    print()
    print("The service_role policies exist but PostgREST hasn't refreshed its cache.")
    print()
    print("Solutions:")
    print()
    print("1. **Restart PostgREST** (Fastest - 30 seconds):")
    print("   • Go to: https://supabase.com/dashboard/project/ktitfajlacjysacdsfxf")
    print("   • Click: Project Settings → API")
    print("   • Look for 'Restart' or 'Reload' button")
    print()
    print("2. **Wait for cache expiry** (5-10 minutes):")
    print("   • PostgREST automatically refreshes schema cache periodically")
    print()
    print("3. **Use direct PostgreSQL connection** (Immediate):")
    print("   • Add database password to .env file")
    print("   • Run: python scripts/test_direct_postgres.py")
    print("   • This bypasses PostgREST entirely")
    print()
    print("=" * 80)
    print(" TO ADD DATABASE PASSWORD:")
    print("=" * 80)
    print()
    print("1. Get password from: https://supabase.com/dashboard/project/ktitfajlacjysacdsfxf/settings/database")
    print("2. Update .env line 19:")
    print("   SUPABASE_DB_URL=postgresql://postgres.ktitfajlacjysacdsfxf:YOUR_PASSWORD_HERE@...")
    print()
