#!/usr/bin/env python3
"""
CareerCoach.ai - Comprehensive Smoke Test
Tests all critical systems and identifies issues
"""

import asyncio
import os
import sys
import json
import aiohttp
import traceback
from datetime import datetime
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

class SmokeTest:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "overall_status": "UNKNOWN",
            "critical_issues": [],
            "warnings": []
        }
        
        # Load environment
        load_dotenv()
    
    async def run_all_tests(self):
        """Run comprehensive smoke test suite"""
        
        print("🔥 CareerCoach.ai - Comprehensive Smoke Test")
        print("=" * 60)
        
        # Test categories
        tests = [
            ("Environment Setup", self.test_environment),
            ("Python Dependencies", self.test_dependencies),
            ("Data Pipeline", self.test_data_pipeline),
            ("Job Database", self.test_job_database),
            ("Zapier Integration", self.test_zapier_webhook),
            ("FastAPI Application", self.test_fastapi_app),
            ("API Endpoints", self.test_api_endpoints),
            ("Automation Workflows", self.test_automation)
        ]
        
        for test_name, test_func in tests:
            print(f"\n Testing: {test_name}")
            print("-" * 40)
            
            try:
                result = await test_func()
                self.results["tests"][test_name] = result
                
                if result["status"] == "PASS":
                    print(f" {test_name}: PASSED")
                elif result["status"] == "WARN":
                    print(f" {test_name}: WARNING - {result['message']}")
                    self.results["warnings"].append(f"{test_name}: {result['message']}")
                else:
                    print(f" {test_name}: FAILED - {result['message']}")
                    self.results["critical_issues"].append(f"{test_name}: {result['message']}")
                    
            except Exception as e:
                error_msg = f"Test crashed: {str(e)}"
                print(f"💥 {test_name}: CRASHED - {error_msg}")
                self.results["tests"][test_name] = {
                    "status": "FAIL",
                    "message": error_msg,
                    "exception": traceback.format_exc()
                }
                self.results["critical_issues"].append(f"{test_name}: {error_msg}")
        
        # Determine overall status
        self.determine_overall_status()
        self.print_summary()
        return self.results
    
    async def test_environment(self):
        """Test environment setup"""
        issues = []
        
        # Check Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        if sys.version_info < (3, 8):
            issues.append(f"Python {python_version} too old (need 3.8+)")
        
        # Check .env file
        if not os.path.exists('.env'):
            issues.append("Missing .env file")
        
        # Check virtual environment
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            issues.append("Not running in virtual environment")
        
        # Check key directories
        required_dirs = ['src', 'config', 'schema']
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                issues.append(f"Missing directory: {dir_name}")
        
        if issues:
            return {"status": "FAIL", "message": "; ".join(issues)}
        
        return {"status": "PASS", "message": f"Python {python_version}, virtual env active"}
    
    async def test_dependencies(self):
        """Test Python dependencies"""
        required_packages = [
            'fastapi', 'uvicorn', 'aiohttp', 'requests', 
            'notion_client', 'dotenv', 'pydantic'
        ]
        
        missing = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            return {"status": "FAIL", "message": f"Missing packages: {', '.join(missing)}"}
        
        return {"status": "PASS", "message": f"All {len(required_packages)} dependencies available"}
    
    async def test_data_pipeline(self):
        """Test data pipeline service"""
        try:
            from data_pipeline_service import DataPipelineService
            
            pipeline = DataPipelineService()
            await pipeline.initialize()
            
            # Check job counts
            jobs = pipeline.get_all_jobs()
            if len(jobs) < 50:
                return {"status": "WARN", "message": f"Only {len(jobs)} jobs loaded (expected 50+)"}
            
            return {"status": "PASS", "message": f"Data pipeline loaded {len(jobs)} jobs"}
            
        except Exception as e:
            return {"status": "FAIL", "message": f"Data pipeline error: {str(e)}"}
    
    async def test_job_database(self):
        """Test job database files"""
        issues = []
        
        # Check comprehensive database
        if os.path.exists('comprehensive_jobs_db.json'):
            try:
                with open('comprehensive_jobs_db.json', 'r') as f:
                    data = json.load(f)
                    if len(data) < 50:
                        issues.append(f"Comprehensive DB only has {len(data)} jobs")
            except json.JSONDecodeError:
                issues.append("Comprehensive DB is corrupted JSON")
        else:
            issues.append("Missing comprehensive_jobs_db.json")
        
        # Check scraped cache
        if os.path.exists('scraped_jobs_cache.json'):
            try:
                with open('scraped_jobs_cache.json', 'r') as f:
                    data = json.load(f)
                    if not data.get('jobs'):
                        issues.append("Scraped cache has no jobs")
            except json.JSONDecodeError:
                issues.append("Scraped cache is corrupted JSON")
        
        if issues:
            return {"status": "WARN", "message": "; ".join(issues)}
        
        return {"status": "PASS", "message": "Job databases are healthy"}
    
    async def test_zapier_webhook(self):
        """Test Zapier webhook connectivity"""
        webhook_url = os.getenv('ZAPIER_WEBHOOK_URL')
        
        if not webhook_url:
            return {"status": "FAIL", "message": "No ZAPIER_WEBHOOK_URL configured"}
        
        if '[your-account-id]' in webhook_url:
            return {"status": "FAIL", "message": "Placeholder webhook URL still configured"}
        
        try:
            test_data = {"test": "smoke_test", "timestamp": datetime.now().isoformat()}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    webhook_url,
                    json=test_data,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        return {"status": "PASS", "message": "Zapier webhook responding"}
                    else:
                        return {"status": "WARN", "message": f"Webhook status {response.status}"}
                        
        except Exception as e:
            return {"status": "FAIL", "message": f"Webhook connection failed: {str(e)}"}
    
    async def test_fastapi_app(self):
        """Test FastAPI application can start"""
        try:
            # Import the app
            from production_app import app
            
            # Check if app has required endpoints
            routes = [route.path for route in app.routes]
            required_routes = ['/api/jobs', '/webhooks/zapier/job-digest']
            
            missing_routes = [route for route in required_routes if route not in routes]
            if missing_routes:
                return {"status": "FAIL", "message": f"Missing routes: {missing_routes}"}
            
            return {"status": "PASS", "message": f"FastAPI app loaded with {len(routes)} routes"}
            
        except Exception as e:
            return {"status": "FAIL", "message": f"FastAPI app error: {str(e)}"}
    
    async def test_api_endpoints(self):
        """Test API endpoints if server is running"""
        try:
            async with aiohttp.ClientSession() as session:
                # Test health endpoint
                async with session.get('http://localhost:8081/') as response:
                    if response.status != 200:
                        return {"status": "WARN", "message": "Server not running on port 8081"}
                
                # Test jobs API
                async with session.get('http://localhost:8081/api/jobs?limit=5') as response:
                    if response.status == 200:
                        data = await response.json()
                        if len(data) > 0:
                            return {"status": "PASS", "message": f"API serving {len(data)} jobs"}
                        else:
                            return {"status": "WARN", "message": "API returns no jobs"}
                    else:
                        return {"status": "FAIL", "message": f"Jobs API returns {response.status}"}
                        
        except aiohttp.ClientConnectorError:
            return {"status": "WARN", "message": "Server not running - start with uvicorn production_app:app --port 8081"}
        except Exception as e:
            return {"status": "FAIL", "message": f"API test error: {str(e)}"}
    
    async def test_automation(self):
        """Test automation workflow functions"""
        try:
            # Import automation functions
            from production_app import send_to_zapier_webhook
            
            # Test with dummy data
            test_data = {"test": "automation_smoke_test"}
            result = await send_to_zapier_webhook(test_data)
            
            if result.get("status") == "success":
                return {"status": "PASS", "message": "Automation functions working"}
            else:
                return {"status": "WARN", "message": f"Automation test: {result.get('message', 'Unknown issue')}"}
                
        except Exception as e:
            return {"status": "FAIL", "message": f"Automation error: {str(e)}"}
    
    def determine_overall_status(self):
        """Determine overall system health"""
        if self.results["critical_issues"]:
            self.results["overall_status"] = "CRITICAL"
        elif self.results["warnings"]:
            self.results["overall_status"] = "WARNING"
        else:
            self.results["overall_status"] = "HEALTHY"
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("🏁 SMOKE TEST SUMMARY")
        print("=" * 60)
        
        # Overall status
        status_emoji = {"HEALTHY": "", "WARNING": "", "CRITICAL": ""}
        print(f"Overall Status: {status_emoji.get(self.results['overall_status'], '❓')} {self.results['overall_status']}")
        
        # Critical issues
        if self.results["critical_issues"]:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.results['critical_issues'])}):")
            for issue in self.results["critical_issues"]:
                print(f"    {issue}")
        
        # Warnings
        if self.results["warnings"]:
            print(f"\n WARNINGS ({len(self.results['warnings'])}):")
            for warning in self.results["warnings"]:
                print(f"    {warning}")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        if self.results["overall_status"] == "CRITICAL":
            print("    Fix critical issues before deployment")
        elif self.results["overall_status"] == "WARNING":
            print("    Address warnings for optimal performance")
        else:
            print("    System is ready for production!")
        
        print("\n" + "=" * 60)

async def main():
    """Run smoke test"""
    smoke_test = SmokeTest()
    results = await smoke_test.run_all_tests()
    
    # Save results
    with open('smoke_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n Full results saved to: smoke_test_results.json")
    
    return results["overall_status"] == "HEALTHY"

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)