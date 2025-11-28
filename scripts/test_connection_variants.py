"""
Try different Supabase connection methods
"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Get credentials
project_ref = "ktitfajlacjysacdsfxf"
password = "t5XVwvfXnYYwQe3g"

# Try different connection strings
connection_strings = [
    # Direct connection (port 5432)
    f"postgresql://postgres.{project_ref}:{password}@aws-0-us-east-1.pooler.supabase.com:5432/postgres",
    # Pooler connection (port 6543)
    f"postgresql://postgres.{project_ref}:{password}@aws-0-us-east-1.pooler.supabase.com:6543/postgres",
    # Transaction mode
    f"postgresql://postgres:{password}@db.{project_ref}.supabase.co:5432/postgres",
    # Session mode
    f"postgresql://postgres:{password}@db.{project_ref}.supabase.co:6543/postgres",
]

print("🔌 Testing different connection strings...\n")

for i, conn_str in enumerate(connection_strings, 1):
    # Hide password in output
    display_str = conn_str.replace(password, "***")
    print(f"Attempt {i}: {display_str}")
    
    try:
        conn = psycopg2.connect(conn_str, connect_timeout=5)
        print(" SUCCESS! This connection works!\n")
        
        # Test a simple query
        cur = conn.cursor()
        cur.execute("SELECT current_database(), current_user;")
        db, user = cur.fetchone()
        print(f"   Database: {db}")
        print(f"   User: {user}")
        
        # Get table count
        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
        count = cur.fetchone()[0]
        print(f"   Tables in public schema: {count}")
        
        cur.close()
        conn.close()
        
        print(f"\n Use this connection string in your .env:")
        print(f"SUPABASE_DB_URL={conn_str}")
        break
        
    except Exception as e:
        error_msg = str(e)
        if "Tenant or user not found" in error_msg:
            print(" Tenant/user not found")
        elif "timeout" in error_msg.lower():
            print(" Connection timeout")
        elif "password" in error_msg.lower():
            print(" Authentication failed")
        else:
            print(f" {error_msg[:100]}")
        print()
