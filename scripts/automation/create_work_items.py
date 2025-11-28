import requests
import os
import json
import base64
from urllib.parse import quote

# Azure DevOps details
organization = "CareerCoachai"
project = "CareerCoach.ai"
pat = os.getenv("AZURE_DEVOPS_PAT")  # Personal Access Token

if not pat:
    raise ValueError("AZURE_DEVOPS_PAT environment variable is not set.")

work_item_type = "User Story"
url = f"https://dev.azure.com/{quote(organization)}/{quote(project)}/_apis/wit/workitems/${quote(work_item_type)}?api-version=7.1"

headers = {
    "Authorization": f"Basic {base64.b64encode(f':{pat}'.encode()).decode()}",
    "Content-Type": "application/json-patch+json"
}

def create_user_story(title, description, area_path, iteration_path):
    payload = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": title
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": description
        },
        {
            "op": "add",
            "path": "/fields/System.AreaPath",
            "value": area_path
        },
        {
            "op": "add",
            "path": "/fields/System.IterationPath",
            "value": iteration_path
        }
    ]

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(f"User Story '{title}' created successfully.")
        return response.json()
    else:
        print(f"Failed to create User Story: {response.status_code} - {response.text}")
        return None

# Example usage
if __name__ == "__main__":
    create_user_story(
        title="Implement Redis Caching for Performance Optimization",
        description="As a developer, I want to implement Redis caching to improve application performance and reduce database load.",
        area_path="CareerCoach.ai\\Redis Caching",
        iteration_path="CareerCoach.ai\\Sprint 1"
    )

    create_user_story(
        title="Configure Prometheus for Monitoring",
        description="As a developer, I want to configure Prometheus to monitor API latency, database performance, and system health.",
        area_path="CareerCoach.ai\\Prometheus Monitoring",
        iteration_path="CareerCoach.ai\\Sprint 1"
    )

    create_user_story(
        title="Automate Deployment on Vercel and Render",
        description="As a developer, I want to automate the deployment of the frontend on Vercel and backend on Render for seamless CI/CD.",
        area_path="CareerCoach.ai\\Deployment Automation",
        iteration_path="CareerCoach.ai\\Sprint 1"
    )