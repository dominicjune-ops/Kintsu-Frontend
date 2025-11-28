#!/usr/bin/env python3
"""
CareerCoach.ai Product Backlog Board Creator
Creates comprehensive product management board in Notion
"""

import os
import asyncio
from datetime import datetime, timedelta
from notion_client import Client
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class ProductBacklogCreator:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        
    async def create_backlog_database(self):
        """Create product backlog database in Notion"""
        
        database_content = {
            "parent": {"page_id": "28c2baee-2b65-8093-b50b-d8602a284ba8"},  # Main CareerCoach page
            "title": [{"type": "text", "text": {"content": " CareerCoach.ai Product Backlog"}}],
            "properties": {
                "Feature": {
                    "title": {}
                },
                "Status": {
                    "select": {
                        "options": [
                            {"name": " Backlog", "color": "gray"},
                            {"name": " Sprint Ready", "color": "yellow"},
                            {"name": " In Progress", "color": "blue"},
                            {"name": "👀 Review", "color": "orange"},
                            {"name": " Complete", "color": "green"},
                            {"name": " Released", "color": "purple"}
                        ]
                    }
                },
                "Priority": {
                    "select": {
                        "options": [
                            {"name": "🔥 Critical", "color": "red"},
                            {"name": " High", "color": "orange"},
                            {"name": " Medium", "color": "yellow"},
                            {"name": " Low", "color": "gray"}
                        ]
                    }
                },
                "Epic": {
                    "select": {
                        "options": [
                            {"name": " Phase 1: Core Automation", "color": "green"},
                            {"name": " Phase 2: Telemetry & Governance", "color": "blue"},
                            {"name": "👥 Phase 3: Communication & Visibility", "color": "purple"},
                            {"name": "🤖 Phase 4: AI & Redundancy", "color": "red"},
                            {"name": "🎨 Branding & UI", "color": "pink"},
                            {"name": " Revenue & Growth", "color": "yellow"}
                        ]
                    }
                },
                "Story Points": {
                    "select": {
                        "options": [
                            {"name": "1", "color": "gray"},
                            {"name": "2", "color": "brown"},
                            {"name": "3", "color": "orange"},
                            {"name": "5", "color": "yellow"},
                            {"name": "8", "color": "green"},
                            {"name": "13", "color": "blue"},
                            {"name": "21", "color": "purple"}
                        ]
                    }
                },
                "Sprint": {
                    "select": {
                        "options": [
                            {"name": "Current Sprint", "color": "green"},
                            {"name": "Next Sprint", "color": "yellow"},
                            {"name": "Future Sprint", "color": "gray"},
                            {"name": "Backlog", "color": "gray"}
                        ]
                    }
                },
                "Assignee": {
                    "people": {}
                },
                "Due Date": {
                    "date": {}
                },
                "Business Value": {
                    "select": {
                        "options": [
                            {"name": " Revenue Impact", "color": "green"},
                            {"name": "👥 User Experience", "color": "blue"},
                            {"name": " Performance", "color": "orange"},
                            {"name": " Security", "color": "red"},
                            {"name": " Analytics", "color": "purple"},
                            {"name": " Scalability", "color": "yellow"}
                        ]
                    }
                },
                "Description": {
                    "rich_text": {}
                },
                "Acceptance Criteria": {
                    "rich_text": {}
                }
            }
        }
        
        try:
            response = self.notion.databases.create(**database_content)
            return response
        except Exception as e:
            print(f"Error creating backlog database: {e}")
            return None
    
    async def populate_initial_backlog(self, database_id):
        """Populate the backlog with initial user stories"""
        
        user_stories = [
            {
                "Feature": "Logo Integration Completion",
                "Status": " In Progress",
                "Priority": "🔥 Critical",
                "Epic": "🎨 Branding & UI",
                "Story Points": "3",
                "Sprint": "Current Sprint",
                "Business Value": "👥 User Experience",
                "Description": "Complete integration of CareerCoach.ai logo across all platform touchpoints including UI, documentation, emails, and Notion pages.",
                "Acceptance Criteria": "- Logo appears in main UI header\n- Documentation includes branded headers\n- Email templates use logo\n- Notion roadmap includes branding\n- All file formats supported (PNG, SVG, JPG)"
            },
            {
                "Feature": "Real-time Job Scraper",
                "Status": " Backlog",
                "Priority": " High",
                "Epic": " Phase 1: Core Automation",
                "Story Points": "8",
                "Sprint": "Next Sprint",
                "Business Value": " Revenue Impact",
                "Description": "Implement production-ready Google Jobs scraper with error handling, rate limiting, and data validation.",
                "Acceptance Criteria": "- Scrapes 100+ jobs daily\n- Handles rate limiting gracefully\n- Validates job data quality\n- Integrates with existing pipeline\n- Error monitoring and alerts"
            },
            {
                "Feature": "Advanced KPI Dashboard",
                "Status": " Backlog",
                "Priority": " High",
                "Epic": " Phase 2: Telemetry & Governance",
                "Story Points": "13",
                "Sprint": "Future Sprint",
                "Business Value": " Analytics",
                "Description": "Create comprehensive KPI dashboard with real-time metrics, investor views, and automated reporting.",
                "Acceptance Criteria": "- Real-time metric updates\n- Investor-ready views\n- Automated weekly reports\n- Custom KPI definitions\n- Export capabilities"
            },
            {
                "Feature": "Slack Integration",
                "Status": " Backlog",
                "Priority": " Medium",
                "Epic": "👥 Phase 3: Communication & Visibility",
                "Story Points": "5",
                "Sprint": "Future Sprint",
                "Business Value": "👥 User Experience",
                "Description": "Integrate with Slack for real-time notifications, slash commands, and team collaboration features.",
                "Acceptance Criteria": "- Real-time job alerts\n- Slash commands for queries\n- KPI breach notifications\n- Team collaboration features\n- Custom notification settings"
            },
            {
                "Feature": "AI Job Matching",
                "Status": " Backlog",
                "Priority": " Medium",
                "Epic": "🤖 Phase 4: AI & Redundancy",
                "Story Points": "21",
                "Sprint": "Backlog",
                "Business Value": " Revenue Impact",
                "Description": "Implement AI-powered job matching algorithm to improve user experience and increase conversion rates.",
                "Acceptance Criteria": "- ML-based matching algorithm\n- User preference learning\n- A/B testing framework\n- Performance analytics\n- Personalization features"
            },
            {
                "Feature": "Premium Subscription Model",
                "Status": " Backlog",
                "Priority": "🔥 Critical",
                "Epic": " Revenue & Growth",
                "Story Points": "13",
                "Sprint": "Next Sprint",
                "Business Value": " Revenue Impact",
                "Description": "Implement premium subscription tiers with advanced features, priority support, and enhanced job matching.",
                "Acceptance Criteria": "- Multiple subscription tiers\n- Payment processing integration\n- Feature gating system\n- Billing management\n- Analytics tracking"
            },
            {
                "Feature": "Mobile-Responsive UI",
                "Status": " Backlog",
                "Priority": " High",
                "Epic": "🎨 Branding & UI",
                "Story Points": "8",
                "Sprint": "Future Sprint",
                "Business Value": "👥 User Experience",
                "Description": "Optimize the platform for mobile devices with responsive design and mobile-first approach.",
                "Acceptance Criteria": "- Responsive design for all screen sizes\n- Touch-friendly interface\n- Fast loading on mobile\n- PWA capabilities\n- App store readiness"
            },
            {
                "Feature": "Advanced Search & Filters",
                "Status": " Backlog",
                "Priority": " High",
                "Epic": "👥 Phase 3: Communication & Visibility",
                "Story Points": "8",
                "Sprint": "Future Sprint",
                "Business Value": "👥 User Experience",
                "Description": "Enhance job search with advanced filtering, sorting, and search capabilities including location, salary, skills, and company filters.",
                "Acceptance Criteria": "- Multiple filter combinations\n- Real-time search results\n- Saved search preferences\n- Search analytics\n- Auto-complete functionality"
            },
            {
                "Feature": "Company Insights Dashboard",
                "Status": " Backlog",
                "Priority": " Medium",
                "Epic": " Phase 2: Telemetry & Governance",
                "Story Points": "13",
                "Sprint": "Backlog",
                "Business Value": "👥 User Experience",
                "Description": "Provide detailed company insights including culture, benefits, interview processes, and employee reviews.",
                "Acceptance Criteria": "- Company profile pages\n- Employee review integration\n- Benefits comparison\n- Interview process guides\n- Culture insights"
            },
            {
                "Feature": "API Rate Limiting & Security",
                "Status": " Backlog",
                "Priority": "🔥 Critical",
                "Epic": " Phase 2: Telemetry & Governance",
                "Story Points": "5",
                "Sprint": "Next Sprint",
                "Business Value": " Security",
                "Description": "Implement comprehensive API security including rate limiting, authentication, and monitoring.",
                "Acceptance Criteria": "- JWT authentication\n- Rate limiting per user/IP\n- API key management\n- Security monitoring\n- Intrusion detection"
            }
        ]
        
        created_items = []
        
        for story in user_stories:
            page_content = {
                "parent": {"database_id": database_id},
                "properties": {
                    "Feature": {
                        "title": [{"text": {"content": story["Feature"]}}]
                    },
                    "Status": {
                        "select": {"name": story["Status"]}
                    },
                    "Priority": {
                        "select": {"name": story["Priority"]}
                    },
                    "Epic": {
                        "select": {"name": story["Epic"]}
                    },
                    "Story Points": {
                        "select": {"name": story["Story Points"]}
                    },
                    "Sprint": {
                        "select": {"name": story["Sprint"]}
                    },
                    "Business Value": {
                        "select": {"name": story["Business Value"]}
                    },
                    "Description": {
                        "rich_text": [{"text": {"content": story["Description"]}}]
                    },
                    "Acceptance Criteria": {
                        "rich_text": [{"text": {"content": story["Acceptance Criteria"]}}]
                    }
                }
            }
            
            try:
                result = self.notion.pages.create(**page_content)
                created_items.append(result)
                print(f" Created: {story['Feature']}")
            except Exception as e:
                print(f" Failed to create: {story['Feature']} - {e}")
        
        return created_items

