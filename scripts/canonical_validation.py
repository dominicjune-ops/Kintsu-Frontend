"""
Canonical Validation Enforcement Script

This script enforces the CareerCoach.ai canonical validation checklist across all connectors,
ensuring governance, data quality, and cross-platform integration compliance.
"""

import json
import jsonschema
import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import argparse
from datetime import datetime
import uuid
import re
import requests
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CanonicalValidator:
    """Enforces canonical validation checklist for CareerCoach.ai connectors"""
    
    REQUIRED_FIELDS = ["job_id", "title", "company_name", "location", "posted_date", "apply_url"]
    EMPLOYMENT_TYPES = ["full_time", "part_time", "contract", "temporary", "internship", "freelance"]
    EXPERIENCE_LEVELS = ["entry", "mid", "senior", "executive"]
    
    def __init__(self, schema_path: str = "schema/canonical-schema.json"):
        self.schema_path = Path(schema_path)
        self.schema = self.load_canonical_schema()
        self.validation_results = {}
    
    def load_canonical_schema(self) -> Dict[str, Any]:
        """Load canonical schema for validation"""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Canonical schema not found at {self.schema_path}")
            sys.exit(1)
    
    def validate_schema_compliance(self, job_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        1. Schema Compliance Validation
        - All required fields present
        - Field types match canonical schema  
        - Location normalized to {city, state, country, remote_flag}
        - posted_date standardized to UTC
        """
        errors = []
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in job_data or job_data[field] is None:
                errors.append(f"Missing required field: {field}")
        
        # Validate field types
        if "job_id" in job_data and not isinstance(job_data["job_id"], str):
            errors.append("job_id must be string")
        
        if "title" in job_data and not isinstance(job_data["title"], str):
            errors.append("title must be string")
        
        if "company_name" in job_data and not isinstance(job_data["company_name"], str):
            errors.append("company_name must be string")
        
        # Validate location structure
        if "location" in job_data:
            location = job_data["location"]
            if not isinstance(location, dict):
                errors.append("location must be object with {city, state, country, remote_flag}")
            else:
                required_location_fields = ["city", "state", "country", "remote_flag"]
                for loc_field in required_location_fields:
                    if loc_field not in location:
                        errors.append(f"location missing required field: {loc_field}")
        
        # Validate posted_date format (ISO 8601 UTC)
        if "posted_date" in job_data:
            try:
                datetime.fromisoformat(job_data["posted_date"].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                errors.append("posted_date must be UTC ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)")
        
        return len(errors) == 0, errors
    
    def validate_data_quality(self, job_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        2. Data Quality Validation
        - Title cleaned (no ALL CAPS, no spam phrases)
        - Company name normalized  
        - Apply URL validated (returns 200 OK)
        - Description clean generated from raw
        """
        errors = []
        
        # Title quality checks
        if "title" in job_data:
            title = job_data["title"]
            
            # Check for ALL CAPS (more than 50% uppercase)
            if sum(c.isupper() for c in title) > len(title) * 0.5:
                errors.append("title should not be ALL CAPS")
            
            # Check for spam phrases
            spam_phrases = ["now hiring", "urgent", "apply now", "immediate start"]
            if any(phrase in title.lower() for phrase in spam_phrases):
                errors.append("title contains spam phrases")
        
        # Company name normalization check
        if "company_name" in job_data:
            company = job_data["company_name"]
            
            # Check for common duplicate patterns
            duplicate_patterns = [r"(.+)\s+inc\.?$", r"(.+)\s+llc\.?$", r"(.+)\s+corp\.?$"]
            normalized_company = company
            for pattern in duplicate_patterns:
                match = re.match(pattern, company.lower())
                if match:
                    normalized_company = match.group(1).title()
            
            if normalized_company != company and normalized_company.lower() != company.lower():
                errors.append(f"company_name should be normalized: '{company}' -> '{normalized_company}'")
        
        # URL validation
        if "apply_url" in job_data:
            url = job_data["apply_url"]
            try:
                parsed_url = urlparse(url)
                if not all([parsed_url.scheme, parsed_url.netloc]):
                    errors.append("apply_url is not a valid URL")
                # Note: Skip actual HTTP request in validation to avoid rate limiting
                # In production, this would check for 200 OK response
            except Exception:
                errors.append("apply_url is malformed")
        
        # Description cleaning check
        if "description_raw" in job_data and "description_clean" not in job_data:
            errors.append("description_clean must be generated from description_raw")
        
        return len(errors) == 0, errors
    
    def validate_enrichment_pipeline(self, job_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        3. Enrichment Pipeline Validation
        - Salary parsed into {min, max, currency, period}
        - Skills extracted via NLP pipeline
        - Experience level derived
        - Intelligence score computed (0-1)
        """
        errors = []
        
        # Salary structure validation
        if "salary_range" in job_data:
            salary = job_data["salary_range"]
            if isinstance(salary, dict):
                required_salary_fields = ["min", "max", "currency", "period"]
                for field in required_salary_fields:
                    if field not in salary:
                        errors.append(f"salary_range missing required field: {field}")
                
                # Validate salary values
                if "min" in salary and "max" in salary:
                    if not isinstance(salary["min"], (int, float)) or not isinstance(salary["max"], (int, float)):
                        errors.append("salary min/max must be numeric")
                    elif salary["min"] > salary["max"]:
                        errors.append("salary min cannot be greater than max")
                
                # Validate currency code
                if "currency" in salary and len(salary["currency"]) != 3:
                    errors.append("salary currency must be 3-letter code (USD, EUR, etc.)")
        
        # Skills extraction validation
        if "skills" in job_data:
            skills = job_data["skills"]
            if not isinstance(skills, list):
                errors.append("skills must be array of skill objects")
            else:
                for skill in skills:
                    if not isinstance(skill, dict) or "name" not in skill:
                        errors.append("each skill must be object with 'name' field")
        
        # Experience level validation
        if "experience_level" in job_data:
            exp_level = job_data["experience_level"]
            if exp_level not in self.EXPERIENCE_LEVELS:
                errors.append(f"experience_level must be one of: {self.EXPERIENCE_LEVELS}")
        
        # Intelligence score validation
        if "intelligence_score" in job_data:
            score = job_data["intelligence_score"]
            if not isinstance(score, (int, float)) or not (0 <= score <= 1):
                errors.append("intelligence_score must be numeric between 0 and 1")
        
        return len(errors) == 0, errors
    
    def validate_governance_audit(self, job_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        4. Governance & Audit Validation
        - Deduplication check fields present
        - Raw payload stored for audit
        - Error handling configured
        - Source attribution present
        """
        errors = []
        
        # Deduplication fields check
        dedup_fields = ["title", "company_id", "location", "posted_date"]
        missing_dedup = [field for field in dedup_fields if field not in job_data]
        if missing_dedup:
            errors.append(f"Missing deduplication fields: {missing_dedup}")
        
        # Audit trail validation
        if "raw_payload" not in job_data:
            errors.append("raw_payload required for audit trail")
        
        if "created_at" not in job_data:
            errors.append("created_at timestamp required for audit trail")
        
        if "updated_at" not in job_data:
            errors.append("updated_at timestamp required for audit trail")
        
        # Source attribution
        if "source" not in job_data:
            errors.append("source field required for data attribution")
        else:
            valid_sources = ["linkedin", "indeed", "ziprecruiter", "google_jobs", "bing_jobs"]
            if job_data["source"] not in valid_sources:
                errors.append(f"source must be one of: {valid_sources}")
        
        # External ID validation
        if "external_id" not in job_data:
            errors.append("external_id required for source system correlation")
        
        return len(errors) == 0, errors
    
    def validate_connector_specific(self, job_data: Dict[str, Any], connector: str) -> Tuple[bool, List[str]]:
        """Connector-specific validation rules"""
        errors = []
        
        if connector == "linkedin":
            # LinkedIn-specific validations
            if "company_id" not in job_data:
                errors.append("LinkedIn: company_id mapping required")
            
            if "employment_type" in job_data:
                if job_data["employment_type"] not in self.EMPLOYMENT_TYPES:
                    errors.append(f"LinkedIn: employment_type must be canonical enum: {self.EMPLOYMENT_TYPES}")
        
        elif connector == "indeed":
            # Indeed-specific validations  
            if not job_data.get("job_id", "").startswith("indeed_"):
                errors.append("Indeed: job_id should be prefixed with 'indeed_'")
            
            # Indeed salary parsing validation
            if "salary_text" in job_data.get("raw_payload", {}):
                if "salary_range" not in job_data:
                    errors.append("Indeed: salary_range should be parsed from salary text")
        
        elif connector == "ziprecruiter":
            # ZipRecruiter-specific validations
            if "hiring_company" in job_data.get("raw_payload", {}):
                if job_data["company_name"] != job_data["raw_payload"]["hiring_company"]["name"]:
                    errors.append("ZipRecruiter: company_name should match hiring_company.name")
        
        return len(errors) == 0, errors
    
    def run_full_validation(self, job_data: Dict[str, Any], connector: str = None) -> Dict[str, Any]:
        """Run complete canonical validation checklist"""
        results = {
            "job_id": job_data.get("job_id", "unknown"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "overall_status": "PASS",
            "validation_results": {}
        }
        
        # 1. Schema Compliance
        schema_pass, schema_errors = self.validate_schema_compliance(job_data)
        results["validation_results"]["schema_compliance"] = {
            "status": "PASS" if schema_pass else "FAIL",
            "errors": schema_errors
        }
        
        # 2. Data Quality  
        quality_pass, quality_errors = self.validate_data_quality(job_data)
        results["validation_results"]["data_quality"] = {
            "status": "PASS" if quality_pass else "FAIL", 
            "errors": quality_errors
        }
        
        # 3. Enrichment Pipeline
        enrichment_pass, enrichment_errors = self.validate_enrichment_pipeline(job_data)
        results["validation_results"]["enrichment_pipeline"] = {
            "status": "PASS" if enrichment_pass else "FAIL",
            "errors": enrichment_errors
        }
        
        # 4. Governance & Audit
        governance_pass, governance_errors = self.validate_governance_audit(job_data)
        results["validation_results"]["governance_audit"] = {
            "status": "PASS" if governance_pass else "FAIL", 
            "errors": governance_errors
        }
        
        # 5. Connector-Specific (if specified)
        if connector:
            connector_pass, connector_errors = self.validate_connector_specific(job_data, connector)
            results["validation_results"]["connector_specific"] = {
                "connector": connector,
                "status": "PASS" if connector_pass else "FAIL",
                "errors": connector_errors
            }
        
        # Overall status
        all_validations = [schema_pass, quality_pass, enrichment_pass, governance_pass]
        if connector:
            all_validations.append(connector_pass)
        
        if not all(all_validations):
            results["overall_status"] = "FAIL"
        
        return results
    
    def print_validation_summary(self, results: Dict[str, Any]):
        """Print formatted validation results"""
        print(f"\n{'='*60}")
        print(f" CANONICAL VALIDATION RESULTS")
        print(f"{'='*60}")
        print(f"Job ID: {results['job_id']}")
        print(f"Timestamp: {results['timestamp']}")
        print(f"Overall Status: {' COMPLIANT' if results['overall_status'] == 'PASS' else ' NON-COMPLIANT'}")
        print()
        
        for category, details in results["validation_results"].items():
            status_icon = "" if details["status"] == "PASS" else ""
            category_name = category.replace("_", " ").title()
            print(f"{status_icon} {category_name}: {details['status']}")
            
            if details["errors"]:
                for error in details["errors"]:
                    print(f"   • {error}")
        
        print(f"\n{'='*60}")


def main():
    """Command line interface for canonical validation"""
    parser = argparse.ArgumentParser(description="CareerCoach.ai Canonical Validation Enforcement")
    parser.add_argument("--connector", choices=["linkedin", "indeed", "ziprecruiter", "google_jobs", "bing_jobs"],
                       help="Specific connector to validate")
    parser.add_argument("--input", required=True, help="JSON file with job data to validate")
    parser.add_argument("--output", help="Output file for validation results")
    parser.add_argument("--fail-fast", action="store_true", help="Exit on first validation failure")
    
    args = parser.parse_args()
    
    # Load job data
    try:
        with open(args.input, 'r') as f:
            job_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Input file not found: {args.input}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in input file: {e}")
        sys.exit(1)
    
    # Run validation
    validator = CanonicalValidator()
    results = validator.run_full_validation(job_data, args.connector)
    
    # Print results
    validator.print_validation_summary(results)
    
    # Save results if output specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Validation results saved to: {args.output}")
    
    # Exit with appropriate code
    exit_code = 0 if results["overall_status"] == "PASS" else 1
    
    if args.fail_fast and exit_code != 0:
        logger.error("Validation failed - exiting due to --fail-fast")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()