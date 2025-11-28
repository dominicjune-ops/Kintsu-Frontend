# Azure Web App + Database Deployment Script
# CareerCoach.ai - Sprint 3 Deployment

Write-Host " CareerCoach.ai - Azure Deployment Script" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host ""

# Configuration
$resourceGroup = "careercoach-rg"
$location = "westus2"
$appServicePlan = "careercoach-plan"
$webAppName = "careercoach-api"
$runtime = "PYTHON:3.11"
$sku = "B1"

# Supabase Configuration (from .env)
$databaseUrl = "postgresql://postgres:t5XVwvfXnYYwQe3g@db.ktitfajlacjysacdsfxf.supabase.co:5432/postgres"
$supabaseUrl = "https://ktitfajlacjysacdsfxf.supabase.co"
$supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt0aXRmYWpsYWNqeXNhY2RzZnhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwNjM2ODQsImV4cCI6MjA3NzYzOTY4NH0.N4kCPI3GeLil80xADpMIN88nwxf3i4t1wlQ1I-oSnJ4"
$supabaseServiceKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt0aXRmYWpsYWNqeXNhY2RzZnhmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjA2MzY4NCwiZXhwIjoyMDc3NjM5Njg0fQ.h7Qt9vqPnz_YQ3nwLFJVO5sPGDrDTILBBoSux11Zw20"

# Step 1: Check Azure CLI
Write-Host " Step 1: Checking Azure CLI..." -ForegroundColor Yellow
try {
    $account = az account show 2>&1 | ConvertFrom-Json
    Write-Host " Logged in as: $($account.user.name)" -ForegroundColor Green
    Write-Host "   Subscription: $($account.name)" -ForegroundColor Gray
} catch {
    Write-Host " Not logged in to Azure CLI" -ForegroundColor Red
    Write-Host "   Run: az login" -ForegroundColor Yellow
    exit 1
}

# Step 2: Create Resource Group
Write-Host "`n Step 2: Creating Resource Group..." -ForegroundColor Yellow
Write-Host "   Name: $resourceGroup" -ForegroundColor Gray
Write-Host "   Location: $location" -ForegroundColor Gray

$rgExists = az group exists --name $resourceGroup
if ($rgExists -eq "true") {
    Write-Host " Resource group already exists" -ForegroundColor Green
} else {
    try {
        az group create --name $resourceGroup --location $location --output none
        Write-Host " Resource group created successfully" -ForegroundColor Green
    } catch {
        Write-Host " Failed to create resource group" -ForegroundColor Red
        Write-Host "   Error: $_" -ForegroundColor Red
        
        Write-Host "`n💡 Alternative: Use Azure Portal" -ForegroundColor Cyan
        Write-Host "   1. Go to https://portal.azure.com" -ForegroundColor Gray
        Write-Host "   2. Search 'Resource groups' → Create" -ForegroundColor Gray
        Write-Host "   3. Name: $resourceGroup, Region: West US 2" -ForegroundColor Gray
        
        $continue = Read-Host "`nDid you create the resource group in Portal? (y/n)"
        if ($continue -ne "y") {
            exit 1
        }
    }
}

# Step 3: Create App Service Plan
Write-Host "`n Step 3: Creating App Service Plan..." -ForegroundColor Yellow
Write-Host "   Name: $appServicePlan" -ForegroundColor Gray
Write-Host "   SKU: $sku (Basic - ~$13/month)" -ForegroundColor Gray

