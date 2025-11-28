#!/usr/bin/env python3
"""
Quick test of the webhook validation endpoint
"""

import requests
import json

def test_webhook_endpoint():
    """Test the webhook validation endpoint"""
    
    url = "http://localhost:8081/webhooks/test-zapier"
    
    try:
        response = requests.post(url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(" Server not running. Start with: uvicorn production_app:app --host 0.0.0.0 --port 8081")
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    test_webhook_endpoint()