#!/usr/bin/env python3
"""
🔗 Kintsu Notion Integration Setup
Using your actual Notion integration token
"""

import requests
import json
import os
from datetime import datetime

class NotionIntegration:
    def __init__(self):
        # Notion integration token - Set via environment variable
        self.token = os.getenv("NOTION_API_TOKEN")
        if not self.token:
            raise ValueError("NOTION_API_TOKEN environment variable not set")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.notion.com/v1"
    
    def test_connection(self):
        """Test if the Notion integration is working"""
        try:
            response = requests.get(f"{self.base_url}/users", headers=self.headers)
            if response.status_code == 200:
                print(" Notion integration connected successfully!")
                return True
            else:
                print(f" Connection failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f" Connection error: {e}")
            return False
    
    def create_database(self, parent_page_id, database_config):
        """Create a new database in Notion"""
        try:
            url = f"{self.base_url}/databases"
            payload = {
                "parent": {"page_id": parent_page_id},
                "title": [{"text": {"content": database_config["title"]}}],
                "properties": database_config["properties"]
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                db_data = response.json()
                print(f" Created database: {database_config['title']}")
                return db_data["id"]
            else:
                print(f" Failed to create database: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f" Database creation error: {e}")
            return None
    
    def add_database_entry(self, database_id, entry_data):
        """Add an entry to a Notion database"""
        try:
            url = f"{self.base_url}/pages"
            payload = {
                "parent": {"database_id": database_id},
                "properties": entry_data
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                print(" Entry added successfully!")
                return response.json()
            else:
                print(f" Failed to add entry: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f" Entry creation error: {e}")
            return None

def get_database_schemas():
    """Define the database schemas for Kintsu"""
    
    # Deploy Tracking Database
    deploy_tracking = {
        "title": " Deploy Tracking & Audit",
        "properties": {
            "Deploy ID": {"title": {}},
            "Timestamp": {"date": {}},
            "Commit Hash": {"rich_text": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": " Success", "color": "green"},
                        {"name": " Failed", "color": "red"},
                        {"name": "🟡 In Progress", "color": "yellow"}
                    ]
                }
            },
            "Performance Impact": {"rich_text": {}},
            "Investor Notes": {"rich_text": {}},
            "Environment": {
                "select": {
                    "options": [
                        {"name": "Production", "color": "green"},
                        {"name": "Staging", "color": "yellow"},
                        {"name": "Development", "color": "blue"}
                    ]
                }
            },
            "Cost Impact": {"rich_text": {}}
        }
    }
    
    # Investor KPI Dashboard
    investor_kpis = {
        "title": " Investor KPI Dashboard",
        "properties": {
            "Metric": {"title": {}},
            "Current Value": {"rich_text": {}},
            "Target": {"rich_text": {}},
            "Trend": {
                "select": {
                    "options": [
                        {"name": " Improving", "color": "green"},
                        {"name": " Stable", "color": "yellow"},
                        {"name": "📉 Declining", "color": "red"},
                        {"name": " Exceeding", "color": "purple"}
                    ]
                }
            },
            "Impact": {"rich_text": {}},
            "Last Updated": {"date": {}}
        }
    }
    
    # GitHub Activity Triage
    github_triage = {
        "title": " GitHub Activity Triage",
        "properties": {
            "Type": {
                "select": {
                    "options": [
                        {"name": "CI/CD", "color": "blue"},
                        {"name": "Deploy Success", "color": "green"},
                        {"name": "PR Review", "color": "yellow"},
                        {"name": "Issue", "color": "red"},
                        {"name": "Workflow", "color": "purple"}
                    ]
                }
            },
            "Repo": {
                "select": {
                    "options": [
                        {"name": "Kintsu", "color": "green"},
                        {"name": "Other", "color": "gray"}
                    ]
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": " Resolved", "color": "green"},
                        {"name": "🟡 Open", "color": "yellow"},
                        {"name": " Assigned", "color": "blue"}
                    ]
                }
            },
            "Action Needed": {"rich_text": {}},
            "Linked Commit": {"rich_text": {}},
            "Priority": {
                "select": {
                    "options": [
                        {"name": " High", "color": "red"},
                        {"name": " Medium", "color": "yellow"},
                        {"name": " Low", "color": "green"}
                    ]
                }
            },
            "Resolution": {"rich_text": {}}
        }
    }
    
    return {
        "deploy_tracking": deploy_tracking,
        "investor_kpis": investor_kpis,
        "github_triage": github_triage
    }

def create_baseline_entries():
    """Create the baseline entries for Nov 3, 2025 milestone"""
    
    # Deploy Tracking Entry
    deploy_entry = {
        "Deploy ID": {"title": [{"text": {"content": "BASELINE-d2b42c0e"}}]},
        "Timestamp": {"date": {"start": "2025-11-03T22:30:00.000Z"}},
        "Commit Hash": {"rich_text": [{"text": {"content": "d2b42c0e"}}]},
        "Status": {"select": {"name": " Success"}},
        "Performance Impact": {"rich_text": [{"text": {"content": "26x job search + 31x AI response improvements"}}]},
        "Investor Notes": {"rich_text": [{"text": {"content": " FUNDABLE MILESTONE: Production-grade maturity achieved"}}]},
        "Environment": {"select": {"name": "Production"}},
        "Cost Impact": {"rich_text": [{"text": {"content": "$125/month operational savings"}}]}
    }
    
    # KPI Entries
    kpi_entries = [
        {
            "Metric": {"title": [{"text": {"content": "Job Search Performance"}}]},
            "Current Value": {"rich_text": [{"text": {"content": "0.2 seconds"}}]},
            "Target": {"rich_text": [{"text": {"content": "< 0.5 seconds"}}]},
            "Trend": {"select": {"name": " Exceeding"}},
            "Impact": {"rich_text": [{"text": {"content": " Competitive advantage - industry leadership"}}]},
            "Last Updated": {"date": {"start": "2025-11-03"}}
        },
        {
            "Metric": {"title": [{"text": {"content": "AI Response Time"}}]},
            "Current Value": {"rich_text": [{"text": {"content": "0.1 seconds"}}]},
            "Target": {"rich_text": [{"text": {"content": "< 1 second"}}]},
            "Trend": {"select": {"name": " Exceeding"}},
            "Impact": {"rich_text": [{"text": {"content": " Technical moat - user experience"}}]},
            "Last Updated": {"date": {"start": "2025-11-03"}}
        },
        {
            "Metric": {"title": [{"text": {"content": "Cost Efficiency"}}]},
            "Current Value": {"rich_text": [{"text": {"content": "68.7% reduction"}}]},
            "Target": {"rich_text": [{"text": {"content": "50% reduction"}}]},
            "Trend": {"select": {"name": " Exceeding"}},
            "Impact": {"rich_text": [{"text": {"content": " ROI demonstration - 17.9x return"}}]},
            "Last Updated": {"date": {"start": "2025-11-03"}}
        }
    ]
    
    # GitHub Entry
    github_entry = {
        "Type": {"select": {"name": "Deploy Success"}},
        "Repo": {"select": {"name": "Kintsu"}},
        "Status": {"select": {"name": " Resolved"}},
        "Action Needed": {"rich_text": [{"text": {"content": "Monitor performance metrics"}}]},
        "Linked Commit": {"rich_text": [{"text": {"content": "d2b42c0e"}}]},
        "Priority": {"select": {"name": " High"}},
        "Resolution": {"rich_text": [{"text": {"content": "All 3 optimization options deployed successfully"}}]}
    }
    
    return {
        "deploy_entry": deploy_entry,
        "kpi_entries": kpi_entries,
        "github_entry": github_entry
    }

def main():
    """Set up Notion integration with Kintsu databases"""
    
    print("🔗 Setting up Kintsu Notion Integration")
    print("=" * 50)
    
    # Initialize Notion integration
    notion = NotionIntegration()
    
    # Test connection
    if not notion.test_connection():
        print(" Please check your Notion integration setup")
        return
    
    print("\n NEXT STEPS FOR NOTION SETUP:")
    print("1. Create a parent page in Notion called 'Kintsu Dashboard'")
    print("2. Share this page with your Kintsu integration")
    print("3. Get the page ID and run the database creation script")
    print("4. Import the baseline milestone data")

    # Save the setup configuration
    setup_config = {
        "integration_token": os.getenv("NOTION_API_TOKEN", "SET_NOTION_API_TOKEN_ENV_VAR"),
        "database_schemas": get_database_schemas(),
        "baseline_entries": create_baseline_entries(),
        "setup_instructions": [
            "Create parent page: 'Kintsu Dashboard'",
            "Share page with Kintsu integration",
            "Run database creation with parent page ID",
            "Import baseline milestone data",
            "Set up Make.com webhook for automated logging"
        ]
    }
    
    with open("notion_setup_config.json", "w") as f:
        json.dump(setup_config, f, indent=2)
    
    print("\n Generated: notion_setup_config.json")
    print(" This file contains your integration token and database schemas")
    print("🔗 Use this to complete your Notion setup manually")
    
    print(f"\n YOUR INTEGRATION TOKEN:")
    print(f"   {notion.token}")
    print(f"\n💡 Add this to your Render environment variables as NOTION_TOKEN")

if __name__ == "__main__":
    main()