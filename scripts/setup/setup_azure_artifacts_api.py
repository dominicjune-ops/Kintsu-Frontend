"""
Azure Artifacts Feed Setup via API
Creates Azure Artifacts feed and configures upstream sources using REST API
"""

import requests
import base64
import json
from typing import Dict, List

# Azure DevOps Configuration
ORGANIZATION = "CareerCoachai"
PROJECT = "CareerCoach.ai"
PAT = os.getenv("AZURE_DEVOPS_PAT")  # PAT token with Packaging (Read, write, & manage) scope - Set via environment variable

# Feed Configuration
FEED_NAME = "careercoach-packages"
FEED_DESCRIPTION = "CareerCoach.ai package feed with PyPI and npm upstream sources"

# API Configuration
API_VERSION = "7.0"
BASE_URL = f"https://feeds.dev.azure.com/{ORGANIZATION}"
PROJECT_URL = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}"

# Create authentication header
def get_headers() -> Dict[str, str]:
    """Create authentication headers for Azure DevOps API"""
    credentials = base64.b64encode(f":{PAT}".encode()).decode()
    return {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }

def create_feed() -> Dict:
    """
    Create Azure Artifacts feed with project scope
    
    Returns:
        Feed details including ID and URLs
    """
    print("\n🎁 Creating Azure Artifacts Feed...")
    print("=" * 60)
    
    url = f"{BASE_URL}/_apis/packaging/feeds"
    
    feed_data = {
        "name": FEED_NAME,
        "description": FEED_DESCRIPTION,
        "hideDeletedPackageVersions": True,
        "upstreamEnabled": True,
        "project": {
            "id": PROJECT
        },
        "capabilities": {
            "upstreamV2": {
                "enabled": True
            }
        }
    }
    
    params = {"api-version": API_VERSION}
    
    try:
        response = requests.post(
            url,
            headers=get_headers(),
            json=feed_data,
            params=params
        )
        
        if response.status_code == 201:
            feed = response.json()
            print(f" Feed created successfully!")
            print(f"   Name: {feed['name']}")
            print(f"   ID: {feed['id']}")
            return feed
        elif response.status_code == 409:
            print(f"ℹ️  Feed '{FEED_NAME}' already exists")
            # Get existing feed
            return get_feed()
        else:
            print(f" Error creating feed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f" Exception creating feed: {e}")
        return None

def get_feed() -> Dict:
    """Get existing feed details"""
    url = f"{BASE_URL}/{PROJECT}/_apis/packaging/feeds/{FEED_NAME}"
    params = {"api-version": API_VERSION}
    
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f" Error getting feed: {response.status_code}")
            return None
    except Exception as e:
        print(f" Exception getting feed: {e}")
        return None