$planExists = az appservice plan show --name $appServicePlan --resource-group $resourceGroup 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " App Service Plan already exists" -ForegroundColor Green
} else {
    try {
        Write-Host "   Creating... (this takes ~30 seconds)" -ForegroundColor Gray
        az appservice plan create `
            --name $appServicePlan `
            --resource-group $resourceGroup `
            --sku $sku `
            --is-linux `
            --output none
        Write-Host " App Service Plan created successfully" -ForegroundColor Green
    } catch {
        Write-Host " Failed to create App Service Plan" -ForegroundColor Red
        Write-Host "   Error: $_" -ForegroundColor Red
        exit 1
    }
}

# Step 4: Create Web App
Write-Host "`n Step 4: Creating Web App..." -ForegroundColor Yellow
Write-Host "   Name: $webAppName" -ForegroundColor Gray
Write-Host "   Runtime: $runtime" -ForegroundColor Gray
Write-Host "   URL: https://$webAppName.azurewebsites.net" -ForegroundColor Gray

$webAppExists = az webapp show --name $webAppName --resource-group $resourceGroup 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " Web App already exists" -ForegroundColor Green
} else {
    try {
        Write-Host "   Creating... (this takes ~1 minute)" -ForegroundColor Gray
        az webapp create `
            --name $webAppName `
            --resource-group $resourceGroup `
            --plan $appServicePlan `
            --runtime $runtime `
            --output none
        Write-Host " Web App created successfully" -ForegroundColor Green
    } catch {
        Write-Host " Failed to create Web App" -ForegroundColor Red
        Write-Host "   Error: $_" -ForegroundColor Red
        
        Write-Host "`n💡 The name '$webAppName' might be taken. Try a different name:" -ForegroundColor Cyan
        Write-Host "   - careercoach-api-$((Get-Random -Maximum 9999))" -ForegroundColor Gray
        Write-Host "   - careercoach-prod" -ForegroundColor Gray
        Write-Host "   - dominic-careercoach-api" -ForegroundColor Gray
        exit 1
    }
}

# Step 5: Configure Environment Variables
Write-Host "`n Step 5: Configuring Environment Variables..." -ForegroundColor Yellow
Write-Host "   Setting 4 application settings..." -ForegroundColor Gray

try {
    az webapp config appsettings set `
        --name $webAppName `
        --resource-group $resourceGroup `
        --settings `
            DATABASE_URL="$databaseUrl" `
            SUPABASE_URL="$supabaseUrl" `
            SUPABASE_ANON_KEY="$supabaseAnonKey" `
            SUPABASE_SERVICE_ROLE_KEY="$supabaseServiceKey" `
        --output none
    Write-Host " Environment variables configured" -ForegroundColor Green
} catch {
    Write-Host " Failed to configure environment variables" -ForegroundColor Red
    Write-Host "   You can set them manually in Azure Portal" -ForegroundColor Yellow
}

# Step 6: Configure Deployment from GitHub
Write-Host "`n Step 6: Configuring GitHub Deployment..." -ForegroundColor Yellow
Write-Host "   Repository: dominicjune-ops/CareerCoach.ai" -ForegroundColor Gray
Write-Host "   Branch: main" -ForegroundColor Gray

Write-Host "`n  GitHub deployment requires manual authorization" -ForegroundColor Yellow
Write-Host "   Please complete this step in Azure Portal:" -ForegroundColor Cyan
Write-Host "   1. Go to: https://portal.azure.com/#resource/subscriptions/$($account.id)/resourceGroups/$resourceGroup/providers/Microsoft.Web/sites/$webAppName/vstscd" -ForegroundColor Gray
Write-Host "   2. Click 'Deployment Center' in left menu" -ForegroundColor Gray
Write-Host "   3. Source: GitHub" -ForegroundColor Gray
Write-Host "   4. Authorize and select:" -ForegroundColor Gray
Write-Host "      - Organization: dominicjune-ops" -ForegroundColor Gray
Write-Host "      - Repository: CareerCoach.ai" -ForegroundColor Gray
Write-Host "      - Branch: main" -ForegroundColor Gray
Write-Host "   5. Click 'Save'" -ForegroundColor Gray

# Step 7: Summary
Write-Host "`n" + ("=" * 70)
Write-Host " DEPLOYMENT SUMMARY" -ForegroundColor Green
Write-Host ("=" * 70)

Write-Host "`n Resources Created:" -ForegroundColor Cyan
Write-Host "    Resource Group: $resourceGroup" -ForegroundColor Green
Write-Host "    App Service Plan: $appServicePlan ($sku)" -ForegroundColor Green
Write-Host "    Web App: $webAppName" -ForegroundColor Green
Write-Host "    Environment Variables: 4 settings configured" -ForegroundColor Green

Write-Host "`n🔗 Your API URL:" -ForegroundColor Cyan
Write-Host "   https://$webAppName.azurewebsites.net" -ForegroundColor White

Write-Host "`n Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Complete GitHub deployment setup in Portal (see instructions above)" -ForegroundColor Gray
Write-Host "   2. Wait for first deployment (~5-10 minutes)" -ForegroundColor Gray
Write-Host "   3. Test your API:" -ForegroundColor Gray
Write-Host "      curl https://$webAppName.azurewebsites.net/health" -ForegroundColor Gray

Write-Host "`n Monitor Deployment:" -ForegroundColor Cyan
Write-Host "   • Azure Portal: https://portal.azure.com" -ForegroundColor Gray
Write-Host "   • GitHub Actions: https://github.com/dominicjune-ops/CareerCoach.ai/actions" -ForegroundColor Gray
Write-Host "   • App Logs: az webapp log tail --name $webAppName --resource-group $resourceGroup" -ForegroundColor Gray

Write-Host "`n✨ Deployment script complete!" -ForegroundColor Green
Write-Host ""

# Optional: Open Portal
$openPortal = Read-Host "Open Azure Portal to complete GitHub setup? (y/n)"
if ($openPortal -eq "y") {
    Start-Process "https://portal.azure.com/#resource/subscriptions/$($account.id)/resourceGroups/$resourceGroup/providers/Microsoft.Web/sites/$webAppName/vstscd"
}
