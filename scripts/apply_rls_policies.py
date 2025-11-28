#!/usr/bin/env python3
"""
Apply RLS policies to Supabase database.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print(" Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
    sys.exit(1)

def execute_sql(sql: str) -> bool:
    """Execute SQL using Supabase REST API."""
    url = f"{SUPABASE_URL}/rest/v1/rpc/exec_sql"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json={"query": sql}, headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f" SQL execution failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f" Error executing SQL: {e}")
        return False

def apply_rls_policies():
    """Apply RLS policies from SQL file."""
    print(" Applying RLS policies to Supabase...")

    sql_file = Path("sql/005_rls_policies.sql")
    if not sql_file.exists():
        print(f" RLS policies file not found: {sql_file}")
        return False

    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Split SQL into individual statements (basic approach)
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]

    success_count = 0
    for i, statement in enumerate(statements, 1):
        if statement:
            print(f"  Executing statement {i}/{len(statements)}...")
            if execute_sql(statement):
                success_count += 1
            else:
                print(f"   Failed to execute statement {i}")
                return False

    print(f" Successfully applied {success_count} RLS policy statements")
    return True

if __name__ == "__main__":
    success = apply_rls_policies()
    sys.exit(0 if success else 1)