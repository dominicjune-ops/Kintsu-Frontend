#!/usr/bin/env python3
"""
Azure DevOps Wiki Sync Setup Helper
Helps configure and test the wiki synchronization
"""

import os
import getpass

def setup_pat():
    """Help user set up their Azure DevOps PAT"""
    print("🔑 Azure DevOps Wiki Sync Setup")
    print("="*50)
    print()
    print("To sync the CareerCoach.ai Product Catalog to Azure DevOps Wiki,")
    print("you need a Personal Access Token (PAT) with the following permissions:")
    print()
    print("Required Permissions:")
    print("• Work Items: Read & Write")
    print("• Project and Team: Read")
    print("• Wiki: Read & Write")
    print()
    print("To create a PAT:")
    print("1. Go to: https://dev.azure.com/CareerCoachai/_usersSettings/tokens")
    print("2. Click 'New Token'")
    print("3. Name: 'CareerCoach Wiki Sync'")
    print("4. Organization: CareerCoachai")
    print("5. Scope: Custom defined")
    print("6. Set permissions as listed above")
    print("7. Expiration: Set to 1 year")
    print("8. Click 'Create'")
    print()
    print("  IMPORTANT: Copy the token immediately - you won't see it again!")
    print()

    pat = getpass.getpass("Enter your Azure DevOps PAT: ")
    if pat:
        os.environ['AZURE_DEVOPS_PAT'] = pat
        print(" PAT set successfully!")
        return True
    else:
        print(" No PAT entered")
        return False

def test_connection():
    """Test the Azure DevOps connection"""
    import requests
    import base64

    pat = os.getenv('AZURE_DEVOPS_PAT')
    if not pat:
        print(" AZURE_DEVOPS_PAT not set")
        return False

    # Create headers
    authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
    headers = {
        'Authorization': 'Basic '+authorization,
        'Content-Type': 'application/json'
    }

    print(" Testing Azure DevOps connection...")
    print("   Organization: CareerCoachai")
    print("   Project: CareerCoach.ai")

    try:
        # Test basic API access
        url = "https://dev.azure.com/CareerCoachai/CareerCoach.ai/_apis/projects?api-version=7.1"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print(" Connection successful!")
            return True
        elif response.status_code == 203:
            print(" Authentication failed - invalid PAT")
            return False
        else:
            print(f" Connection failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f" Error: {e}")
        return False

if __name__ == "__main__":
    print(" CareerCoach.ai Azure DevOps Wiki Sync Setup")
    print()

    if setup_pat():
        if test_connection():
            print()
            print(" Ready to sync wiki!")
            print("Run: python azure_devops_realtime_sync.py")
            print("Then select option 5: 'Update CareerCoach.ai Wiki'")
        else:
            print()
            print(" Setup failed. Please check your PAT and try again.")