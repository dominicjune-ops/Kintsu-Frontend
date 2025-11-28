"""
KPI Dashboard Setup and Data Collection

This script automatically sets up the CareerCoach KPI Dashboard in Notion and 
provides real-time data collection for connector performance and Epic 2 milestones.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging
from dataclasses import dataclass, asdict
import asyncio
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class ConnectorMetrics:
    """Data class for connector performance metrics"""
    connector: str
    date: str
    jobs_ingested_daily: int = 0
    unique_jobs_daily: int = 0
    schema_failures: int = 0
    data_quality_failures: int = 0
    enrichment_failures: int = 0
    avg_intelligence_score: float = 0.0
    jobs_with_salary: int = 0
    jobs_with_skills: int = 0
    jobs_with_experience: int = 0
    pipeline_latency_avg: float = 0.0
    pipeline_latency_p95: float = 0.0
    api_response_time: float = 0.0
    rate_limit_hits: int = 0
    last_sync: str = ""
    
    def calculate_derived_metrics(self) -> Dict[str, float]:
        """Calculate derived KPI metrics"""
        if self.jobs_ingested_daily == 0:
            return {
                "deduplication_rate": 0.0,
                "validation_pass_rate": 0.0,
                "error_rate": 0.0,
                "enrichment_coverage": 0.0,
                "health_score": 0.0
            }
        
        deduplication_rate = (self.unique_jobs_daily / self.jobs_ingested_daily) * 100
        
        total_failures = self.schema_failures + self.data_quality_failures + self.enrichment_failures
        validation_pass_rate = ((self.jobs_ingested_daily - total_failures) / self.jobs_ingested_daily) * 100
        error_rate = (total_failures / self.jobs_ingested_daily) * 100
        
        enrichment_jobs = self.jobs_with_salary + self.jobs_with_skills + self.jobs_with_experience
        enrichment_coverage = (enrichment_jobs / (self.jobs_ingested_daily * 3)) * 100
        
        # Health score calculation (0-100)
        health_score = ((100 - error_rate) + validation_pass_rate + (enrichment_coverage / 100 * 50)) / 2.5
        
        return {
            "deduplication_rate": round(deduplication_rate, 2),
            "validation_pass_rate": round(validation_pass_rate, 2),
            "error_rate": round(error_rate, 2),
            "enrichment_coverage": round(enrichment_coverage, 2),
            "health_score": round(health_score, 2)
        }


class NotionKPIDashboard:
    """Manages KPI dashboard in Notion"""
    
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.connector_db_id = None
        self.milestone_db_id = None
    
    def create_connector_performance_database(self) -> str:
        """Create the Connector Performance Dashboard database"""
        database_config = {
            "parent": {"type": "page_id", "page_id": os.getenv("NOTION_PARENT_PAGE_ID")},
            "title": [{"type": "text", "text": {"content": "CareerCoach Connector Performance Dashboard"}}],
            "properties": {
                "Connector": {
                    "select": {
                        "options": [
                            {"name": "linkedin", "color": "blue"},
                            {"name": "indeed", "color": "green"},
                            {"name": "ziprecruiter", "color": "orange"},
                            {"name": "google_jobs", "color": "red"},
                            {"name": "bing_jobs", "color": "purple"},
                            {"name": "universal", "color": "gray"}
                        ]
                    }
                },
                "Status": {
                    "select": {
                        "options": [
                            {"name": " Planned", "color": "red"},
                            {"name": "🟡 In Progress", "color": "yellow"},
                            {"name": "🟢 Live", "color": "green"},
                            {"name": " Failed", "color": "red"},
                            {"name": "🔵 Maintenance", "color": "blue"}
                        ]
                    }
                },
                "Date": {"date": {}},
                "Jobs Ingested (Daily)": {"number": {"format": "number"}},
                "Unique Jobs (Daily)": {"number": {"format": "number"}},
                "Schema Failures": {"number": {"format": "number"}},
                "Data Quality Failures": {"number": {"format": "number"}},
                "Enrichment Failures": {"number": {"format": "number"}},
                "Avg Intelligence Score": {"number": {"format": "number_with_commas"}},
                "Jobs with Salary": {"number": {"format": "number"}},
                "Jobs with Skills": {"number": {"format": "number"}},
                "Jobs with Experience": {"number": {"format": "number"}},
                "Pipeline Latency (Avg)": {"number": {"format": "number_with_commas"}},
                "Pipeline Latency (P95)": {"number": {"format": "number_with_commas"}},
                "API Response Time": {"number": {"format": "number"}},
                "Rate Limit Hits": {"number": {"format": "number"}},
                "Last Sync": {"date": {}},
                "Owner": {"people": {}},
                "Notes": {"rich_text": {}},
                # Calculated fields (would need to be added via Notion UI)
                "Deduplication Rate": {"formula": {"expression": "prop(\"Unique Jobs (Daily)\") / prop(\"Jobs Ingested (Daily)\") * 100"}},
                "Validation Pass Rate": {"formula": {"expression": "(prop(\"Jobs Ingested (Daily)\") - (prop(\"Schema Failures\") + prop(\"Data Quality Failures\") + prop(\"Enrichment Failures\"))) / prop(\"Jobs Ingested (Daily)\") * 100"}},
                "Error Rate": {"formula": {"expression": "(prop(\"Schema Failures\") + prop(\"Data Quality Failures\") + prop(\"Enrichment Failures\")) / prop(\"Jobs Ingested (Daily)\") * 100"}},
                "Enrichment Coverage": {"formula": {"expression": "(prop(\"Jobs with Salary\") + prop(\"Jobs with Skills\") + prop(\"Jobs with Experience\")) / (prop(\"Jobs Ingested (Daily)\") * 3) * 100"}},
                "Health Score": {"formula": {"expression": "((100 - prop(\"Error Rate\")) + prop(\"Validation Pass Rate\") + (prop(\"Enrichment Coverage\") / 100 * 50)) / 2.5"}},
                "SLA Status": {"formula": {"expression": "if(prop(\"Health Score\") >= 95, \" Green\", if(prop(\"Health Score\") >= 85, \"🟡 Yellow\", \" Red\"))"}}
            }
        }
        
        try:
            response = requests.post(
                "https://api.notion.com/v1/databases",
                headers=self.headers,
                json=database_config,
                timeout=30
            )
            
            if response.status_code == 200:
                db_data = response.json()
                self.connector_db_id = db_data["id"]
                logger.info(f" Created Connector Performance database: {self.connector_db_id}")
                return self.connector_db_id
            else:
                logger.error(f" Failed to create database: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f" Error creating database: {e}")
            return None
    
    def create_milestone_database(self) -> str:
        """Create the Epic 2 Milestone Tracker database"""
        milestone_config = {
            "parent": {"type": "page_id", "page_id": os.getenv("NOTION_PARENT_PAGE_ID")},
            "title": [{"type": "text", "text": {"content": "Epic 2 Rollout Tracker"}}],
            "properties": {
                "Milestone": {"title": {}},
                "Epic Phase": {
                    "select": {
                        "options": [
                            {"name": "Phase 1: Foundation", "color": "blue"},
                            {"name": "Phase 2: Connectors", "color": "green"},
                            {"name": "Phase 3: Enrichment", "color": "orange"},
                            {"name": "Phase 4: Governance", "color": "red"},
                            {"name": "Phase 5: Integration", "color": "purple"}
                        ]
                    }
                },
                "Status": {
                    "select": {
                        "options": [
                            {"name": " Not Started", "color": "red"},
                            {"name": "🟡 In Progress", "color": "yellow"},
                            {"name": "🟢 Complete", "color": "green"},
                            {"name": " Blocked", "color": "red"},
                            {"name": "⏸️ Paused", "color": "gray"}
                        ]
                    }
                },
                "Target Date": {"date": {}},
                "Actual Date": {"date": {}},
                "Progress": {"number": {"format": "percent"}},
                "Success Criteria": {"rich_text": {}},
                "KPI Targets": {"rich_text": {}},
                "Responsible Team": {"people": {}},
                "Risk Level": {
                    "select": {
                        "options": [
                            {"name": "🟢 Low", "color": "green"},
                            {"name": "🟡 Medium", "color": "yellow"},
                            {"name": " High", "color": "red"},
                            {"name": "🚨 Critical", "color": "red"}
                        ]
                    }
                },
                "Last Updated": {"last_edited_time": {}}
            }
        }
        
        try:
            response = requests.post(
                "https://api.notion.com/v1/databases",
                headers=self.headers,
                json=milestone_config,
                timeout=30
            )
            
            if response.status_code == 200:
                db_data = response.json()
                self.milestone_db_id = db_data["id"]
                logger.info(f" Created Milestone Tracker database: {self.milestone_db_id}")
                return self.milestone_db_id
            else:
                logger.error(f" Failed to create milestone database: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f" Error creating milestone database: {e}")
            return None
    
    def populate_initial_milestones(self):
        """Populate the milestone database with Epic 2 milestones"""
        milestones = [
            {
                "name": "Schema Foundation Complete",
                "phase": "Phase 1: Foundation",
                "target_date": "2024-02-01",
                "success_criteria": "Canonical schema validated, all tests passing, documentation complete",
                "kpi_targets": "100% schema compliance, all validation tests pass",
                "risk_level": "🟢 Low"
            },
            {
                "name": "LinkedIn Connector Live", 
                "phase": "Phase 2: Connectors",
                "target_date": "2024-02-15",
                "success_criteria": "Production deployment, 24h stable operation, validation passing",
                "kpi_targets": "Validation Pass Rate ≥ 95%, Error Rate ≤ 5%, Jobs Ingested ≥ 1000/day",
                "risk_level": "🟡 Medium"
            },
            {
                "name": "Indeed + ZipRecruiter Live",
                "phase": "Phase 2: Connectors",
                "target_date": "2024-03-01", 
                "success_criteria": "Both connectors stable, deduplication working, no data quality issues",
                "kpi_targets": "Deduplication Rate ≥ 90%, Combined ingestion ≥ 5000/day, Health Score ≥ 90",
                "risk_level": "🟡 Medium"
            },
            {
                "name": "Google Jobs + Bing Jobs Live",
                "phase": "Phase 2: Connectors",
                "target_date": "2024-03-15",
                "success_criteria": "Search engine connectors operational, API compliance verified",
                "kpi_targets": "Error Rate ≤ 5%, API compliance 100%, Rate limit management working",
                "risk_level": " High"
            },
            {
                "name": "Enrichment Pipeline Live",
                "phase": "Phase 3: Enrichment", 
                "target_date": "2024-04-01",
                "success_criteria": "NLP processing, salary parsing, skills extraction all operational",
                "kpi_targets": "Enrichment Coverage ≥ 80%, Intelligence Score avg ≥ 0.7, Pipeline Latency ≤ 30s",
                "risk_level": " High"
            },
            {
                "name": "Validation Framework Live",
                "phase": "Phase 4: Governance",
                "target_date": "2024-04-15", 
                "success_criteria": "Automated validation, error handling, audit trail, compliance reporting",
                "kpi_targets": "Validation Pass Rate ≥ 98%, Zero silent failures, 100% audit coverage",
                "risk_level": "🟡 Medium"
            },
            {
                "name": "Cross-Platform Integration Complete",
                "phase": "Phase 5: Integration",
                "target_date": "2024-05-01",
                "success_criteria": "Notion, Zapier, Slack, GitHub integration working seamlessly",
                "kpi_targets": "100% automation success rate, <5min alert latency, Zero integration failures",
                "risk_level": "🟡 Medium"
            },
            {
                "name": "Epic 2 Production Ready",
                "phase": "Phase 5: Integration",
                "target_date": "2024-05-15",
                "success_criteria": "All connectors live, KPIs met, documentation complete, team trained",
                "kpi_targets": "All milestone KPIs achieved, 7-day stable operation, Executive sign-off",
                "risk_level": "🟢 Low"
            }
        ]
        
        for milestone in milestones:
            self.create_milestone_page(milestone)
    
    def create_milestone_page(self, milestone_data: Dict[str, str]):
        """Create a milestone page in the database"""
        page_config = {
            "parent": {"database_id": self.milestone_db_id},
            "properties": {
                "Milestone": {
                    "title": [{"text": {"content": milestone_data["name"]}}]
                },
                "Epic Phase": {
                    "select": {"name": milestone_data["phase"]}
                },
                "Status": {
                    "select": {"name": " Not Started"}
                },
                "Target Date": {
                    "date": {"start": milestone_data["target_date"]}
                },
                "Progress": {
                    "number": 0
                },
                "Success Criteria": {
                    "rich_text": [{"text": {"content": milestone_data["success_criteria"]}}]
                },
                "KPI Targets": {
                    "rich_text": [{"text": {"content": milestone_data["kpi_targets"]}}]
                },
                "Risk Level": {
                    "select": {"name": milestone_data["risk_level"]}
                }
            }
        }
        
        try:
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=self.headers,
                json=page_config,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f" Created milestone: {milestone_data['name']}")
            else:
                logger.error(f" Failed to create milestone {milestone_data['name']}: {response.status_code}")
                
        except Exception as e:
            logger.error(f" Error creating milestone {milestone_data['name']}: {e}")
    
    def update_connector_metrics(self, metrics: ConnectorMetrics):
        """Update or create connector performance record"""
        derived_metrics = metrics.calculate_derived_metrics()
        
        page_config = {
            "parent": {"database_id": self.connector_db_id},
            "properties": {
                "Connector": {"select": {"name": metrics.connector}},
                "Status": {"select": {"name": "🟢 Live"}},  # Assume live if we're getting metrics
                "Date": {"date": {"start": metrics.date}},
                "Jobs Ingested (Daily)": {"number": metrics.jobs_ingested_daily},
                "Unique Jobs (Daily)": {"number": metrics.unique_jobs_daily},
                "Schema Failures": {"number": metrics.schema_failures},
                "Data Quality Failures": {"number": metrics.data_quality_failures},
                "Enrichment Failures": {"number": metrics.enrichment_failures},
                "Avg Intelligence Score": {"number": metrics.avg_intelligence_score},
                "Jobs with Salary": {"number": metrics.jobs_with_salary},
                "Jobs with Skills": {"number": metrics.jobs_with_skills},
                "Jobs with Experience": {"number": metrics.jobs_with_experience},
                "Pipeline Latency (Avg)": {"number": metrics.pipeline_latency_avg},
                "Pipeline Latency (P95)": {"number": metrics.pipeline_latency_p95},
                "API Response Time": {"number": metrics.api_response_time},
                "Rate Limit Hits": {"number": metrics.rate_limit_hits},
                "Last Sync": {"date": {"start": metrics.last_sync}},
                "Notes": {"rich_text": [{"text": {"content": f"Health Score: {derived_metrics['health_score']}, SLA: {' Green' if derived_metrics['health_score'] >= 95 else '🟡 Yellow' if derived_metrics['health_score'] >= 85 else ' Red'}"}}]}
            }
        }
        
        try:
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=self.headers,
                json=page_config,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f" Updated metrics for {metrics.connector} on {metrics.date}")
                return True
            else:
                logger.error(f" Failed to update metrics for {metrics.connector}: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f" Error updating metrics for {metrics.connector}: {e}")
            return False


class KPIDataCollector:
    """Collects KPI data from various sources"""
    
    def __init__(self):
        self.connectors = ["linkedin", "indeed", "ziprecruiter", "google_jobs", "bing_jobs"]
        self.notion_dashboard = NotionKPIDashboard(os.getenv("NOTION_API_TOKEN"))
        
        # Resume processing metrics
        self.resume_metrics = {
            "files_processed_daily": 0,
            "parsing_success_rate": 0.0,
            "avg_parsing_confidence": 0.0,
            "contact_extraction_rate": 0.0,
            "skills_extraction_rate": 0.0,
            "experience_extraction_rate": 0.0,
            "schema_validation_failures": 0,
            "avg_processing_time": 0.0
        }
        
    def collect_connector_metrics(self, connector: str, date: str) -> ConnectorMetrics:
        """Collect metrics for a specific connector (mock implementation)"""
        # In production, this would integrate with your actual data sources:
        # - Query your job database for daily counts
        # - Get validation results from your pipeline
        # - Collect performance metrics from monitoring systems
        
        # Mock data for demonstration
        import random
        
        base_jobs = {"linkedin": 1500, "indeed": 3000, "ziprecruiter": 2000, "google_jobs": 1000, "bing_jobs": 800}
        
        jobs_ingested = base_jobs.get(connector, 1000) + random.randint(-200, 300)
        unique_jobs = int(jobs_ingested * (0.85 + random.random() * 0.1))  # 85-95% unique
        
        return ConnectorMetrics(
            connector=connector,
            date=date,
            jobs_ingested_daily=jobs_ingested,
            unique_jobs_daily=unique_jobs,
            schema_failures=random.randint(5, 25),
            data_quality_failures=random.randint(3, 15),
            enrichment_failures=random.randint(8, 30),
            avg_intelligence_score=0.65 + random.random() * 0.25,  # 0.65-0.90
            jobs_with_salary=int(jobs_ingested * (0.70 + random.random() * 0.20)),  # 70-90%
            jobs_with_skills=int(jobs_ingested * (0.80 + random.random() * 0.15)),  # 80-95%
            jobs_with_experience=int(jobs_ingested * (0.75 + random.random() * 0.20)),  # 75-95%
            pipeline_latency_avg=15 + random.random() * 20,  # 15-35 seconds
            pipeline_latency_p95=30 + random.random() * 40,  # 30-70 seconds
            api_response_time=100 + random.random() * 200,  # 100-300ms
            rate_limit_hits=random.randint(0, 5),
            last_sync=datetime.now().isoformat() + "Z"
        )
    
    def collect_all_metrics(self, date: str = None) -> List[ConnectorMetrics]:
        """Collect metrics for all connectors"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Collect connector metrics
        all_metrics = []
        for connector in self.connectors:
            metrics = self.collect_connector_metrics(connector, date)
            all_metrics.append(metrics)
            logger.info(f" Collected metrics for {connector}: {metrics.jobs_ingested_daily} jobs, {metrics.calculate_derived_metrics()['health_score']:.1f} health score")
        
        # Collect resume processing metrics
        self.collect_resume_processing_metrics(date)
        
        return all_metrics
    
    def collect_resume_processing_metrics(self, date: str):
        """Collect resume file processing metrics"""
        # In production, this would query your resume processing system
        # Mock data for demonstration
        import random
        
        self.resume_metrics = {
            "files_processed_daily": random.randint(50, 200),
            "parsing_success_rate": 85.0 + random.random() * 10,  # 85-95%
            "avg_parsing_confidence": 0.70 + random.random() * 0.20,  # 0.7-0.9
            "contact_extraction_rate": 90.0 + random.random() * 8,  # 90-98%
            "skills_extraction_rate": 75.0 + random.random() * 20,  # 75-95%
            "experience_extraction_rate": 80.0 + random.random() * 15,  # 80-95%
            "schema_validation_failures": random.randint(0, 10),
            "avg_processing_time": 2.0 + random.random() * 3.0  # 2-5 seconds
        }
        
        logger.info(f"📄 Resume processing metrics: {self.resume_metrics['files_processed_daily']} files, {self.resume_metrics['parsing_success_rate']:.1f}% success rate")
    
    def push_metrics_to_dashboard(self, metrics_list: List[ConnectorMetrics]):
        """Push all metrics to Notion dashboard"""
        for metrics in metrics_list:
            success = self.notion_dashboard.update_connector_metrics(metrics)
            if success:
                logger.info(f" Pushed {metrics.connector} metrics to dashboard")
            else:
                logger.error(f" Failed to push {metrics.connector} metrics")


