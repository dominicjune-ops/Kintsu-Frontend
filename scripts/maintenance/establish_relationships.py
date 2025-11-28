import requests
import os
import base64
import csv

# Ensure proper work item relationships based on CSV data
org = os.getenv('AZURE_DEVOPS_ORG', 'CareerCoachai')
project = os.getenv('AZURE_DEVOPS_PROJECT', 'CareerCoach.ai')
pat = os.getenv('AZURE_DEVOPS_PAT')

auth = base64.b64encode(f':{pat}'.encode()).decode()
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {auth}'
}

patch_headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': f'Basic {auth}'
}

print('🔗 Establishing Complete Work Item Relationships...')
print('=' * 60)

# Load CSV data
epic_feature_mapping = {}
user_story_mapping = {}

with open('master_product_backlog.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        epic_id = row['Epic ID']
        user_story_id = row['User Story ID']

        if epic_id not in epic_feature_mapping:
            epic_feature_mapping[epic_id] = {
                'name': row['Epic Name'],
                'user_stories': []
            }
        epic_feature_mapping[epic_id]['user_stories'].append(user_story_id)

        user_story_mapping[user_story_id] = {
            'title': row['User Story Title'],
            'epic_id': epic_id
        }

print(f'Loaded {len(epic_feature_mapping)} epics with user stories from CSV')

# Get all existing work items
url = f'https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version=7.0'

# Get all epics
epic_query = '''
SELECT [System.Id], [System.Title], [System.Tags]
FROM WorkItems
WHERE [System.WorkItemType] = 'Epic'
ORDER BY [System.Id]
'''

epic_response = requests.post(url, json={'query': epic_query}, headers=headers)
epics = {}
if epic_response.status_code == 200:
    data = epic_response.json()
    for item in data.get('workItems', []):
        epics[item['id']] = item

print(f'Found {len(epics)} epics in Azure DevOps')

# Get all features
feature_query = '''
SELECT [System.Id], [System.Title], [System.Parent], [System.Tags]
FROM WorkItems
WHERE [System.WorkItemType] = 'Feature'
ORDER BY [System.Id]
'''

feature_response = requests.post(url, json={'query': feature_query}, headers=headers)
features = {}
if feature_response.status_code == 200:
    data = feature_response.json()
    for item in data.get('workItems', []):
        features[item['id']] = item

print(f'Found {len(features)} features in Azure DevOps')

# Get all user stories
story_query = '''
SELECT [System.Id], [System.Title], [System.Parent], [System.Tags]
FROM WorkItems
WHERE [System.WorkItemType] = 'User Story'
ORDER BY [System.Id]
'''

story_response = requests.post(url, json={'query': story_query}, headers=headers)
user_stories = {}
if story_response.status_code == 200:
    data = story_response.json()
    for item in data.get('workItems', []):
        user_stories[item['id']] = item

print(f'Found {len(user_stories)} user stories in Azure DevOps')

# Now establish relationships
print('\n🔗 Establishing Epic → Feature → User Story Relationships...')

relationships_updated = 0

# For each epic in CSV, ensure features exist and are linked
for epic_id, epic_data in epic_feature_mapping.items():
    print(f'\nProcessing Epic: {epic_id} - {epic_data["name"]}')

    # Find the corresponding Azure DevOps epic
    azure_epic_id = None
    for eid, epic in epics.items():
        if epic_id in epic.get('fields', {}).get('System.Title', ''):
            azure_epic_id = eid
            break

    if not azure_epic_id:
        print(f'   Could not find Azure DevOps epic for {epic_id}')
        continue

    print(f'   Found Azure DevOps Epic ID: {azure_epic_id}')

    # Group user stories by feature (we'll create features based on user story patterns)
    feature_groups = {}
    for story_id in epic_data['user_stories']:
        if story_id in user_story_mapping:
            # Create feature name based on user story title pattern
            story_title = user_story_mapping[story_id]['title']
            # Group by common prefixes or themes
            if 'GPT' in story_title or 'OpenAI' in story_title or 'LangChain' in story_title:
                feature_name = 'OpenAI GPT-4 Integration'
            elif 'Job Search' in story_title or 'Job Recommendations' in story_title or 'Job Alerts' in story_title:
                feature_name = 'Job Search System'
            elif 'Market Trend' in story_title or 'Competitive Intelligence' in story_title or 'Predictive Career' in story_title:
                feature_name = 'Market Trend Analysis'
            elif 'Article' in story_title or 'PRESENT' in story_title or 'CALM' in story_title or 'MATCH' in story_title:
                feature_name = 'Research Framework Automation'
            elif 'Premium' in story_title or 'Advanced Predictive' in story_title or 'Analytics' in story_title:
                feature_name = 'Advanced Predictive Modeling'
            elif 'Personality' in story_title or 'Aptitude' in story_title or 'Career Matching' in story_title:
                feature_name = 'Career Assessment System'
            else:
                feature_name = f'{epic_id} Core Features'

            if feature_name not in feature_groups:
                feature_groups[feature_name] = []
            feature_groups[feature_name].append(story_id)

    # Create or update features
    for feature_name, story_ids in feature_groups.items():
        print(f'    📁 Processing Feature: {feature_name} ({len(story_ids)} stories)')

        # Find existing feature or create new one
        feature_id = None
        for fid, feature in features.items():
            if feature_name in feature.get('fields', {}).get('System.Title', ''):
                feature_id = fid
                break

        if not feature_id:
            # Create new feature
            create_url = f'https://dev.azure.com/{org}/{project}/_apis/wit/workitems/$Feature?api-version=7.0'
            feature_data = [
                {
                    "op": "add",
                    "path": "/fields/System.Title",
                    "value": feature_name
                },
                {
                    "op": "add",
                    "path": "/fields/System.Parent",
                    "value": int(azure_epic_id)
                },
                {
                    "op": "add",
                    "path": "/fields/System.State",
                    "value": "New"
                },
                {
                    "op": "add",
                    "path": "/fields/System.Tags",
                    "value": f"{epic_id};feature"
                }
            ]

            create_response = requests.post(create_url, json=feature_data, headers=patch_headers)
            if create_response.status_code == 200:
                new_feature = create_response.json()
                feature_id = new_feature['id']
                features[feature_id] = new_feature
                print(f'       Created Feature ID: {feature_id}')
                relationships_updated += 1
            else:
                print(f'       Failed to create feature: {create_response.text}')
                continue
        else:
            # Ensure feature has correct parent
            detail_url = f'https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{feature_id}?$expand=all&api-version=7.0'
            detail_response = requests.get(detail_url, headers=headers)

            if detail_response.status_code == 200:
                item_data = detail_response.json()
                current_parent = item_data.get('fields', {}).get('System.Parent')

                if str(current_parent) != str(azure_epic_id):
                    # Update parent relationship
                    update_data = [
                        {
                            "op": "add",
                            "path": "/fields/System.Parent",
                            "value": int(azure_epic_id)
                        }
                    ]
                    update_url = f'https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{feature_id}?api-version=7.0'
                    update_response = requests.patch(update_url, json=update_data, headers=patch_headers)

                    if update_response.status_code == 200:
                        print(f'       Updated Feature {feature_id} parent to Epic {azure_epic_id}')
                        relationships_updated += 1
                    else:
                        print(f'       Failed to update feature parent: {update_response.text}')

        # Now link user stories to this feature
        if feature_id:
            for story_id in story_ids:
                # Find the Azure DevOps user story ID
                azure_story_id = None
                for sid, story in user_stories.items():
                    story_title = story.get('fields', {}).get('System.Title', '')
                    if story_id in story_title or user_story_mapping[story_id]['title'] in story_title:
                        azure_story_id = sid
                        break

                if azure_story_id:
                    # Check current parent
                    detail_url = f'https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{azure_story_id}?$expand=all&api-version=7.0'
                    detail_response = requests.get(detail_url, headers=headers)

                    if detail_response.status_code == 200:
                        item_data = detail_response.json()
                        current_parent = item_data.get('fields', {}).get('System.Parent')

                        if str(current_parent) != str(feature_id):
                            # Update parent relationship
                            update_data = [
                                {
                                    "op": "add",
                                    "path": "/fields/System.Parent",
                                    "value": int(feature_id)
                                }
                            ]
                            update_url = f'https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{azure_story_id}?api-version=7.0'
                            update_response = requests.patch(update_url, json=update_data, headers=patch_headers)

                            if update_response.status_code == 200:
                                print(f'         Linked User Story {azure_story_id} to Feature {feature_id}')
                                relationships_updated += 1
                            else:
                                print(f'         Failed to link story: {update_response.text}')

print(f'\n Relationship Establishment Complete!')
print(f'Updated {relationships_updated} relationships')
print('Hierarchy: Epic → Feature → User Story is now properly established.')