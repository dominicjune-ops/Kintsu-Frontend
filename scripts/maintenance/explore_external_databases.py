"""
Explore what data exists in Airtable and Notion
"""
import os
from dotenv import load_dotenv
import requests
from typing import Dict, List, Any

load_dotenv()

print("=" * 80)
print("EXPLORING EXTERNAL DATABASES")
print("=" * 80)

# ============================================================================
# NOTION EXPLORATION
# ============================================================================
notion_token = os.getenv("NOTION_TOKEN")
notion_db_id = os.getenv("NOTION_JOBS_DATABASE_ID")

print("\n" + "=" * 80)
print("NOTION")
print("=" * 80)

if notion_token and "your_notion" not in notion_token:
    print("\n Notion credentials found!")
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # Search for databases
    print("\nSearching for Notion databases...")
    try:
        search_response = requests.post(
            "https://api.notion.com/v1/search",
            headers=headers,
            json={
                "filter": {
                    "property": "object",
                    "value": "database"
                }
            }
        )
        
        if search_response.status_code == 200:
            databases = search_response.json().get("results", [])
            print(f"\n Found {len(databases)} Notion databases:")
            
            for i, db in enumerate(databases, 1):
                db_id = db.get("id", "")
                title = ""
                if "title" in db:
                    title_parts = db["title"]
                    if title_parts:
                        title = title_parts[0].get("plain_text", "Untitled")
                
                print(f"\n{i}. {title}")
                print(f"   ID: {db_id}")
                print(f"   URL: {db.get('url', 'N/A')}")
                
                # Try to get schema
                if db_id:
                    db_response = requests.get(
                        f"https://api.notion.com/v1/databases/{db_id}",
                        headers=headers
                    )
                    if db_response.status_code == 200:
                        db_data = db_response.json()
                        properties = db_data.get("properties", {})
                        print(f"   Properties ({len(properties)}):")
                        for prop_name, prop_info in list(properties.items())[:10]:
                            prop_type = prop_info.get("type", "unknown")
                            print(f"      - {prop_name}: {prop_type}")
                        
                        if len(properties) > 10:
                            print(f"      ... and {len(properties) - 10} more")
                        
                        # Get record count
                        query_response = requests.post(
                            f"https://api.notion.com/v1/databases/{db_id}/query",
                            headers=headers,
                            json={"page_size": 1}
                        )
                        if query_response.status_code == 200:
                            results = query_response.json().get("results", [])
                            has_more = query_response.json().get("has_more", False)
                            count = "1+" if (results and has_more) else str(len(results))
                            print(f"   Records: {count}")
        else:
            print(f" Error searching Notion: {search_response.status_code}")
            print(search_response.text)
            
    except Exception as e:
        print(f" Error connecting to Notion: {str(e)}")
else:
    print("\n  Notion credentials not configured")

# ============================================================================
# AIRTABLE EXPLORATION
# ============================================================================
airtable_key = os.getenv("AIRTABLE_API_KEY")
airtable_base = os.getenv("AIRTABLE_BASE_ID")

print("\n" + "=" * 80)
print("AIRTABLE")
print("=" * 80)

if airtable_key and "your_airtable" not in airtable_key:
    print("\n Airtable credentials found!")
    print(f"   Base ID: {airtable_base}")
    
    headers = {
        "Authorization": f"Bearer {airtable_key}",
        "Content-Type": "application/json"
    }
    
    # Get base schema
    print("\nFetching Airtable base schema...")
    try:
        # First, get the base metadata
        schema_response = requests.get(
            f"https://api.airtable.com/v0/meta/bases/{airtable_base}/tables",
            headers=headers
        )
        
        if schema_response.status_code == 200:
            tables = schema_response.json().get("tables", [])
            print(f"\n Found {len(tables)} Airtable tables:")
            
            for i, table in enumerate(tables, 1):
                table_id = table.get("id", "")
                table_name = table.get("name", "Untitled")
                
                print(f"\n{i}. {table_name}")
                print(f"   ID: {table_id}")
                
                # Get fields
                fields = table.get("fields", [])
                print(f"   Fields ({len(fields)}):")
                for field in fields[:10]:
                    field_name = field.get("name", "Unknown")
                    field_type = field.get("type", "unknown")
                    print(f"      - {field_name}: {field_type}")
                
                if len(fields) > 10:
                    print(f"      ... and {len(fields) - 10} more")
                
                # Try to get record count
                try:
                    records_response = requests.get(
                        f"https://api.airtable.com/v0/{airtable_base}/{table_id}",
                        headers=headers,
                        params={"maxRecords": 1}
                    )
                    if records_response.status_code == 200:
                        records_data = records_response.json()
                        offset = records_data.get("offset")
                        count = "1+" if offset else str(len(records_data.get("records", [])))
                        print(f"   Records: {count}")
                except Exception as e:
                    print(f"   Records: Unable to fetch ({str(e)[:50]})")
                    
        else:
            print(f" Error fetching Airtable schema: {schema_response.status_code}")
            print(schema_response.text)
            
    except Exception as e:
        print(f" Error connecting to Airtable: {str(e)}")
else:
    print("\n  Airtable credentials not configured")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("""
Based on the databases found, I can help you:
1. Identify which data should migrate to Supabase
2. Create migration scripts
3. Set up sync between systems if needed
""")