def setup_kpi_dashboard():
    """Complete KPI dashboard setup"""
    logger.info(" Starting CareerCoach KPI Dashboard Setup")
    
    # Validate environment variables
    required_vars = ["NOTION_API_TOKEN", "NOTION_PARENT_PAGE_ID"]
    for var in required_vars:
        if not os.getenv(var):
            logger.error(f" Missing required environment variable: {var}")
            return False
    
    # Create Notion dashboard
    dashboard = NotionKPIDashboard(os.getenv("NOTION_API_TOKEN"))
    
    # Create databases
    logger.info(" Creating Notion databases...")
    connector_db = dashboard.create_connector_performance_database()
    milestone_db = dashboard.create_milestone_database()
    
    if not connector_db or not milestone_db:
        logger.error(" Failed to create required databases")
        return False
    
    # Populate initial milestones
    logger.info(" Populating Epic 2 milestones...")
    dashboard.populate_initial_milestones()
    
    # Collect and push initial metrics
    logger.info(" Collecting initial connector metrics...")
    collector = KPIDataCollector()
    collector.notion_dashboard.connector_db_id = connector_db
    collector.notion_dashboard.milestone_db_id = milestone_db
    
    # Generate sample data for the last 7 days
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        metrics_list = collector.collect_all_metrics(date)
        collector.push_metrics_to_dashboard(metrics_list)
    
    logger.info(" KPI Dashboard setup complete!")
    logger.info(f" Connector Performance Database: https://notion.so/{connector_db.replace('-', '')}")
    logger.info(f" Epic 2 Milestone Tracker: https://notion.so/{milestone_db.replace('-', '')}")
    
    return True


