"""
Test SQLAlchemy connection to Supabase PostgreSQL
This bypasses PostgREST and uses direct database driver
"""
import asyncio
from sqlalchemy import text
from database.config import async_engine, engine

async def test_async_connection():
    """Test async connection to Supabase"""
    print("🔌 Testing async PostgreSQL connection to Supabase...\n")
    
    try:
        async with async_engine.connect() as conn:
            # Test basic query
            result = await conn.execute(text("SELECT current_database(), current_user, version()"))
            row = result.fetchone()
            
            print(" Connection successful!")
            print(f"   Database: {row[0]}")
            print(f"   User: {row[1]}")
            print(f"   PostgreSQL: {row[2][:50]}...")
            print()
            
            # List tables in public schema
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
                LIMIT 20
            """))
            tables = [row[0] for row in result.fetchall()]
            
            print(f" Found {len(tables)} tables in public schema:")
            for table in tables:
                print(f"   • {table}")
            print()
            
            # Get row counts for key tables
            key_tables = ['candidates', 'job_postings', 'applications', 'resumes']
            print(" Record counts:")
            for table in key_tables:
                if table in tables:
                    try:
                        result = await conn.execute(text(f"SELECT COUNT(*) FROM public.{table}"))
                        count = result.fetchone()[0]
                        print(f"   • {table}: {count} records")
                    except Exception as e:
                        print(f"   • {table}: Error - {str(e)[:50]}")
            
            return True
            
    except Exception as e:
        print(f" Connection failed: {e}")
        return False

def test_sync_connection():
    """Test sync connection (for migrations)"""
    print("\n🔌 Testing sync PostgreSQL connection...\n")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database()"))
            db = result.fetchone()[0]
            print(f" Sync connection successful!")
            print(f"   Database: {db}")
            return True
    except Exception as e:
        print(f" Sync connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test async connection
    async_result = asyncio.run(test_async_connection())
    
    # Test sync connection
    sync_result = test_sync_connection()
    
    print("\n" + "=" * 80)
    print(" SUMMARY")
    print("=" * 80)
    if async_result and sync_result:
        print(" SUCCESS! Both async and sync connections work!")
        print()
        print(" Next steps:")
        print("   1. Update SQLAlchemy models to match Supabase schema")
        print("   2. Test API endpoints with real Supabase data")
        print("   3. Create/update seed data in Supabase")
    else:
        print("  Some connections failed. Check errors above.")
