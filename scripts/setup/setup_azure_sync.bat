@echo off
echo CareerCoach.ai Azure DevOps Sync Setup
echo ===================================
echo.
echo This script will help you set up Azure DevOps synchronization.
echo.
echo You need a Personal Access Token (PAT) with Work Items permissions.
echo.
echo To create a PAT:
echo 1. Go to: https://dev.azure.com/
echo 2. Sign in with your Microsoft account
echo 3. User Settings → Personal Access Tokens → New Token
echo 4. Set scope: Work Items (Read, Write, Manage)
echo 5. Copy the token
echo.
set /p PAT="Enter your Azure DevOps PAT: "
setx AZURE_DEVOPS_PAT "%PAT%" /M
setx AZURE_DEVOPS_ORG "CareerCoachai" /M
setx AZURE_DEVOPS_PROJECT "CareerCoach.ai" /M
echo.
echo Environment variables set successfully!
echo PAT: %PAT%
echo Organization: CareerCoachai
echo Project: CareerCoach.ai
echo.
echo You can now run the sync service with: python azure_devops_realtime_sync.py
pause