def daily_kpi_collection():
    """Daily KPI collection routine (for cron/scheduled execution)"""
    logger.info(" Starting daily KPI collection")
    
    collector = KPIDataCollector()
    
    # Set database IDs from environment variables
    collector.notion_dashboard.connector_db_id = os.getenv("NOTION_CONNECTOR_DB_ID")
    collector.notion_dashboard.milestone_db_id = os.getenv("NOTION_MILESTONE_DB_ID")
    
    if not collector.notion_dashboard.connector_db_id:
        logger.error(" NOTION_CONNECTOR_DB_ID not set")
        return False
    
    # Collect today's metrics
    today = datetime.now().strftime("%Y-%m-%d")
    metrics_list = collector.collect_all_metrics(today)
    
    # Push to dashboard
    collector.push_metrics_to_dashboard(metrics_list)
    
    # Check for alerts
    check_kpi_alerts(metrics_list)
    
    logger.info(" Daily KPI collection complete")
    return True


def check_kpi_alerts(metrics_list: List[ConnectorMetrics]):
    """Check for KPI threshold violations and send alerts"""
    alerts = []
    
    for metrics in metrics_list:
        derived = metrics.calculate_derived_metrics()
        
        # Check critical thresholds
        if derived["error_rate"] > 10:
            alerts.append(f"🚨 {metrics.connector}: Error rate {derived['error_rate']:.1f}% > 10%")
        
        if derived["validation_pass_rate"] < 90:
            alerts.append(f" {metrics.connector}: Validation pass rate {derived['validation_pass_rate']:.1f}% < 90%")
        
        if derived["health_score"] < 75:
            alerts.append(f" {metrics.connector}: Health score {derived['health_score']:.1f} < 75")
        
        if metrics.pipeline_latency_avg > 60:
            alerts.append(f" {metrics.connector}: Pipeline latency {metrics.pipeline_latency_avg:.1f}s > 60s")
    
    # Send alerts if any found
    if alerts:
        send_slack_alert("\n".join(alerts))
        logger.warning(f"🚨 {len(alerts)} KPI alerts triggered")
    else:
        logger.info(" All KPIs within normal thresholds")


def send_slack_alert(message: str):
    """Send alert to Slack webhook"""
    slack_webhook = os.getenv("SLACK_ALERTS_WEBHOOK")
    if not slack_webhook:
        logger.warning(" SLACK_ALERTS_WEBHOOK not configured, skipping alert")
        return
    
    payload = {
        "text": "🚨 CareerCoach KPI Alert",
        "attachments": [
            {
                "color": "danger",
                "title": "KPI Threshold Violations",
                "text": message,
                "footer": "CareerCoach KPI Dashboard",
                "ts": int(datetime.now().timestamp())
            }
        ]
    }
    
    try:
        response = requests.post(slack_webhook, json=payload, timeout=10)
        if response.status_code == 200:
            logger.info(" Slack alert sent successfully")
        else:
            logger.error(f" Failed to send Slack alert: {response.status_code}")
    except Exception as e:
        logger.error(f" Error sending Slack alert: {e}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CareerCoach KPI Dashboard Management")
    parser.add_argument("--setup", action="store_true", help="Set up initial KPI dashboard")
    parser.add_argument("--collect", action="store_true", help="Run daily KPI collection")
    parser.add_argument("--test", action="store_true", help="Test KPI collection without pushing to Notion")
    
    args = parser.parse_args()
    
    if args.setup:
        success = setup_kpi_dashboard()
        exit(0 if success else 1)
    elif args.collect:
        success = daily_kpi_collection()
        exit(0 if success else 1)
    elif args.test:
        collector = KPIDataCollector()
        metrics = collector.collect_all_metrics()
        for m in metrics:
            derived = m.calculate_derived_metrics()
            print(f" {m.connector}: {m.jobs_ingested_daily} jobs, {derived['health_score']:.1f} health")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()