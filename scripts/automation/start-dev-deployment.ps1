# CareerCoach.ai Development Environment Deployment Starter
# Run this script to deploy to your development environment

param(
    [Parameter(Mandatory=$false)]
    [string]$SubscriptionId,
    
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroupName = "careercoach-rg-dev",
    
    [Parameter(Mandatory=$false)]
    [switch]$WhatIf = $true
)

Write-Host " CareerCoach.ai Development Deployment Starter" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Check prerequisites
Write-Host " Checking prerequisites..." -ForegroundColor Yellow

# Check Azure CLI
try {
    $azVersion = az --version 2>$null
    if ($azVersion) {
        Write-Host " Azure CLI is installed" -ForegroundColor Green
    } else {
        throw "Azure CLI not found"
    }
} catch {
    Write-Host " Azure CLI is not installed" -ForegroundColor Red
    Write-Host "Install it with: winget install Microsoft.AzureCLI" -ForegroundColor Yellow
    Write-Host "Then restart PowerShell and try again." -ForegroundColor Yellow
    exit 1
}

# Check Azure login
try {
    $account = az account show --output json 2>$null | ConvertFrom-Json
    if ($account) {
        Write-Host " Logged into Azure as: $($account.user.name)" -ForegroundColor Green
        Write-Host "   Current subscription: $($account.name)" -ForegroundColor Cyan
        
        if (-not $SubscriptionId) {
            $SubscriptionId = $account.id
            Write-Host "   Using current subscription: $SubscriptionId" -ForegroundColor Cyan
        }
    } else {
        throw "Not logged in"
    }
} catch {
    Write-Host " Not logged into Azure" -ForegroundColor Red
    Write-Host "Login with: az login" -ForegroundColor Yellow
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit 1
}

# Check PowerShell execution policy
$executionPolicy = Get-ExecutionPolicy
if ($executionPolicy -eq "Restricted") {
    Write-Host " PowerShell execution policy is restricted" -ForegroundColor Red
    Write-Host "Fix with: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host " PowerShell execution policy: $executionPolicy" -ForegroundColor Green
}

# Check deployment script exists
if (-not (Test-Path ".\scripts\deploy-multi-environment.ps1")) {
    Write-Host " Deployment script not found" -ForegroundColor Red
    Write-Host "Make sure you're in the CareerCoach.ai project root directory" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host " Deployment script found" -ForegroundColor Green
}

Write-Host ""
Write-Host " Deployment Configuration:" -ForegroundColor Yellow
Write-Host "   Environment: dev" -ForegroundColor Cyan
Write-Host "   Subscription: $SubscriptionId" -ForegroundColor Cyan
Write-Host "   Resource Group: $ResourceGroupName" -ForegroundColor Cyan
Write-Host "   Mode: $(if ($WhatIf) { 'Preview (WhatIf)' } else { 'Deploy' })" -ForegroundColor Cyan

Write-Host ""
if ($WhatIf) {
    Write-Host " Running in preview mode (no actual deployment)" -ForegroundColor Yellow
    Write-Host "This will show you what would be created without making changes." -ForegroundColor Yellow
} else {
    Write-Host " Running actual deployment" -ForegroundColor Green
    Write-Host "This will create real Azure resources." -ForegroundColor Yellow
}

Write-Host ""
$confirm = Read-Host "Continue? (y/N)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host " Starting deployment..." -ForegroundColor Green

try {
    # Run the deployment
    $deployParams = @{
        Environment = "dev"
        SubscriptionId = $SubscriptionId
        ResourceGroupName = $ResourceGroupName
    }
    
    if ($WhatIf) {
        $deployParams.Add("WhatIf", $true)
    }
    
    & ".\scripts\deploy-multi-environment.ps1" @deployParams
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host " Deployment completed successfully!" -ForegroundColor Green
        
        if (-not $WhatIf) {
            Write-Host ""
            Write-Host " Next Steps:" -ForegroundColor Yellow
            Write-Host "1. Test the health endpoint:" -ForegroundColor Cyan
            Write-Host "   curl https://careercoach-func-dev.azurewebsites.net/api/scraping_status" -ForegroundColor Gray
            Write-Host "2. Check Azure Portal for created resources" -ForegroundColor Cyan
            Write-Host "3. Set up monitoring:" -ForegroundColor Cyan
            Write-Host "   .\scripts\deploy-monitoring.ps1 -Environment dev -ResourceGroupName $ResourceGroupName -SubscriptionId $SubscriptionId" -ForegroundColor Gray
        } else {
            Write-Host ""
            Write-Host " Ready to deploy! Run again with -WhatIf:`$false to proceed with actual deployment." -ForegroundColor Green
        }
    } else {
        Write-Host ""
        Write-Host " Deployment failed. Check the error messages above." -ForegroundColor Red
    }
    
} catch {
    Write-Host ""
    Write-Host " Deployment failed with error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "📚 For more help, see DEV_DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan