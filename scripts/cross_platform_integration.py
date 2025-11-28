"""
Cross-Platform Validation Integration

This script integrates canonical validation across DevOps, Notion, Zapier, 
GitHub, MS Project, and VS Code to ensure governance compliance everywhere.
"""

import json
import os
import requests
from typing import Dict, Any, List
from datetime import datetime
import subprocess
import sys
from pathlib import Path


class CrossPlatformValidator:
    """Integrates canonical validation across entire CareerCoach.ai stack"""
    
    def __init__(self):
        self.notion_token = os.getenv("NOTION_API_TOKEN")
        self.notion_db_id = os.getenv("NOTION_VALIDATION_DB_ID")
        self.zapier_webhook = os.getenv("ZAPIER_VALIDATION_WEBHOOK")
        self.slack_webhook = os.getenv("SLACK_ALERTS_WEBHOOK")
        
    def update_azure_pipeline_status(self, validation_results: Dict[str, Any]) -> bool:
        """Update Azure DevOps pipeline with validation status"""
        try:
            # Set Azure DevOps variable for pipeline decision
            status = validation_results["overall_status"]
            
            if os.getenv("AZURE_DEVOPS_CLI_PAT"):
                cmd = [
                    "az", "pipelines", "variable", "set",
                    "--name", "ValidationStatus", 
                    "--value", status,
                    "--org", os.getenv("AZURE_DEVOPS_ORG"),
                    "--project", os.getenv("AZURE_DEVOPS_PROJECT")
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(" Azure Pipeline: Validation status updated")
                    return True
                else:
                    print(f" Azure Pipeline: Failed to update status - {result.stderr}")
                    return False
            else:
                print(" Azure Pipeline: AZURE_DEVOPS_CLI_PAT not configured")
                return True
                
        except Exception as e:
            print(f" Azure Pipeline: Error updating status - {e}")
            return False
    
    def update_notion_validation_record(self, validation_results: Dict[str, Any]) -> bool:
        """Update Notion database with validation status"""
        if not self.notion_token or not self.notion_db_id:
            print(" Notion: API credentials not configured")
            return True
        
        try:
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
            
            # Create validation record in Notion
            page_data = {
                "parent": {"database_id": self.notion_db_id},
                "properties": {
                    "Job ID": {
                        "title": [{"text": {"content": validation_results["job_id"]}}]
                    },
                    "Validation Status": {
                        "select": {"name": " COMPLIANT" if validation_results["overall_status"] == "PASS" else " NON-COMPLIANT"}
                    },
                    "Timestamp": {
                        "date": {"start": validation_results["timestamp"]}
                    },
                    "Schema Compliance": {
                        "checkbox": validation_results["validation_results"]["schema_compliance"]["status"] == "PASS"
                    },
                    "Data Quality": {
                        "checkbox": validation_results["validation_results"]["data_quality"]["status"] == "PASS"
                    },
                    "Enrichment Pipeline": {
                        "checkbox": validation_results["validation_results"]["enrichment_pipeline"]["status"] == "PASS"
                    },
                    "Governance & Audit": {
                        "checkbox": validation_results["validation_results"]["governance_audit"]["status"] == "PASS"
                    }
                }
            }
            
            # Add connector-specific status if present
            if "connector_specific" in validation_results["validation_results"]:
                connector_result = validation_results["validation_results"]["connector_specific"]
                page_data["properties"]["Connector"] = {
                    "select": {"name": connector_result["connector"].title()}
                }
                page_data["properties"]["Connector Validation"] = {
                    "checkbox": connector_result["status"] == "PASS"
                }
            
            response = requests.post(
                "https://api.notion.com/v1/pages", 
                headers=headers, 
                json=page_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print(" Notion: Validation record created")
                return True
            else:
                print(f" Notion: Failed to create record - {response.status_code} {response.text}")
                return False
                
        except Exception as e:
            print(f" Notion: Error creating validation record - {e}")
            return False
    
    def trigger_zapier_workflow(self, validation_results: Dict[str, Any]) -> bool:
        """Trigger Zapier automation based on validation results"""
        if not self.zapier_webhook:
            print(" Zapier: Webhook URL not configured")
            return True
        
        try:
            # Determine workflow path based on validation status
            workflow_path = "success" if validation_results["overall_status"] == "PASS" else "quarantine"
            
            webhook_data = {
                "job_id": validation_results["job_id"],
                "validation_status": validation_results["overall_status"],
                "workflow_path": workflow_path,
                "timestamp": validation_results["timestamp"],
                "validation_summary": {
                    category: details["status"] 
                    for category, details in validation_results["validation_results"].items()
                },
                "error_count": sum(
                    len(details["errors"]) 
                    for details in validation_results["validation_results"].values()
                )
            }
            
            response = requests.post(
                self.zapier_webhook, 
                json=webhook_data,
                timeout=10
            )
            
            if response.status_code in [200, 201, 202]:
                print(f" Zapier: Workflow triggered ({workflow_path} path)")
                return True
            else:
                print(f" Zapier: Failed to trigger workflow - {response.status_code}")
                return False
                
        except Exception as e:
            print(f" Zapier: Error triggering workflow - {e}")
            return False
    
    def send_slack_alert(self, validation_results: Dict[str, Any]) -> bool:
        """Send Slack alert for validation failures"""
        if not self.slack_webhook:
            print(" Slack: Webhook URL not configured")
            return True
        
        # Only send alerts for failures
        if validation_results["overall_status"] == "PASS":
            return True
        
        try:
            # Collect all errors
            all_errors = []
            for category, details in validation_results["validation_results"].items():
                if details["errors"]:
                    category_name = category.replace("_", " ").title()
                    all_errors.extend([f"**{category_name}**: {error}" for error in details["errors"]])
            
            slack_message = {
                "text": "🚨 CareerCoach.ai Validation Failure",
                "attachments": [
                    {
                        "color": "danger",
                        "title": f"Job Validation Failed: {validation_results['job_id']}",
                        "fields": [
                            {
                                "title": "Timestamp", 
                                "value": validation_results["timestamp"],
                                "short": True
                            },
                            {
                                "title": "Status",
                                "value": " NON-COMPLIANT", 
                                "short": True
                            },
                            {
                                "title": "Errors",
                                "value": "\n".join(all_errors[:10])  # Limit to first 10 errors
                            }
                        ],
                        "actions": [
                            {
                                "type": "button",
                                "text": "View in Notion",
                                "url": f"https://notion.so/{self.notion_db_id.replace('-', '')}"
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                self.slack_webhook,
                json=slack_message,
                timeout=10
            )
            
            if response.status_code == 200:
                print(" Slack: Alert sent to dev team")
                return True
            else:
                print(f" Slack: Failed to send alert - {response.status_code}")
                return False
                
        except Exception as e:
            print(f" Slack: Error sending alert - {e}")
            return False
    
    def update_github_status(self, validation_results: Dict[str, Any], commit_sha: str = None) -> bool:
        """Update GitHub commit status with validation results"""
        github_token = os.getenv("GITHUB_TOKEN")
        github_repo = os.getenv("GITHUB_REPOSITORY")  # format: owner/repo
        
        if not github_token or not github_repo or not commit_sha:
            print(" GitHub: Missing credentials or commit SHA")
            return True
        
        try:
            headers = {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            status_data = {
                "state": "success" if validation_results["overall_status"] == "PASS" else "failure",
                "target_url": f"https://notion.so/{self.notion_db_id.replace('-', '')}",
                "description": f"Canonical validation: {validation_results['overall_status']}",
                "context": "careercoach/canonical-validation"
            }
            
            response = requests.post(
                f"https://api.github.com/repos/{github_repo}/statuses/{commit_sha}",
                headers=headers,
                json=status_data,
                timeout=10
            )
            
            if response.status_code == 201:
                print(" GitHub: Commit status updated")
                return True
            else:
                print(f" GitHub: Failed to update status - {response.status_code}")
                return False
                
        except Exception as e:
            print(f" GitHub: Error updating status - {e}")
            return False
    
    def update_vscode_settings(self, validation_results: Dict[str, Any]) -> bool:
        """Update VS Code workspace settings with validation status"""
        try:
            vscode_settings_path = Path(".vscode/settings.json")
            
            # Load existing settings or create new
            if vscode_settings_path.exists():
                with open(vscode_settings_path, 'r') as f:
                    settings = json.load(f)
            else:
                settings = {}
            
            # Update validation status in settings
            settings["careercoach.lastValidation"] = {
                "timestamp": validation_results["timestamp"],
                "status": validation_results["overall_status"],
                "jobId": validation_results["job_id"]
            }
            
            # Add schema validation settings if not present
            if "json.schemas" not in settings:
                settings["json.schemas"] = []
            
            # Ensure our canonical schema is associated
            canonical_schema_mapping = {
                "fileMatch": ["**/job-data/*.json", "**/canonical-jobs/*.json"],
                "url": "./schema/canonical-schema.json"
            }
            
            if canonical_schema_mapping not in settings["json.schemas"]:
                settings["json.schemas"].append(canonical_schema_mapping)
            
            # Create .vscode directory if it doesn't exist
            vscode_settings_path.parent.mkdir(exist_ok=True)
            
            # Write updated settings
            with open(vscode_settings_path, 'w') as f:
                json.dump(settings, f, indent=2)
            
            print(" VS Code: Workspace settings updated with validation status")
            return True
            
        except Exception as e:
            print(f" VS Code: Error updating settings - {e}")
            return False
    
    def run_cross_platform_integration(self, validation_results: Dict[str, Any], commit_sha: str = None) -> Dict[str, bool]:
        """Run validation integration across all platforms"""
        print(f"\n{'='*60}")
        print("⚙️ CROSS-PLATFORM VALIDATION INTEGRATION")
        print(f"{'='*60}")
        
        integration_results = {}
        
        # Azure DevOps Pipeline
        integration_results["azure_pipeline"] = self.update_azure_pipeline_status(validation_results)
        
        # Notion Database  
        integration_results["notion"] = self.update_notion_validation_record(validation_results)
        
        # Zapier Automation
        integration_results["zapier"] = self.trigger_zapier_workflow(validation_results)
        
        # Slack Alerts (only for failures)
        integration_results["slack"] = self.send_slack_alert(validation_results)
        
        # GitHub Status
        integration_results["github"] = self.update_github_status(validation_results, commit_sha)
        
        # VS Code Settings
        integration_results["vscode"] = self.update_vscode_settings(validation_results)
        
        # Summary
        successful_integrations = sum(integration_results.values())
        total_integrations = len(integration_results)
        
        print(f"\n Integration Summary: {successful_integrations}/{total_integrations} platforms updated successfully")
        
        if successful_integrations == total_integrations:
            print(" All platform integrations completed successfully!")
        else:
            print(" Some platform integrations failed - check configuration")
        
        return integration_results


def main():
    """Command line interface for cross-platform validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cross-Platform Validation Integration")
    parser.add_argument("--validation-results", required=True, 
                       help="JSON file with validation results")
    parser.add_argument("--commit-sha", help="Git commit SHA for GitHub status")
    parser.add_argument("--platform", choices=["azure", "notion", "zapier", "slack", "github", "vscode"],
                       help="Run integration for specific platform only")
    
    args = parser.parse_args()
    
    # Load validation results
    try:
        with open(args.validation_results, 'r') as f:
            validation_results = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f" Error loading validation results: {e}")
        sys.exit(1)
    
    # Run integrations
    integrator = CrossPlatformValidator()
    
    if args.platform:
        # Run single platform integration
        method_map = {
            "azure": integrator.update_azure_pipeline_status,
            "notion": integrator.update_notion_validation_record,
            "zapier": integrator.trigger_zapier_workflow,
            "slack": integrator.send_slack_alert,
            "github": lambda vr: integrator.update_github_status(vr, args.commit_sha),
            "vscode": integrator.update_vscode_settings
        }
        
        success = method_map[args.platform](validation_results)
        sys.exit(0 if success else 1)
    else:
        # Run all integrations
        results = integrator.run_cross_platform_integration(validation_results, args.commit_sha)
        sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()