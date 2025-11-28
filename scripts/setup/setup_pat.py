#!/usr/bin/env python3
"""
Azure DevOps PAT Setup and Verification
"""

import requests
import base64
import getpass
import os

def setup_and_verify_pat():
    """Set up and verify Azure DevOps PAT"""

    print("🔐 Azure DevOps PAT Setup & Verification")
    print("="*45)

    # Get PAT from user
    print("\n Enter your Azure DevOps Personal Access Token:")
    print("   (Go to https://dev.azure.com → User settings → Personal access tokens)")
    print("   Required scopes: Work Items (Read/Write), Project/Team (Read), Wiki (Read/Write)")

    pat = getpass.getpass("PAT: ")
    if not pat:
        print(" No PAT entered")
        return False

    # Test the PAT
    print("\n Testing PAT...")

    credentials = f":{pat}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    # Test 1: Organization access
    print("1. Testing organization access...")
    org_url = "https://dev.azure.com/CareerCoachai/_apis/organization?api-version=7.1"
    response = requests.get(org_url, headers=headers)
    print(f"   Status: {response.status_code}")

    if response.status_code == 203:
        print("    PAT authentication failed - check if PAT is correct and not expired")
        print("   💡 Make sure your PAT has these scopes:")
        print("      - Work Items: Read & Write")
        print("      - Project and Team: Read")
        print("      - Wiki: Read & Write")
        return False

    # Test 2: Project access
    print("\n2. Testing project access...")
    projects_url = "https://dev.azure.com/CareerCoachai/_apis/projects?api-version=7.1"
    response = requests.get(projects_url, headers=headers)
    print(f"   Status: {response.status_code}")

    if response.status_code != 200:
        print(f"    Project access failed: {response.status_code}")
        return False

    projects = response.json().get('value', [])
    print(f"    Found {len(projects)} projects")

    # Test 3: Wiki access
    print("\n3. Testing wiki access...")
    wiki_url = "https://dev.azure.com/CareerCoachai/CareerCoach.ai/_apis/wiki/wikis?api-version=7.1"
    response = requests.get(wiki_url, headers=headers)
    print(f"   Status: {response.status_code}")

    if response.status_code != 200:
        print(f"    Wiki access failed: {response.status_code}")
        return False

    wikis = response.json().get('value', [])
    print(f"    Found {len(wikis)} wikis")

    # Success - set environment variable
    print("\n PAT verification successful!")
    print(" Setting AZURE_DEVOPS_PAT environment variable...")

    # For PowerShell
    print("\n Run this command in PowerShell to set the PAT permanently:")
    print(f"$env:AZURE_DEVOPS_PAT = '{pat}'")
    print("\nOr add it to your PowerShell profile for persistence.")

    # Set it for current session
    os.environ['AZURE_DEVOPS_PAT'] = pat
    print(" PAT set for current session")

    return True

if __name__ == "__main__":
    success = setup_and_verify_pat()
    if success:
        print("\n Ready to sync wiki! Run:")
        print("python azure_devops_realtime_sync.py")
        print("Then choose option 5")
    else:
        print("\n PAT setup failed. Please check your PAT and try again.")