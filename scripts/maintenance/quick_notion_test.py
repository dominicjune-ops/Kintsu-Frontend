#!/usr/bin/env python3
"""
Quick Notion Connection Test
Tests the Notion API connection before publishing the roadmap
"""

import os
import asyncio
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_notion_connection():
    """Test Notion API connection"""
    
    print("🔗 Testing Notion API Connection...")
    
    try:
        # Initialize Notion client
        notion = Client(auth=os.getenv("NOTION_TOKEN"))
        
        # Test basic API access
        print(" Notion client initialized")
        
        # Try to list pages (this tests authentication)
        response = notion.search(filter={"property": "object", "value": "page"})
        
        print(f" API connection successful!")
        print(f" Found {len(response['results'])} pages accessible to this integration")
        
        # Show available pages
        if response['results']:
            print("\n Available Pages:")
            for i, page in enumerate(response['results'][:5], 1):  # Show first 5
                title = "Untitled"
                if page.get('properties'):
                    # Try to get title from properties
                    for prop_name, prop_value in page['properties'].items():
                        if prop_value.get('type') == 'title' and prop_value.get('title'):
                            if len(prop_value['title']) > 0:
                                title = prop_value['title'][0]['plain_text']
                                break
                print(f"   {i}. {title} (ID: {page['id']})")
        
        # Test if we can create a simple page
        project_db_id = os.getenv("NOTION_PROJECT_DATABASE_ID")
        if project_db_id:
            print(f"\n Testing project database access...")
            print(f"   Database ID: {project_db_id}")
            
            # Try to create a test page
            test_page = {
                "parent": {"database_id": project_db_id},
                "properties": {
                    "title": {
                        "title": [{"text": {"content": " Notion Connection Test - DELETE ME"}}]
                    }
                },
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "This is a test page to verify the integration is working. You can delete this page."}}]
                        }
                    }
                ]
            }
            
            try:
                test_result = notion.pages.create(**test_page)
                print(f" Successfully created test page!")
                print(f"🔗 Page URL: {test_result['url']}")
                print(f"📄 Page ID: {test_result['id']}")
                
                print("\n Notion integration is ready for roadmap publication!")
                return True
                
            except Exception as e:
                print(f" Failed to create test page: {e}")
                print("💡 Make sure the database is shared with your integration")
                return False
        else:
            print("  NOTION_PROJECT_DATABASE_ID not configured")
            return False
            
    except Exception as e:
        print(f" Connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_notion_connection())