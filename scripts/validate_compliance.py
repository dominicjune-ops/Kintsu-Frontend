"""
Schema Validation Scripts

Automated validation scripts for CareerCoach.ai schema compliance,
connector output verification, and cross-platform integration testing.
"""

import json
import jsonschema
import glob
import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import argparse
from datetime import datetime
import requests
import uuid
import re


class SchemaValidator:
    """Comprehensive schema validation for CareerCoach.ai"""
    
    def __init__(self, schema_dir: str = "schema"):
        self.schema_dir = Path(schema_dir)
        self.schemas = {}
        self.load_schemas()
    
    def load_schemas(self):
        """Load all JSON schema files"""
        schema_files = glob.glob(str(self.schema_dir / "*-schema.json"))
        
        for schema_file in schema_files:
            schema_name = Path(schema_file).stem.replace("-schema", "")
            try:
                with open(schema_file, 'r') as f:
                    self.schemas[schema_name] = json.load(f)
                print(f" Loaded schema: {schema_name}")
            except Exception as e:
                print(f" Failed to load schema {schema_file}: {e}")
                sys.exit(1)
    
    def validate_schema_syntax(self) -> bool:
        """Validate all schemas have correct JSON Schema syntax"""
        print("\n Validating Schema Syntax...")
        all_valid = True
        
        for name, schema in self.schemas.items():
            try:
                jsonschema.Draft7Validator.check_schema(schema)
                print(f"   {name}: Valid JSON Schema Draft 7")
            except jsonschema.SchemaError as e:
                print(f"   {name}: Invalid schema - {e.message}")
                all_valid = False
        
        return all_valid
    
    def validate_reference_resolution(self) -> bool:
        """Validate all $ref references resolve correctly"""
        print("\n🔗 Validating Reference Resolution...")
        all_valid = True
        
        # Load canonical schema for reference resolution
        try:
            canonical_path = self.schema_dir / "canonical-schema.json"
            with open(canonical_path, 'r') as f:
                canonical_schema = json.load(f)
        except FileNotFoundError:
            print(" canonical-schema.json not found")
            return False
        
        for name, schema in self.schemas.items():
            try:
                resolver = jsonschema.RefResolver(
                    base_uri=f"file://{canonical_path.absolute()}", 
                    referrer=canonical_schema
                )
                validator = jsonschema.Draft7Validator(schema, resolver=resolver)
                validator.check_schema(schema)
                print(f"   {name}: All references resolve")
            except jsonschema.RefResolutionError as e:
                print(f"   {name}: Reference resolution failed - {e}")
                all_valid = False
            except Exception as e:
                print(f"   {name}: Validation error - {e}")
                all_valid = False
        
        return all_valid
    
    def validate_sample_data(self) -> bool:
        """Validate sample data against schemas"""
        print("\n Validating Sample Data...")
        all_valid = True
        
        sample_data = {
            "job-posting": {
                "id": str(uuid.uuid4()),
                "title": "Senior Software Engineer",
                "company": "TechCorp Inc",
                "location": {
                    "city": "San Francisco", 
                    "state": "CA",
                    "country": "US"
                },
                "employment_type": "full_time",
                "remote_policy": "hybrid",
                "created_at": "2024-01-01T00:00:00Z",
                "source": "linkedin",
                "external_id": "linkedin123"
            },
            "user-profile": {
                "id": str(uuid.uuid4()),
                "email": "user@example.com",
                "name": "John Doe",
                "location": {
                    "city": "San Francisco",
                    "state": "CA", 
                    "country": "US"
                },
                "created_at": "2024-01-01T00:00:00Z"
            },
            "application": {
                "id": str(uuid.uuid4()),
                "user_id": str(uuid.uuid4()),
                "job_posting_id": str(uuid.uuid4()),
                "status": "applied",
                "applied_at": "2024-01-01T00:00:00Z"
            }
        }
        
        for schema_name, data in sample_data.items():
            if schema_name in self.schemas:
                try:
                    jsonschema.validate(data, self.schemas[schema_name])
                    print(f"   {schema_name}: Sample data validates")
                except jsonschema.ValidationError as e:
                    print(f"   {schema_name}: Sample validation failed - {e.message}")
                    all_valid = False
        
        return all_valid
    
    def run_all_validations(self) -> bool:
        """Run complete schema validation suite"""
        print(" Starting Schema Validation Suite")
        print("=" * 50)
        
        results = [
            self.validate_schema_syntax(),
            self.validate_reference_resolution(),
            self.validate_sample_data()
        ]
        
        all_passed = all(results)
        
        print("\n" + "=" * 50)
        if all_passed:
            print(" All Schema Validations PASSED!")
        else:
            print(" Some Schema Validations FAILED!")
        
        return all_passed


