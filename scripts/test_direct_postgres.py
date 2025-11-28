"""
Connect directly to Supabase PostgreSQL database
This bypasses PostgREST and connects directly to PostgreSQL
"""
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

# Get database URL and replace [YOUR-PASSWORD] with actual password
db_url = os.getenv('SUPABASE_DB_URL', '')

if '[YOUR-PASSWORD]' in db_url:
    print(" Database password not set in .env file!")
    print()
    print("Please update SUPABASE_DB_URL in .env file:")
    print("Replace [YOUR-PASSWORD] with your actual database password")
    print()
    print("Find your password in Supabase dashboard:")
    print("Settings → Database → Connection string")
    print()
    exit(1)

print("🔌 Connecting to PostgreSQL...")
print(f"   Database: {db_url.split('@')[1] if '@' in db_url else 'unknown'}")
print()

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(db_url)
    print(" Connected to PostgreSQL!\n")
    
    # Create cursor
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Get list of tables in public schema
    cur.execute("""
        SELECT 
            tablename,
            schemaname
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename;
    """)
    
    tables = cur.fetchall()
    
    print("=" * 80)
    print(" TABLES IN PUBLIC SCHEMA")
    print("=" * 80)
    print()
    
    for table in tables:
        table_name = table['tablename']
        
        # Get row count
        cur.execute(f"SELECT COUNT(*) as count FROM public.{table_name};")
        count = cur.fetchone()['count']
        
        # Get column info
        cur.execute(f"""
            SELECT 
                column_name,
                data_type,
                is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public' 
                AND table_name = '{table_name}'
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        
        print(f" {table_name}")
        print(f"   Records: {count}")
        print(f"   Columns ({len(columns)}):")
        for col in columns[:5]:  # Show first 5 columns
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            print(f"      • {col['column_name']}: {col['data_type']} ({nullable})")
        if len(columns) > 5:
            print(f"      • ... and {len(columns) - 5} more columns")
        print()
    
    # Check RLS policies
    print("=" * 80)
    print(" RLS POLICIES")
    print("=" * 80)
    print()
    
    cur.execute("""
        SELECT 
            tablename,
            policyname,
            roles,
            cmd,
            CASE 
                WHEN qual IS NOT NULL THEN 'USING clause defined'
                ELSE 'No USING clause'
            END as using_clause,
            CASE 
                WHEN with_check IS NOT NULL THEN 'WITH CHECK clause defined'
                ELSE 'No WITH CHECK clause'
            END as with_check_clause
        FROM pg_policies
        WHERE schemaname = 'public'
            AND policyname LIKE '%service%'
        ORDER BY tablename, policyname;
    """)
    
    policies = cur.fetchall()
    
    if policies:
        for policy in policies:
            print(f" {policy['tablename']}")
            print(f"   Policy: {policy['policyname']}")
            print(f"   Roles: {policy['roles']}")
            print(f"   Command: {policy['cmd']}")
            print(f"   {policy['using_clause']}")
            print(f"   {policy['with_check_clause']}")
            print()
    else:
        print("  No service role policies found!")
        print()
    
    # Close connection
    cur.close()
    conn.close()
    
    print("=" * 80)
    print(" CONNECTION TEST SUCCESSFUL")
    print("=" * 80)
    print()
    print(f"Found {len(tables)} tables in public schema")
    print("Direct PostgreSQL access is working!")
    
except psycopg2.OperationalError as e:
    print(f" Connection failed: {e}")
    print()
    print("Common issues:")
    print("1. Wrong password in SUPABASE_DB_URL")
    print("2. Database URL format incorrect")
    print("3. Network/firewall blocking connection")
    print()
except Exception as e:
    print(f" Error: {e}")
    print()
