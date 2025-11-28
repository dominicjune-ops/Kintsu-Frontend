# CareerCoach KPI Dashboard Setup Guide

A complete PowerShell automation script for setting up and managing your CareerCoach KPI Dashboard with Notion integration, Zapier automation, and real-time monitoring.

##  Quick Setup

### Prerequisites
```powershell
# 1. Install Python requirements
pip install -r requirements.txt
pip install notion-client aiohttp

# 2. Create Notion integration
# - Go to https://www.notion.so/my-integrations
# - Create new internal integration
# - Copy the API token
# - Share your parent page with the integration

# 3. Set environment variables
$env:NOTION_API_TOKEN = "secret_xxxxxxxxxxxxxxxxxxxxx"
$env:NOTION_PARENT_PAGE_ID = "your-parent-page-id"
$env:SLACK_ALERTS_WEBHOOK = "https://hooks.slack.com/services/xxx/xxx/xxx"
```

### One-Command Setup
```powershell
# Set up complete KPI dashboard
python scripts/kpi_dashboard.py --setup

# Run daily collection (for scheduling)
python scripts/kpi_dashboard.py --collect

# Test without pushing to Notion
python scripts/kpi_dashboard.py --test
```

##  Dashboard Components Created

### 1. Connector Performance Database
**Fields:**
- Connector (LinkedIn, Indeed, ZipRecruiter, Google Jobs, Bing Jobs)
- Status ( Planned, 🟡 In Progress, 🟢 Live,  Failed, 🔵 Maintenance)
- Date, Jobs Ingested (Daily), Unique Jobs (Daily)
- Schema/Data Quality/Enrichment Failures
- Intelligence Scores, Salary/Skills/Experience Enrichment
- Pipeline Latency (Avg/P95), API Response Time, Rate Limit Hits
- **Auto-calculated:** Deduplication Rate, Validation Pass Rate, Error Rate, Health Score

### 2. Epic 2 Milestone Tracker
**Pre-loaded Milestones:**
1. **Schema Foundation Complete** (Target: Feb 1)
2. **LinkedIn Connector Live** (Target: Feb 15) 
3. **Indeed + ZipRecruiter Live** (Target: Mar 1)
4. **Google Jobs + Bing Jobs Live** (Target: Mar 15)
5. **Enrichment Pipeline Live** (Target: Apr 1)
6. **Validation Framework Live** (Target: Apr 15)
7. **Cross-Platform Integration Complete** (Target: May 1)
8. **Epic 2 Production Ready** (Target: May 15)

##  Automation Setup

### Daily KPI Collection (Windows Task Scheduler)
```powershell
# Create daily task
$action = New-ScheduledTaskAction -Execute "python" -Argument "scripts/kpi_dashboard.py --collect" -WorkingDirectory "C:\Users\domin\OneDrive\Desktop\CareerCoach.ai\CareerCoach.ai"
$trigger = New-ScheduledTaskTrigger -Daily -At "6:00 AM"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName "CareerCoach KPI Collection" -Description "Daily KPI collection for CareerCoach dashboard"
```

### Real-Time Alerts (Slack Integration)
The script automatically checks these thresholds:
- 🚨 **Critical:** Error Rate > 10%
-  **Warning:** Validation Pass Rate < 90%
-  **Alert:** Health Score < 75
-  **Performance:** Pipeline Latency > 60s

##  Zapier Integration Webhooks

### Webhook 1: Connector Status Updates
```json
{
  "trigger": "Azure DevOps Pipeline Complete",
  "webhook_url": "https://hooks.zapier.com/hooks/catch/xxxx/connector-status/",
  "payload": {
    "connector": "linkedin",
    "status": "Live",
    "pipeline_result": "Success",
    "build_id": "12345",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "action": "Update Notion connector status + Slack notification"
}
```

### Webhook 2: Milestone Progress Updates  
```json
{
  "trigger": "GitHub PR Merged",
  "webhook_url": "https://hooks.zapier.com/hooks/catch/xxxx/milestone-progress/",
  "payload": {
    "milestone": "LinkedIn Connector Live",
    "progress_percent": 85,
    "completion_status": "In Progress", 
    "pr_number": 123,
    "assignee": "@developer"
  },
  "action": "Update milestone progress + notify team"
}
```

### Webhook 3: KPI Alert Escalation
```json
{
  "trigger": "KPI Threshold Breach",
  "webhook_url": "https://hooks.zapier.com/hooks/catch/xxxx/kpi-alerts/",
  "payload": {
    "connector": "indeed",
    "metric": "error_rate", 
    "current_value": 12.5,
    "threshold": 10,
    "severity": "critical",
    "health_score": 68
  },
  "action": "Escalate to on-call + create Notion task + Slack alert"
}
```

##  KPI Thresholds & SLA Targets

### Green Zone (Healthy)
```yaml
Health Score: ≥ 95
Error Rate: ≤ 5%
Validation Pass Rate: ≥ 95%
Deduplication Rate: ≥ 90%
Enrichment Coverage: ≥ 80%
Pipeline Latency: ≤ 30s
API Response Time: ≤ 200ms
```

### Yellow Zone (Warning)
```yaml
Health Score: 85-94
Error Rate: 5-10%
Validation Pass Rate: 90-94%
Deduplication Rate: 80-89%
Enrichment Coverage: 60-79%
Pipeline Latency: 30-60s
API Response Time: 200-500ms
```

