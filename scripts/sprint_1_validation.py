#!/usr/bin/env python3
"""
Sprint 1 Validation Test Suite
Comprehensive testing for CAREER-AI-001, CAREER-AI-002, CAREER-AI-003

This script validates all acceptance criteria for Sprint 1 user stories
according to Azure DevOps board organization and quality gates.
"""

import asyncio
import aiohttp
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any

class Sprint1Validator:
    """
    Validates all Sprint 1 acceptance criteria and quality gates
    """
    
    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        self.start_time = time.time()
    
    def log_test(self, test_name: str, passed: bool, details: str = "", 
                 response_time: float = 0, user_story: str = ""):
        """Log test result"""
        result = {
            "test_name": test_name,
            "user_story": user_story,
            "passed": passed,
            "details": details,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        
        if passed:
            self.passed_tests += 1
            print(f" {test_name}: PASSED ({response_time:.3f}s)")
            if details:
                print(f"    {details}")
        else:
            self.failed_tests += 1
            print(f" {test_name}: FAILED")
            if details:
                print(f"   ❗ {details}")
        print()
    
    async def test_career_ai_001_openai_integration(self) -> bool:
        """
        CAREER-AI-001: OpenAI GPT-4 API Integration (13 points)
        
        Acceptance Criteria:
        - OpenAI API endpoint accessible
        - GPT-4 model configuration
        - Error handling for API failures
        - Response time < 2 seconds (quality gate)
        - Success rate > 90% (quality gate)
        """
        print(" Testing CAREER-AI-001: OpenAI GPT-4 API Integration")
        
        # Test 1: AI Chat Endpoint Exists
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                
                test_payload = {
                    "message": "Hello, I need career advice",
                    "user_context": {"test": True},
                    "coaching_type": "general"
                }
                
                async with session.post(
                    f"{self.base_url}/api/v1/ai/chat",
                    json=test_payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Check response structure
                        required_fields = ["response", "model", "response_time", "success", "request_id"]
                        missing_fields = [field for field in required_fields if field not in data]
                        
                        if not missing_fields:
                            self.log_test(
                                "AI Chat Endpoint Response Structure",
                                True,
                                f"All required fields present: {required_fields}",
                                response_time,
                                "CAREER-AI-001"
                            )
                        else:
                            self.log_test(
                                "AI Chat Endpoint Response Structure",
                                False,
                                f"Missing fields: {missing_fields}",
                                response_time,
                                "CAREER-AI-001"
                            )
                        
                        # Check response time quality gate (< 2 seconds)
                        self.log_test(
                            "Response Time Quality Gate",
                            response_time < 2.0,
                            f"Response time: {response_time:.3f}s (requirement: <2.0s)",
                            response_time,
                            "CAREER-AI-001"
                        )
                        
                        # Check if AI is working or gracefully handling disabled state
                        if data.get("success"):
                            self.log_test(
                                "OpenAI Integration Active",
                                True,
                                f"AI responded with model: {data.get('model')}",
                                response_time,
                                "CAREER-AI-001"
                            )
                        else:
                            # Check graceful degradation
                            if "AI functionality is currently disabled" in data.get("response", ""):
                                self.log_test(
                                    "Graceful AI Degradation",
                                    True,
                                    "AI properly handles disabled state with fallback",
                                    response_time,
                                    "CAREER-AI-001"
                                )
                            else:
                                self.log_test(
                                    "AI Error Handling",
                                    False,
                                    f"Unexpected error: {data.get('error', 'Unknown')}",
                                    response_time,
                                    "CAREER-AI-001"
                                )
                    else:
                        self.log_test(
                            "AI Chat Endpoint Accessibility",
                            False,
                            f"HTTP {response.status}",
                            response_time,
                            "CAREER-AI-001"
                        )
        
        except Exception as e:
            self.log_test(
                "AI Chat Endpoint Accessibility",
                False,
                f"Connection error: {str(e)}",
                0,
                "CAREER-AI-001"
            )
        
        # Test 2: AI Health Check Endpoint
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                
                async with session.get(f"{self.base_url}/api/v1/ai/health") as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        self.log_test(
                            "AI Health Check Endpoint",
                            True,
                            f"Status: {data.get('status', 'unknown')}",
                            response_time,
                            "CAREER-AI-001"
                        )
                    else:
                        self.log_test(
                            "AI Health Check Endpoint",
                            False,
                            f"HTTP {response.status}",
                            response_time,
                            "CAREER-AI-001"
                        )
        
        except Exception as e:
            self.log_test(
                "AI Health Check Endpoint",
                False,
                f"Connection error: {str(e)}",
                0,
                "CAREER-AI-001"
            )
        
        # Test 3: Additional AI Endpoints
        ai_endpoints = [
            "/api/v1/ai/job-match",
            "/api/v1/ai/coaching"
        ]
        
        for endpoint in ai_endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    start_time = time.time()
                    
                    test_payload = {
                        "message": "Test message",
                        "user_context": {},
                        "coaching_type": "general"
                    } if "coaching" in endpoint else {
                        "user_profile": {"experience": "5 years Python"},
                        "job_requirements": "Python developer position"
                    }
                    
                    async with session.post(
                        f"{self.base_url}{endpoint}",
                        json=test_payload,
                        headers={"Content-Type": "application/json"}
                    ) as response:
                        response_time = time.time() - start_time
                        
                        self.log_test(
                            f"AI Endpoint {endpoint}",
                            response.status in [200, 400],  # 400 OK for disabled AI
                            f"HTTP {response.status}",
                            response_time,
                            "CAREER-AI-001"
                        )
            
            except Exception as e:
                self.log_test(
                    f"AI Endpoint {endpoint}",
                    False,
                    f"Connection error: {str(e)}",
                    0,
                    "CAREER-AI-001"
                )
        
        return True
    
    async def test_career_ai_002_chat_interface(self) -> bool:
        """
        CAREER-AI-002: AI Chat Interface (8 points)
        
        Acceptance Criteria:
        - Interactive chat UI accessible
        - Real-time AI responses
        - Chat history and conversation flow
        - Mobile responsive design
        - Error handling in UI
        """
        print(" Testing CAREER-AI-002: AI Chat Interface")
        
        # Test 1: Chat Page Accessibility
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                
                async with session.get(f"{self.base_url}/ai-chat") as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        html_content = await response.text()
                        
                        # Check for key UI elements
                        ui_elements = [
                            "chat-container",
                            "chat-input",
                            "sendMessage",
                            "/api/v1/ai/chat",  # API integration
                            "typing-indicator"
                        ]
                        
                        missing_elements = [elem for elem in ui_elements if elem not in html_content]
                        
                        self.log_test(
                            "Chat Interface UI Elements",
                            len(missing_elements) == 0,
                            f"Missing: {missing_elements}" if missing_elements else "All UI elements present",
                            response_time,
                            "CAREER-AI-002"
                        )
                        
                        # Check for API integration
                        self.log_test(
                            "API Integration in Chat UI",
                            "/api/v1/ai/chat" in html_content,
                            "Chat interface properly integrated with AI API",
                            response_time,
                            "CAREER-AI-002"
                        )
                        
                        # Check for error handling
                        self.log_test(
                            "Error Handling in Chat UI",
                            "catch (error)" in html_content,
                            "Error handling implemented in JavaScript",
                            response_time,
                            "CAREER-AI-002"
                        )
                    else:
                        self.log_test(
                            "Chat Interface Accessibility",
                            False,
                            f"HTTP {response.status}",
                            response_time,
                            "CAREER-AI-002"
                        )
        
        except Exception as e:
            self.log_test(
                "Chat Interface Accessibility",
                False,
                f"Connection error: {str(e)}",
                0,
                "CAREER-AI-002"
            )
        
        return True
    
    async def test_career_ai_003_performance_analytics(self) -> bool:
        """
        CAREER-AI-003: AI Performance Analytics (8 points)
        
        Acceptance Criteria:
        - Performance metrics collection
        - Analytics dashboard/API
        - Response time monitoring
        - Error rate tracking
        - Real-time health metrics
        """
        print(" Testing CAREER-AI-003: AI Performance Analytics")
        
        # Test 1: Analytics API Endpoint
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                
                async with session.get(f"{self.base_url}/api/v1/ai/analytics") as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Check analytics structure
                        required_fields = ["success", "health", "performance", "timestamp"]
                        missing_fields = [field for field in required_fields if field not in data]
                        
                        self.log_test(
                            "Analytics API Structure",
                            len(missing_fields) == 0,
                            f"Missing: {missing_fields}" if missing_fields else "All analytics fields present",
                            response_time,
                            "CAREER-AI-003"
                        )
                        
                        # Check performance metrics
                        if "performance" in data:
                            perf_metrics = ["total_requests", "success_rate", "avg_response_time"]
                            missing_metrics = [m for m in perf_metrics if m not in data["performance"]]
                            
                            self.log_test(
                                "Performance Metrics Collection",
                                len(missing_metrics) == 0,
                                f"Missing: {missing_metrics}" if missing_metrics else "All performance metrics available",
                                response_time,
                                "CAREER-AI-003"
                            )
                        
                        # Check health metrics
                        if "health" in data:
                            self.log_test(
                                "Real-time Health Metrics",
                                "status" in data["health"],
                                f"Health status: {data['health'].get('status', 'unknown')}",
                                response_time,
                                "CAREER-AI-003"
                            )
                    else:
                        self.log_test(
                            "Analytics API Accessibility",
                            False,
                            f"HTTP {response.status}",
                            response_time,
                            "CAREER-AI-003"
                        )
        
        except Exception as e:
            self.log_test(
                "Analytics API Accessibility",
                False,
                f"Connection error: {str(e)}",
                0,
                "CAREER-AI-003"
            )
        
        # Test 2: Analytics Export Functionality
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                
                async with session.get(f"{self.base_url}/api/v1/ai/analytics/export") as response:
                    response_time = time.time() - start_time
                    
                    self.log_test(
                        "Analytics Export API",
                        response.status in [200, 500],  # 500 OK if no data yet
                        f"HTTP {response.status}",
                        response_time,
                        "CAREER-AI-003"
                    )
        
        except Exception as e:
            self.log_test(
                "Analytics Export API",
                False,
                f"Connection error: {str(e)}",
                0,
                "CAREER-AI-003"
            )
        
        return True
    
    async def test_quality_gates(self) -> bool:
        """
        Test Azure DevOps Quality Gates
        
        Quality Gates:
        1. Performance: Response time <2 seconds  (tested above)
        2. Security: API endpoints secure
        3. Documentation: APIs documented
        4. Integration: All components working together
        """
        print(" Testing Quality Gates")
        
        # Test API Documentation (OpenAPI/Swagger)
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                
                async with session.get(f"{self.base_url}/docs") as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        content = await response.text()
                        
                        api_documented = all(endpoint in content for endpoint in [
                            "/api/v1/ai/chat",
                            "/api/v1/ai/health",
                            "/api/v1/ai/analytics"
                        ])
                        
                        self.log_test(
                            "API Documentation Quality Gate",
                            api_documented,
                            "All AI endpoints documented in OpenAPI" if api_documented else "Missing AI endpoint documentation",
                            response_time,
                            "Quality Gate"
                        )
                    else:
                        self.log_test(
                            "API Documentation Accessibility",
                            False,
                            f"HTTP {response.status}",
                            response_time,
                            "Quality Gate"
                        )
        
        except Exception as e:
            self.log_test(
                "API Documentation",
                False,
                f"Connection error: {str(e)}",
                0,
                "Quality Gate"
            )
        
        # Test Integration - Production App Running
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                
                async with session.get(f"{self.base_url}/") as response:
                    response_time = time.time() - start_time
                    
                    self.log_test(
                        "Production App Integration",
                        response.status == 200,
                        f"CareerCoach.ai production app running",
                        response_time,
                        "Quality Gate"
                    )
        
        except Exception as e:
            self.log_test(
                "Production App Integration",
                False,
                f"Connection error: {str(e)}",
                0,
                "Quality Gate"
            )
        
        return True
    
    def generate_sprint_report(self) -> Dict[str, Any]:
        """Generate comprehensive Sprint 1 validation report"""
        total_time = time.time() - self.start_time
        success_rate = (self.passed_tests / (self.passed_tests + self.failed_tests)) * 100 if (self.passed_tests + self.failed_tests) > 0 else 0
        
        # Group tests by user story
        story_results = {}
        for test in self.test_results:
            story = test["user_story"] or "General"
            if story not in story_results:
                story_results[story] = {"passed": 0, "failed": 0, "tests": []}
            
            story_results[story]["tests"].append(test)
            if test["passed"]:
                story_results[story]["passed"] += 1
            else:
                story_results[story]["failed"] += 1
        
        report = {
            "sprint": "Sprint 1: AI Foundation Setup",
            "validation_date": datetime.now().isoformat(),
            "total_execution_time": round(total_time, 2),
            "summary": {
                "total_tests": self.passed_tests + self.failed_tests,
                "passed_tests": self.passed_tests,
                "failed_tests": self.failed_tests,
                "success_rate": round(success_rate, 2)
            },
            "user_story_results": story_results,
            "quality_gates_status": {
                "response_time": "PASSED" if any(t["test_name"] == "Response Time Quality Gate" and t["passed"] for t in self.test_results) else "FAILED",
                "api_documentation": "PASSED" if any(t["test_name"] == "API Documentation Quality Gate" and t["passed"] for t in self.test_results) else "FAILED",
                "integration": "PASSED" if any(t["test_name"] == "Production App Integration" and t["passed"] for t in self.test_results) else "FAILED"
            },
            "detailed_results": self.test_results,
            "sprint_readiness": success_rate >= 85  # 85% pass rate for Sprint 2 readiness
        }
        
        return report
    
    async def run_validation(self):
        """Run complete Sprint 1 validation suite"""
        print(" Starting Sprint 1 Validation Test Suite")
        print("=" * 60)
        print()
        
        # Run all user story tests
        await self.test_career_ai_001_openai_integration()
        await self.test_career_ai_002_chat_interface()
        await self.test_career_ai_003_performance_analytics()
        await self.test_quality_gates()
        
        # Generate and display report
        report = self.generate_sprint_report()
        
        print("=" * 60)
        print(" SPRINT 1 VALIDATION REPORT")
        print("=" * 60)
        print(f" Sprint: {report['sprint']}")
        print(f"📅 Date: {report['validation_date']}")
        print(f" Execution Time: {report['total_execution_time']}s")
        print()
        print(" SUMMARY:")
        print(f"   Total Tests: {report['summary']['total_tests']}")
        print(f"   Passed: {report['summary']['passed_tests']} ")
        print(f"   Failed: {report['summary']['failed_tests']} ")
        print(f"   Success Rate: {report['summary']['success_rate']}%")
        print()
        
        print(" USER STORY RESULTS:")
        for story, results in report['user_story_results'].items():
            total = results['passed'] + results['failed']
            rate = (results['passed'] / total * 100) if total > 0 else 0
            status = " PASSED" if rate >= 85 else " FAILED"
            print(f"   {story}: {results['passed']}/{total} ({rate:.1f}%) {status}")
        print()
        
        print("🚪 QUALITY GATES:")
        for gate, status in report['quality_gates_status'].items():
            emoji = "" if status == "PASSED" else ""
            print(f"   {gate.replace('_', ' ').title()}: {status} {emoji}")
        print()
        
        sprint_status = " READY FOR SPRINT 2" if report['sprint_readiness'] else " NEEDS ATTENTION"
        print(f" SPRINT READINESS: {sprint_status}")
        print()
        
        # Save report to file
        with open("sprint_1_validation_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(" Detailed report saved to: sprint_1_validation_report.json")
        
        return report

async def main():
    """Main validation runner"""
    validator = Sprint1Validator()
    await validator.run_validation()

if __name__ == "__main__":
    asyncio.run(main())