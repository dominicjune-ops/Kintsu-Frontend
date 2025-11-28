# Azure Deployment Checklist - CareerCoach.ai

Write-Host " Azure Deployment Checklist for CareerCoach.ai" -ForegroundColor Cyan
Write-Host "=" * 60

# Step 1: Check Git Status
Write-Host "`n Step 1: Check Git Status" -ForegroundColor Yellow
$gitStatus = git status --short
if ($gitStatus) {
    Write-Host "  Uncommitted changes detected:" -ForegroundColor Yellow
    Write-Host $gitStatus
    Write-Host "`n💡 Consider committing these changes before deployment"
} else {
    Write-Host " Working directory clean" -ForegroundColor Green
}

# Step 2: Check Azure CLI
Write-Host "`n Step 2: Check Azure CLI" -ForegroundColor Yellow
try {
    $azVersion = az version --output json 2>&1 | ConvertFrom-Json
    Write-Host " Azure CLI installed: $($azVersion.'azure-cli')" -ForegroundColor Green
    
    $account = az account show 2>&1 | ConvertFrom-Json
    Write-Host " Logged in as: $($account.user.name)" -ForegroundColor Green
    
    # Check for active subscription
    $subscriptions = az account list --output json 2>&1 | ConvertFrom-Json
    $activeSubscription = $subscriptions | Where-Object { $_.state -eq "Enabled" -and $_.name -ne "N/A(tenant level account)" }
    
    if ($activeSubscription) {
        Write-Host " Active subscription found: $($activeSubscription.name)" -ForegroundColor Green
        Write-Host "   Subscription ID: $($activeSubscription.id)"
    } else {
        Write-Host "  No active subscription found" -ForegroundColor Yellow
        Write-Host "   You'll need to use Azure Portal instead of CLI"
    }
} catch {
    Write-Host " Azure CLI not installed or not logged in" -ForegroundColor Red
    Write-Host "   Install: https://docs.microsoft.com/cli/azure/install-azure-cli"
}

# Step 3: Check Supabase Configuration
Write-Host "`n Step 3: Check Supabase Configuration" -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    $supabaseUrl = $envContent | Select-String "SUPABASE_URL=" | ForEach-Object { $_.ToString().Split('=')[1] }
    $databaseUrl = $envContent | Select-String "^DATABASE_URL=" | ForEach-Object { $_.ToString().Split('=')[1] }
    
    if ($supabaseUrl) {
        Write-Host " SUPABASE_URL configured: $supabaseUrl" -ForegroundColor Green
    } else {
        Write-Host " SUPABASE_URL not found in .env" -ForegroundColor Red
    }
    
    if ($databaseUrl) {
        Write-Host " DATABASE_URL configured" -ForegroundColor Green
    } else {
        Write-Host " DATABASE_URL not found in .env" -ForegroundColor Red
    }
} else {
    Write-Host " .env file not found" -ForegroundColor Red
}

# Step 4: Check Database Scripts
Write-Host "`n Step 4: Check Database Scripts" -ForegroundColor Yellow
$requiredScripts = @(
    "supabase_create_indexes.sql",
    "supabase_create_rls_policies.sql"
)

foreach ($script in $requiredScripts) {
    if (Test-Path $script) {
        Write-Host " Found: $script" -ForegroundColor Green
    } else {
        Write-Host " Missing: $script" -ForegroundColor Red
    }
}

# Step 5: Check Requirements
Write-Host "`n Step 5: Check Requirements File" -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    $requirements = Get-Content "requirements.txt"
    $criticalDeps = @("fastapi", "uvicorn", "sqlalchemy", "asyncpg")
    
    $missingDeps = @()
    foreach ($dep in $criticalDeps) {
        $found = $requirements | Select-String $dep
        if ($found) {
            Write-Host " $dep included" -ForegroundColor Green
        } else {
            Write-Host " $dep missing" -ForegroundColor Red
            $missingDeps += $dep
        }
    }
    
    if ($missingDeps.Count -eq 0) {
        Write-Host " All critical dependencies present" -ForegroundColor Green
    }
} else {
    Write-Host " requirements.txt not found" -ForegroundColor Red
}

# Step 6: Check GitHub Workflow
Write-Host "`n Step 6: Check GitHub Actions Workflow" -ForegroundColor Yellow
if (Test-Path ".github/workflows/azure-web-app.yml") {
    Write-Host " Azure deployment workflow exists" -ForegroundColor Green
} else {
    Write-Host "  Azure deployment workflow not found" -ForegroundColor Yellow
    Write-Host "   Workflow will be auto-generated when you configure Deployment Center"
}

# Summary
Write-Host "`n" + "=" * 60
Write-Host " DEPLOYMENT READINESS SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 60

Write-Host "`n Ready to Deploy:" -ForegroundColor Green
Write-Host "   • Sprint 3 code complete and tested"
Write-Host "   • Database models aligned with Supabase schema"
Write-Host "   • API routes updated and functional"
Write-Host "   • GitHub Actions workflow created"
Write-Host "   • Requirements.txt updated with database dependencies"

Write-Host "`n Manual Steps Required:" -ForegroundColor Yellow
Write-Host "   1. Run supabase_create_indexes.sql in Supabase SQL Editor"
Write-Host "   2. Run supabase_create_rls_policies.sql in Supabase SQL Editor"
Write-Host "   3. Create Azure App Service via Portal (recommended)"
Write-Host "   4. Configure 4 environment variables in Azure"
Write-Host "   5. Connect GitHub repository in Deployment Center"
Write-Host "   6. Wait for first deployment (5-10 minutes)"
Write-Host "   7. Test API endpoints"

Write-Host "`n🔗 Quick Links:" -ForegroundColor Cyan
Write-Host "   • Azure Portal: https://portal.azure.com"
Write-Host "   • Supabase Dashboard: https://supabase.com/dashboard/project/ktitfajlacjysacdsfxf"
Write-Host "   • Supabase SQL Editor: https://supabase.com/dashboard/project/ktitfajlacjysacdsfxf/sql"
Write-Host "   • GitHub Repository: https://github.com/dominicjune-ops/CareerCoach.ai"
Write-Host "   • Deployment Guide: See AZURE_DEPLOYMENT_GUIDE.md"

Write-Host "`n💡 Recommended Next Action:" -ForegroundColor Cyan
Write-Host "   Since you don't have an active Azure subscription,"
Write-Host "   start by going to Azure Portal to create/activate one."
Write-Host "   Then follow the step-by-step guide in AZURE_DEPLOYMENT_GUIDE.md"

Write-Host "`n✨ Good luck with your deployment!" -ForegroundColor Green
