#!/usr/bin/env python3
"""
Script to set Azure DevOps PAT and test wiki sync
"""

import os
import getpass
from azure_devops_realtime_sync import AzureDevOpsSync

def main():
    print("🔑 Azure DevOps PAT Setup & Wiki Sync Test")
    print("=" * 50)

    # Get current PAT
    current_pat = os.getenv('AZURE_DEVOPS_PAT', '')
    if current_pat and len(current_pat) > 30:
        print(" PAT appears to be set (length > 30 characters)")
        use_current = input("Use current PAT? (y/n): ").lower().strip()
        if use_current == 'y':
            pat = current_pat
        else:
            pat = getpass.getpass("Enter your Azure DevOps PAT: ")
    else:
        print(" No valid PAT found")
        pat = getpass.getpass("Enter your Azure DevOps PAT: ")

    # Set the PAT
    os.environ['AZURE_DEVOPS_PAT'] = pat
    print(" PAT set in environment")

    # Test the sync
    print("\n Testing README.md sync to Azure DevOps wiki...")
    try:
        sync = AzureDevOpsSync()
        result = sync.sync_wiki_content(force_update=True)
        if result:
            print(" Sync successful!")
        else:
            print(" Sync failed - check error messages above")
    except Exception as e:
        print(f" Error during sync: {e}")

if __name__ == "__main__":
    main()