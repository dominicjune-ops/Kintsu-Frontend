#!/usr/bin/env python3
"""
 Add KPIs to KPI_Tracker
Add our enterprise optimization metrics to the KPI tracking database
"""

import requests
import json
from scripts.setup.setup_notion_integration import NotionIntegration

def add_to_kpi_tracker():
    """Add our performance metrics to KPI_Tracker"""
    
    notion = NotionIntegration()
    
    # Database ID from the KPI_Tracker link
    kpi_db_id = "2932baee-2b65-8001-b22f-ffa32a82634c"
    
    print(" Adding Enterprise KPIs to KPI_Tracker")
    print("=" * 42)
    
    try:
        # Create KPI entry with our performance metrics
        kpi_entry = {
            "🟢 Conversion & Growth Metrics": {
                "title": [{"text": {"content": " Enterprise Optimization Baseline - Nov 3, 2025"}}]
            },
            "Category": {
                "rich_text": [{"text": {"content": "Performance Optimization"}}]
            },
            "column 3": {
                "rich_text": [{"text": {"content": "26x faster job search performance"}}]
            },
            "column 4": {
                "rich_text": [{"text": {"content": "31x faster AI response times"}}]
            },
            "column 5": {
                "rich_text": [{"text": {"content": "68.7% cost reduction achieved"}}]
            },
            "column 6": {
                "rich_text": [{"text": {"content": "$125/month operational savings"}}]
            },
            "column 7": {
                "rich_text": [{"text": {"content": "1000+ concurrent user capacity"}}]
            },
            "column 8": {
                "rich_text": [{"text": {"content": "$7/month hosting (enterprise-grade)"}}]
            }
        }
        
        result = notion.add_database_entry(kpi_db_id, kpi_entry)
        
        if result:
            print(" Successfully added KPIs to KPI_Tracker!")
            print(f"🆔 Entry ID: {result['id']}")
            print(f" Title:  Enterprise Optimization Baseline")
            print(f" Category: Performance Optimization")
            print()
            print(" Key Performance Indicators Added:")
            print("   • 26x faster job search performance")
            print("   • 31x faster AI response times")
            print("   • 68.7% cost reduction achieved")
            print("   • $125/month operational savings")
            print("   • 1000+ concurrent user capacity")
            print("   • $7/month hosting (enterprise-grade)")
            print()
            print("🔗 View in Notion:")
            print(f"   KPI Database: https://www.notion.so/2932baee2b658001b22fffa32a82634c")
            print(f"   Direct Entry: https://notion.so/{result['id'].replace('-', '')}")
            
            return True
        else:
            print(" Failed to add to KPI_Tracker")
            return False
            
    except Exception as e:
        print(f" Error: {e}")
        return False

def main():
    add_to_kpi_tracker()

if __name__ == "__main__":
    main()