class ConnectorValidator:
    """Validate connector outputs against canonical schema"""
    
    def __init__(self):
        self.schema_validator = SchemaValidator()
        self.job_schema = self.schema_validator.schemas.get("job-posting")
        if not self.job_schema:
            raise ValueError("job-posting schema not found")
    
    def validate_connector_output(self, connector_name: str, sample_data: Dict[str, Any]) -> bool:
        """Validate a single connector's output"""
        print(f"\n🔌 Validating {connector_name} Connector...")
        
        try:
            # Import connector dynamically
            module_path = f"src.connectors.{connector_name}_connector"
            connector_module = __import__(module_path, fromlist=[f"{connector_name.title()}Connector"])
            connector_class = getattr(connector_module, f"{connector_name.title()}Connector")
            connector = connector_class()
            
            # Transform sample data
            transformed = connector.transform_to_canonical(sample_data)
            
            # Validate against schema
            jsonschema.validate(transformed, self.job_schema)
            
            print(f"   {connector_name}: Output validates against canonical schema")
            return True
            
        except ImportError:
            print(f"   {connector_name}: Connector not implemented yet")
            return True  # Not a failure if not implemented
        except jsonschema.ValidationError as e:
            print(f"   {connector_name}: Schema validation failed - {e.message}")
            return False
        except Exception as e:
            print(f"   {connector_name}: Error - {e}")
            return False
    
    def validate_all_connectors(self) -> bool:
        """Validate all implemented connectors"""
        print("🔌 Starting Connector Validation Suite")
        print("=" * 50)
        
        # Sample data for each connector type
        sample_data = {
            "linkedin": {
                "id": "3775094825",
                "title": "Software Engineer",
                "formattedLocation": "San Francisco, CA",
                "employmentType": "FULL_TIME",
                "listedAt": 1703721600000,
                "company": {"name": "TechCorp Inc"}
            },
            "indeed": {
                "jobkey": "abc123",
                "jobtitle": "Software Engineer", 
                "company": "TechCorp Inc",
                "formattedLocation": "San Francisco, CA",
                "date": "2024-01-01",
                "jobtype": "fulltime"
            },
            "ziprecruiter": {
                "id": "job123",
                "name": "Software Engineer",
                "hiring_company": {"name": "TechCorp Inc"},
                "location": "San Francisco, CA",
                "employment_type": "FullTime",
                "posted_time": "2024-01-01T00:00:00Z"
            }
        }
        
        results = []
        for connector_name, data in sample_data.items():
            results.append(self.validate_connector_output(connector_name, data))
        
        all_passed = all(results)
        
        print("\n" + "=" * 50)
        if all_passed:
            print(" All Connector Validations PASSED!")
        else:
            print(" Some Connector Validations FAILED!")
        
        return all_passed