### Red Zone (Critical)
```yaml
Health Score: < 85
Error Rate: > 10%
Validation Pass Rate: < 90%
Deduplication Rate: < 80%
Enrichment Coverage: < 60%
Pipeline Latency: > 60s
API Response Time: > 500ms
```

##  Integration Points

### Azure DevOps Pipeline Integration
```yaml
# Add to azure-pipelines.yml
- task: PowerShell@2
  displayName: 'Update KPI Dashboard'
  inputs:
    targetType: 'inline'
    script: |
      # Update connector status based on pipeline result
      $status = if ($env:Agent_JobStatus -eq "Succeeded") { "Live" } else { "Failed" }
      
      # Call KPI update webhook
      $webhook = "https://hooks.zapier.com/hooks/catch/xxxx/connector-status/"
      $payload = @{
        connector = "$(ConnectorName)"
        status = $status
        pipeline_result = "$env:Agent_JobStatus"
        build_id = "$env:Build_BuildId"
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
      } | ConvertTo-Json
      
      Invoke-RestMethod -Uri $webhook -Method Post -Body $payload -ContentType "application/json"
```

### GitHub Actions Integration
```yaml
# .github/workflows/kpi-update.yml
name: Update KPI Dashboard
on:
  pull_request:
    types: [closed]
  push:
    branches: [main]

jobs:
  update-kpi:
    runs-on: ubuntu-latest
    steps:
      - name: Update milestone progress
        if: github.event.pull_request.merged == true
        run: |
          curl -X POST "https://hooks.zapier.com/hooks/catch/xxxx/milestone-progress/" \
            -H "Content-Type: application/json" \
            -d '{
              "milestone": "${{ github.event.pull_request.labels[0].name }}",
              "progress_percent": 100,
              "completion_status": "Complete",
              "pr_number": ${{ github.event.pull_request.number }},
              "assignee": "${{ github.event.pull_request.user.login }}"
            }'
```

##  Manual Operations

### Update Individual Connector Metrics
```powershell
# Update specific connector
python -c "
from scripts.kpi_dashboard import KPIDataCollector, ConnectorMetrics
from datetime import datetime

collector = KPIDataCollector()
collector.notion_dashboard.connector_db_id = '$env:NOTION_CONNECTOR_DB_ID'

metrics = ConnectorMetrics(
    connector='linkedin',
    date=datetime.now().strftime('%Y-%m-%d'),
    jobs_ingested_daily=2500,
    unique_jobs_daily=2100,
    schema_failures=15,
    data_quality_failures=8,
    enrichment_failures=12,
    avg_intelligence_score=0.85,
    jobs_with_salary=2200,
    jobs_with_skills=2300,
    jobs_with_experience=2000,
    pipeline_latency_avg=25.0,
    pipeline_latency_p95=45.0,
    api_response_time=150.0,
    rate_limit_hits=2,
    last_sync=datetime.now().isoformat() + 'Z'
)

collector.notion_dashboard.update_connector_metrics(metrics)
print(' Updated LinkedIn metrics')
"
```

### Force Milestone Update
```powershell
# Update milestone status
python -c "
import requests
import os

headers = {
    'Authorization': f'Bearer {os.getenv(\"NOTION_API_TOKEN\")}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# Update milestone (replace PAGE_ID with actual page ID)
page_update = {
    'properties': {
        'Status': {'select': {'name': '🟢 Complete'}},
        'Progress': {'number': 100},
        'Actual Date': {'date': {'start': '2024-01-15'}}
    }
}

response = requests.patch(
    'https://api.notion.com/v1/pages/PAGE_ID',
    headers=headers,
    json=page_update
)

print(' Milestone updated' if response.status_code == 200 else f' Error: {response.text}')
"
```

## 🏃‍♂️ Getting Started

### 1. Initial Setup (5 minutes)
```powershell
# Clone and setup
cd "C:\Users\domin\OneDrive\Desktop\CareerCoach.ai\CareerCoach.ai"

# Install dependencies  
pip install notion-client aiohttp requests

# Set environment variables (replace with your values)
$env:NOTION_API_TOKEN = "secret_your_api_token_here"
$env:NOTION_PARENT_PAGE_ID = "your-page-id-here"
$env:SLACK_ALERTS_WEBHOOK = "your-slack-webhook-here"

# Create dashboard
python scripts/kpi_dashboard.py --setup
```

### 2. Verify Setup
```powershell
# Test data collection
python scripts/kpi_dashboard.py --test

# Manual collection test
python scripts/kpi_dashboard.py --collect
```

### 3. Schedule Automation
```powershell
# Set up daily collection task
$action = New-ScheduledTaskAction -Execute "python" -Argument "scripts/kpi_dashboard.py --collect" -WorkingDirectory "$PWD"
$trigger = New-ScheduledTaskTrigger -Daily -At "6:00 AM"  
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "CareerCoach KPI Collection"

Write-Host " KPI Dashboard is now live and automated!"
```

Your dashboard will be accessible at:
- **Connector Performance:** `https://notion.so/your-connector-db-id`
- **Epic 2 Milestones:** `https://notion.so/your-milestone-db-id`

##  Success Validation

After setup, you should see:
-  2 Notion databases created and populated
-  8 Epic 2 milestones pre-loaded with target dates
-  Sample connector metrics for last 7 days
-  Daily collection scheduled  
-  Slack alerts configured
-  All KPI calculations working (health scores, SLA status)

**Ready for Epic 2 rollout monitoring! **