async def main():
    """Create product backlog board"""
    creator = ProductBacklogCreator()
    
    print(" Creating CareerCoach.ai Product Backlog Board...")
    
    # Create database
    database = await creator.create_backlog_database()
    
    if database:
        print(f" Backlog database created!")
        print(f"📄 Database ID: {database['id']}")
        print(f"🔗 URL: {database['url']}")
        
        # Populate with initial stories
        print("\n Populating initial user stories...")
        items = await creator.populate_initial_backlog(database['id'])
        
        # Save backlog info
        backlog_info = {
            "created_at": datetime.now().isoformat(),
            "notion_database_id": database['id'],
            "notion_url": database['url'],
            "type": "product_backlog",
            "total_items": len(items),
            "status": "active"
        }
        
        with open("product_backlog_info.json", "w") as f:
            json.dump(backlog_info, f, indent=2)
        
        print(f"\n Backlog Summary:")
        print(f"• Created {len(items)} initial user stories")
        print(f"• 6 different epics configured")
        print(f"• Sprint planning ready")
        print(f"• Priority matrix established")
        
        print("\n Next Steps:")
        print("1.  Create Launch Tracker")
        print("2.  Review and prioritize backlog items")
        print("3.  Plan next sprint")
        print("4. 👥 Assign team members")
        
    else:
        print(" Failed to create backlog database")

if __name__ == "__main__":
    asyncio.run(main())