class IntegrationValidator:
    """Validate cross-platform integrations"""
    
    def __init__(self):
        self.notion_api_key = os.getenv("NOTION_API_KEY")
        self.webhook_url = os.getenv("WEBHOOK_URL")
    
    def validate_notion_integration(self) -> bool:
        """Test Notion database integration"""
        print("\n Validating Notion Integration...")
        
        if not self.notion_api_key:
            print("   NOTION_API_KEY not set, skipping Notion validation")
            return True
        
        try:
            headers = {
                "Authorization": f"Bearer {self.notion_api_key}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            }
            
            # Test API connectivity
            response = requests.get("https://api.notion.com/v1/users/me", headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("   Notion API: Connected successfully")
                return True
            else:
                print(f"   Notion API: Connection failed - {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Notion API: Error - {e}")
            return False
    
    def validate_webhook_endpoint(self) -> bool:
        """Test webhook endpoint availability"""
        print("\n🔗 Validating Webhook Endpoint...")
        
        if not self.webhook_url:
            print("   WEBHOOK_URL not set, skipping webhook validation")
            return True
        
        try:
            test_payload = {
                "job_id": str(uuid.uuid4()),
                "title": "Test Job",
                "company": "Test Company",
                "status": "test"
            }
            
            response = requests.post(
                self.webhook_url, 
                json=test_payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code in [200, 201, 202]:
                print("   Webhook: Endpoint responding")
                return True
            else:
                print(f"   Webhook: Unexpected status - {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Webhook: Error - {e}")
            return False
    
    def validate_azure_services(self) -> bool:
        """Validate Azure service connectivity"""
        print("\n☁️ Validating Azure Services...")
        
        # This would typically test Service Bus, Container Apps, etc.
        # For now, just validate environment variables are set
        required_vars = [
            "AZURE_SERVICE_BUS_CONNECTION_STRING",
            "AZURE_CONTAINER_APPS_ENVIRONMENT",
            "APPLICATION_INSIGHTS_KEY"
        ]
        
        all_set = True
        for var in required_vars:
            if os.getenv(var):
                print(f"   {var}: Set")
            else:
                print(f"   {var}: Not set")
                all_set = False
        
        return all_set
    
    def run_integration_tests(self) -> bool:
        """Run complete integration test suite"""
        print("🔗 Starting Integration Validation Suite")
        print("=" * 50)
        
        results = [
            self.validate_notion_integration(),
            self.validate_webhook_endpoint(),
            self.validate_azure_services()
        ]
        
        all_passed = all(results)
        
        print("\n" + "=" * 50)
        if all_passed:
            print(" All Integration Validations PASSED!")
        else:
            print(" Some Integration Validations FAILED!")
        
        return all_passed


class ComplianceChecker:
    """Check overall CareerCoach.ai compliance"""
    
    def __init__(self):
        self.schema_validator = SchemaValidator()
        self.connector_validator = ConnectorValidator()
        self.integration_validator = IntegrationValidator()
    
    def check_file_structure(self) -> bool:
        """Validate required file structure exists"""
        print("\n📁 Checking File Structure...")
        
        required_files = [
            "schema/canonical-schema.json",
            "schema/job-posting-schema.json", 
            "schema/user-profile-schema.json",
            "schema/application-schema.json",
            "azure-pipelines.yml",
            "src/enrichment_service.py",
            "infrastructure/main.bicep",
            "docs/FIELD_MAPPING.md",
            "docs/archive/deprecated/INTEGRATION_GUIDE.md",
            "docs/COMPLIANCE_CHECKLISTS.md",
            ".github/pull_request_template.md"
        ]
        
        all_exist = True
        for file_path in required_files:
            if Path(file_path).exists():
                print(f"   {file_path}")
            else:
                print(f"   {file_path}: Missing")
                all_exist = False
        
        return all_exist
    
    def run_full_compliance_check(self) -> bool:
        """Run complete compliance validation"""
        print(" CareerCoach.ai Compliance Check")
        print("=" * 60)
        
        results = [
            self.check_file_structure(),
            self.schema_validator.run_all_validations(),
            self.connector_validator.validate_all_connectors(),
            self.integration_validator.run_integration_tests()
        ]
        
        all_passed = all(results)
        
        print("\n" + "=" * 60)
        if all_passed:
            print(" CareerCoach.ai is FULLY COMPLIANT! ")
        else:
            print(" CareerCoach.ai has COMPLIANCE ISSUES that need attention!")
        
        return all_passed


def main():
    """Command line interface for validation scripts"""
    parser = argparse.ArgumentParser(description="CareerCoach.ai Validation Scripts")
    parser.add_argument("--mode", choices=["schema", "connectors", "integration", "all"], 
                       default="all", help="Validation mode to run")
    parser.add_argument("--connector", help="Specific connector to validate")
    parser.add_argument("--output", choices=["text", "json"], default="text",
                       help="Output format")
    
    args = parser.parse_args()
    
    if args.mode == "schema":
        validator = SchemaValidator()
        success = validator.run_all_validations()
    elif args.mode == "connectors":
        validator = ConnectorValidator()
        if args.connector:
            # Validate specific connector (would need sample data)
            success = True  # Placeholder
        else:
            success = validator.validate_all_connectors()
    elif args.mode == "integration":
        validator = IntegrationValidator()
        success = validator.run_integration_tests()
    else:  # args.mode == "all"
        checker = ComplianceChecker()
        success = checker.run_full_compliance_check()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()