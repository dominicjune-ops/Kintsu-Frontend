"""
Comprehensive verification after PostgREST restart
Shows: table access, record counts, sample data structure
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

print("🔌 Connecting to Supabase with service_role key...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
print(" Connected!\n")

# Core tables for CareerCoach.ai
tables_to_check = {
    'candidates': 'User profiles and candidate information',
    'job_postings': 'Job listings from various sources',
    'applications': 'User job applications tracking',
    'resumes': 'Resume storage and management',
    'resume_versions': 'Resume version history',
    'cover_letters': 'Cover letter templates and versions',
    'companies': 'Company information',
    'user_preferences': 'User settings and preferences',
    'strategies': 'Job search strategies',
    'automation_logs': 'System automation tracking'
}

print("=" * 80)
print(" TESTING SERVICE_ROLE ACCESS (After PostgREST Restart)")
print("=" * 80)
print()

results = {
    'accessible': [],
    'blocked': [],
    'empty': [],
    'with_data': []
}

for table, description in tables_to_check.items():
    try:
        # Test access and get count
        response = supabase.table(table).select("*", count="exact").limit(3).execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        
        print(f" {table}")
        print(f"   {description}")
        print(f"   Records: {count}")
        
        if response.data and len(response.data) > 0:
            # Show column structure from first record
            first_record = response.data[0]
            cols = list(first_record.keys())
            print(f"   Columns ({len(cols)}): {', '.join(cols[:10])}")
            if len(cols) > 10:
                print(f"                {' ' * 12}...and {len(cols) - 10} more")
            
            results['with_data'].append({
                'table': table,
                'count': count,
                'columns': cols
            })
        else:
            print(f"   (empty table - no records yet)")
            results['empty'].append(table)
        
        results['accessible'].append(table)
        print()
        
    except Exception as e:
        error_msg = str(e)
        print(f" {table}")
        print(f"   {description}")
        print(f"   Error: {error_msg[:150]}")
        results['blocked'].append(table)
        print()

print("=" * 80)
print(" SUMMARY")
print("=" * 80)
print()

if results['accessible']:
    print(f" Accessible: {len(results['accessible'])}/{len(tables_to_check)}")
    for t in results['accessible']:
        print(f"   • {t}")
    print()

if results['with_data']:
    print(f"📦 Tables with data: {len(results['with_data'])}")
    for item in results['with_data']:
        print(f"   • {item['table']}: {item['count']} records, {len(item['columns'])} columns")
    print()

if results['empty']:
    print(f"📭 Empty tables: {len(results['empty'])}")
    for t in results['empty']:
        print(f"   • {t}")
    print()

if results['blocked']:
    print(f" Still blocked: {len(results['blocked'])}")
    for t in results['blocked']:
        print(f"   • {t}")
    print()
    print("  If tables are still blocked:")
    print("   1. Wait another minute for PostgREST cache")
    print("   2. Check Supabase logs for errors")
    print("   3. Use Option B (direct PostgreSQL connection)")
else:
    print(" SUCCESS! All tables are accessible!")
    print()
    print("=" * 80)
    print(" NEXT STEPS")
    print("=" * 80)
    print()
    print("1. Update database/config.py to use Supabase PostgreSQL")
    print("2. Update SQLAlchemy models to match Supabase schema")
    print("3. Create migration mapping between SQLite models and Supabase tables")
    print("4. Test API endpoints with real Supabase data")
    print()
    
    # Save schema information for model mapping
    if results['with_data']:
        schema_map = {
            item['table']: item['columns'] 
            for item in results['with_data']
        }
        
        with open('supabase_schema_mapping.json', 'w') as f:
            json.dump(schema_map, f, indent=2)
        
        print(" Saved schema mapping to: supabase_schema_mapping.json")
        print("   Use this to update your SQLAlchemy models!")
