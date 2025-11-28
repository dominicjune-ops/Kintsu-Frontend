Write-Host "CareerCoach.ai Azure DevOps Sync Setup" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will help you set up Azure DevOps synchronization." -ForegroundColor Yellow
Write-Host ""
Write-Host "You need a Personal Access Token (PAT) with Work Items permissions." -ForegroundColor Yellow
Write-Host ""
Write-Host "To create a PAT:" -ForegroundColor Green
Write-Host "1. Go to: https://dev.azure.com/" -ForegroundColor Green
Write-Host "2. Sign in with your Microsoft account" -ForegroundColor Green
Write-Host "3. User Settings → Personal Access Tokens → New Token" -ForegroundColor Green
Write-Host "4. Set scope: Work Items (Read, Write, Manage)" -ForegroundColor Green
Write-Host "5. Copy the token" -ForegroundColor Green
Write-Host ""

$pat = Read-Host "Enter your Azure DevOps PAT" -AsSecureString
$patPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($pat))

if (-not $patPlain) {
    Write-Host " ERROR: PAT cannot be empty. Please try again." -ForegroundColor Red
    exit 1
}

# Add error handling for invalid PAT
if ($patPlain.Length -lt 20) {
    Write-Host " ERROR: The PAT seems too short. Please ensure you have copied the full token." -ForegroundColor Red
    exit 1
}

[Environment]::SetEnvironmentVariable("AZURE_DEVOPS_PAT", $patPlain, "Machine")
[Environment]::SetEnvironmentVariable("AZURE_DEVOPS_ORG", "CareerCoachai", "Machine")
[Environment]::SetEnvironmentVariable("AZURE_DEVOPS_PROJECT", "CareerCoach.ai", "Machine")

# Also set for current process in case registry access fails
$env:AZURE_DEVOPS_PAT = $patPlain
$env:AZURE_DEVOPS_ORG = "CareerCoachai"
$env:AZURE_DEVOPS_PROJECT = "CareerCoach.ai"

if ($?) {
    Write-Host " SUCCESS: Azure DevOps environment variables set successfully." -ForegroundColor Green
} else {
    Write-Host " ERROR: Failed to set environment variables." -ForegroundColor Red
    exit 1
}

# Log setup success to a file
$logFile = "setup_azure_sync.log"
$logMessage = "[$(Get-Date)] Azure DevOps sync setup completed successfully."
Add-Content -Path $logFile -Value $logMessage
Write-Host " SUCCESS: Setup log written to $logFile" -ForegroundColor Green

Write-Host ""
Write-Host "PAT: $patPlain" -ForegroundColor Gray
Write-Host "Organization: CareerCoachai" -ForegroundColor White
Write-Host "Project: CareerCoach.ai" -ForegroundColor White
Write-Host ""
Write-Host "You can now run the sync service with: python azure_devops_realtime_sync.py" -ForegroundColor Cyan
Read-Host "Press Enter to continue"