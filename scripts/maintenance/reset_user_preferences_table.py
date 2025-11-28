"""
Drop and recreate user_preferences table with correct structure
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

print("=" * 80)
print("RESETTING user_preferences TABLE")
print("=" * 80)

# Read the migration SQL file
migration_file = "migrations/001_create_user_preferences.sql"
print(f"\nReading migration file: {migration_file}")

with open(migration_file, 'r') as f:
    migration_sql = f.read()

# Prepare the DROP and CREATE statements
drop_sql = """
-- Drop existing table and related objects
DROP TABLE IF EXISTS public.user_preferences CASCADE;
DROP TYPE IF EXISTS work_mode_enum CASCADE;
DROP TYPE IF EXISTS experience_level_enum CASCADE;
DROP TYPE IF EXISTS notification_frequency_enum CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
"""

print("\n" + "=" * 80)
print("STEP 1: Dropping existing table and types")
print("=" * 80)
print(drop_sql)

# Note: Supabase Python client doesn't support raw SQL execution directly
# We need to use the SQL editor or REST API
print("\n  The Python Supabase client doesn't support raw SQL execution.")
print("We need to execute this via the Supabase Dashboard SQL Editor.")
print("\nPlease follow these steps:")
print("\n1. Open: https://supabase.com/dashboard/project/ktitfajlacjysacdsfxf/sql/new")
print("\n2. Copy and paste this DROP statement:")
print("\n" + "-" * 80)
print(drop_sql)
print("-" * 80)

print("\n3. Click 'Run' (or press F5)")
print("\n4. Then copy and paste the CREATE statement from:")
print(f"   {os.path.abspath(migration_file)}")

print("\n5. Click 'Run' again")

print("\n" + "=" * 80)
print("ALTERNATIVE: Use the run_migration.py script")
print("=" * 80)
print("\nOr I can help you run the migration programmatically.")
print("Would you like me to try that instead?")
print("\n" + "=" * 80)

# Create a combined SQL file for easy execution
combined_sql_file = "migrations/reset_and_create_user_preferences.sql"
print(f"\nCreating combined SQL file: {combined_sql_file}")

with open(combined_sql_file, 'w') as f:
    f.write("-- Reset and Create user_preferences table\n")
    f.write("-- Generated: " + str(__import__('datetime').datetime.now()) + "\n\n")
    f.write(drop_sql)
    f.write("\n")
    f.write(migration_sql)

print(f" Created: {combined_sql_file}")
print("\nYou can now execute this file in Supabase SQL Editor!")
