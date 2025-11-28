"""
Discover the actual structure of the user_preferences table
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
print("DISCOVERING ACTUAL TABLE STRUCTURE")
print("=" * 80)

# Try to get any record to see the actual columns
try:
    result = supabase.table('user_preferences').select('*').limit(1).execute()
    
    if result.data:
        print("\n Found existing data. Columns in the table:")
        for key in result.data[0].keys():
            print(f"  - {key}")
    else:
        print("\n  Table exists but is empty.")
        print("Cannot determine column structure from data.")
        print("\nTrying to insert a minimal test record to discover required fields...")
        
        # Try minimal insert
        try:
            test_result = supabase.table('user_preferences').insert({}).execute()
        except Exception as insert_error:
            error_msg = str(insert_error)
            print(f"\n Insert error: {error_msg}")
            
            # Parse error to find required columns
            if "null value in column" in error_msg:
                print("\nThis tells us which columns are required (NOT NULL)")
                
except Exception as e:
    print(f"\n Error: {str(e)}")

print("\n" + "=" * 80)
print("RECOMMENDATION:")
print("=" * 80)
print("""
The table exists but has a different structure than expected.

Options:
1. DROP the existing table and run the migration fresh
2. ALTER the existing table to add missing columns
3. Check Supabase Dashboard to see the actual structure

Let me know which option you prefer!
""")
