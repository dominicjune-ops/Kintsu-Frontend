#!/usr/bin/env python3
"""
Quick test of CareerCoach.ai automation endpoints
"""

import requests
import json

def test_zapier_endpoint():
    """Test Zapier webhook endpoint"""
    try:
        response = requests.post("http://localhost:8081/webhooks/zapier/job-digest", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(" Zapier Integration Working!")
            print(f" Jobs Available: {result.get('payload', {}).get('jobs_scraped', 0)}")
            print(f" Revenue Potential: ${result.get('payload', {}).get('revenue_potential', 0):,}")
            print(f" Average Salary: ${result.get('payload', {}).get('avg_salary', 0):,}")
            return True
        else:
            print(f" Zapier test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f" Connection error: {str(e)}")
        print("💡 Make sure the server is running at http://localhost:8081")
        return False

def test_platform_stats():
    """Test platform statistics"""
    try:
        response = requests.get("http://localhost:8081/api/stats", timeout=10)
        
        if response.status_code == 200:
            stats = response.json()
            print(" Platform Statistics Working!")
            print(f" Total Jobs: {stats.get('total_jobs', 0)}")
            print(f" Average Salary: ${stats.get('average_salary', 0):,.0f}")
            print(f"🏢 Companies: {stats.get('companies', 0)}")
            return True
        else:
            print(f" Stats test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f" Connection error: {str(e)}")
        return False

if __name__ == "__main__":
    print(" CareerCoach.ai Quick Integration Test")
    print("=" * 50)
    
    # Test basic platform
    stats_ok = test_platform_stats()
    print()
    
    # Test Zapier integration
    zapier_ok = test_zapier_endpoint()
    print()
    
    print("=" * 50)
    if stats_ok and zapier_ok:
        print(" SUCCESS: All integrations working!")
        print("💡 Your platform is ready for automation workflows!")
    else:
        print("  Some tests failed - check server status")
        print("💡 Run: python production_app.py to start server")