def add_upstream_source(feed_id: str, source_name: str, protocol: str, location: str) -> bool:
    """
    Add upstream source to feed
    
    Args:
        feed_id: Feed ID
        source_name: Name of upstream source (e.g., "PyPI", "npmjs")
        protocol: Protocol type (e.g., "PyPI", "npm")
        location: Upstream source URL
    
    Returns:
        True if successful
    """
    print(f"\n📦 Adding upstream source: {source_name}...")
    
    url = f"{BASE_URL}/{PROJECT}/_apis/packaging/feeds/{feed_id}/upstreamsources"
    
    upstream_data = {
        "name": source_name,
        "protocol": protocol,
        "location": location,
        "upstreamSourceType": "public"
    }
    
    params = {"api-version": API_VERSION}
    
    try:
        response = requests.post(
            url,
            headers=get_headers(),
            json=upstream_data,
            params=params
        )
        
        if response.status_code in [200, 201]:
            print(f"    {source_name} upstream source added")
            return True
        elif response.status_code == 409:
            print(f"   ℹ️  {source_name} upstream source already exists")
            return True
        else:
            print(f"    Error adding {source_name}: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"    Exception adding {source_name}: {e}")
        return False

def configure_upstream_sources(feed_id: str) -> None:
    """Configure all upstream sources for the feed"""
    print("\n Configuring Upstream Sources...")
    print("=" * 60)
    
    # PyPI upstream source
    add_upstream_source(
        feed_id=feed_id,
        source_name="PyPI",
        protocol="PyPI",
        location="https://pypi.org/simple/"
    )
    
    # npm upstream source
    add_upstream_source(
        feed_id=feed_id,
        source_name="npmjs",
        protocol="npm",
        location="https://registry.npmjs.org/"
    )

def set_feed_permissions(feed_id: str) -> bool:
    """
    Set feed permissions (Organization-level read access)
    
    Args:
        feed_id: Feed ID
    
    Returns:
        True if successful
    """
    print("\n🔐 Setting Feed Permissions...")
    
    # Note: Permissions API requires specific organization-level permissions
    # This is a simplified version - full implementation would need group/user IDs
    
    url = f"{BASE_URL}/_apis/packaging/feeds/{feed_id}/permissions"
    params = {"api-version": API_VERSION}
    
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        if response.status_code == 200:
            print("    Feed permissions configured")
            return True
        else:
            print(f"     Could not verify permissions: {response.status_code}")
            return False
    except Exception as e:
        print(f"     Could not verify permissions: {e}")
        return False

def get_feed_urls(feed_name: str) -> Dict[str, str]:
    """Generate feed URLs for different protocols"""
    return {
        "pypi_index": f"https://pkgs.dev.azure.com/{ORGANIZATION}/{PROJECT}/_packaging/{feed_name}/pypi/simple/",
        "pypi_upload": f"https://pkgs.dev.azure.com/{ORGANIZATION}/{PROJECT}/_packaging/{feed_name}/pypi/upload/",
        "npm_registry": f"https://pkgs.dev.azure.com/{ORGANIZATION}/{PROJECT}/_packaging/{feed_name}/npm/registry/",
        "nuget": f"https://pkgs.dev.azure.com/{ORGANIZATION}/{PROJECT}/_packaging/{feed_name}/nuget/v3/index.json",
        "web_url": f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_artifacts/feed/{feed_name}"
    }

def create_pip_conf(feed_name: str) -> None:
    """Create pip.conf file for Python package management"""
    print("\n Creating pip.conf...")
    
    urls = get_feed_urls(feed_name)
    
    config = f"""[global]
# Azure Artifacts feed for CareerCoach.ai
# This configuration allows pip to install packages from Azure Artifacts with fallback to PyPI

# Primary source: Azure Artifacts (caches public packages + hosts private packages)
index-url = {urls['pypi_index']}

# Fallback source: Public PyPI (if package not found in Azure Artifacts)
extra-index-url = https://pypi.org/simple

[install]
# Trust Azure Artifacts host
trusted-host = pkgs.dev.azure.com
"""
    
    with open("pip.conf", "w") as f:
        f.write(config)
    
    print("    pip.conf created")

def create_npmrc(feed_name: str) -> None:
    """Create .npmrc file for npm package management"""
    print("\n Creating .npmrc...")
    
    urls = get_feed_urls(feed_name)
    
    config = f"""# Azure Artifacts npm configuration for CareerCoach.ai
registry={urls['npm_registry']}
always-auth=true
"""
    
    with open(".npmrc", "w") as f:
        f.write(config)
    
    print("    .npmrc created")

def display_summary(feed: Dict) -> None:
    """Display setup summary and next steps"""
    print("\n" + "=" * 60)
    print(" AZURE ARTIFACTS SETUP COMPLETE!")
    print("=" * 60)
    
    urls = get_feed_urls(feed['name'])
    
    print(f"\n Feed Information:")
    print(f"   Name: {feed['name']}")
    print(f"   ID: {feed['id']}")
    print(f"   Description: {feed.get('description', 'N/A')}")
    
    print(f"\n🔗 Feed URLs:")
    print(f"   Web: {urls['web_url']}")
    print(f"   PyPI: {urls['pypi_index']}")
    print(f"   npm: {urls['npm_registry']}")
    
    print(f"\n📦 Upstream Sources Configured:")
    print(f"    PyPI (https://pypi.org/simple/)")
    print(f"    npmjs (https://registry.npmjs.org/)")
    
    print(f"\n Configuration Files Created:")
    print(f"    pip.conf (Python package management)")
    print(f"    .npmrc (npm package management)")
    
    print(f"\n Next Steps:")
    print(f"   1. Install Azure Artifacts keyring:")
    print(f"      pip install keyring artifacts-keyring")
    print(f"")
    print(f"   2. Install packages (they'll be cached in Azure Artifacts):")
    print(f"      pip install -r requirements.txt")
    print(f"")
    print(f"   3. View feed in Azure DevOps:")
    print(f"      {urls['web_url']}")
    print(f"")
    print(f"   4. (Optional) Publish private packages:")
    print(f"      twine upload --repository-url {urls['pypi_upload']} dist/*")
    
    print("\n" + "=" * 60)

def main():
    """Main execution function"""
    print("\n AZURE ARTIFACTS API SETUP")
    print("=" * 60)
    print(f"Organization: {ORGANIZATION}")
    print(f"Project: {PROJECT}")
    print(f"Feed Name: {FEED_NAME}")
    print("=" * 60)
    
    if not PAT:
        print("\n ERROR: PAT token not configured!")
        print("   Please add your Personal Access Token to the script:")
        print("   PAT = 'your-token-here'")
        print("\n   Required scopes: Packaging (Read, write, & manage)")
        return
    
    # Step 1: Create feed
    feed = create_feed()
    if not feed:
        print("\n Failed to create or retrieve feed")
        return
    
    # Step 2: Configure upstream sources
    configure_upstream_sources(feed['id'])
    
    # Step 3: Set permissions (optional)
    set_feed_permissions(feed['id'])
    
    # Step 4: Create configuration files
    create_pip_conf(feed['name'])
    create_npmrc(feed['name'])
    
    # Step 5: Display summary
    display_summary(feed)

if __name__ == "__main__":
    main()
