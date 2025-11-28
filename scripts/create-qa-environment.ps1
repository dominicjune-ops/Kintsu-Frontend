#!/usr/bin/env powershell
# CareerCoach.ai QA Environment Creation Script
# Creates complete QA infrastructure in Azure

param(
    [Parameter(Mandatory=$false)]
    [string]$Location = "westus",
    
    [Parameter(Mandatory=$false)]
    [switch]$WhatIf = $false
)

$ErrorActionPreference = "Stop"

Write-Host " Creating CareerCoach.ai QA Environment" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host "Location: $Location" -ForegroundColor Cyan
Write-Host "Mode: $(if ($WhatIf) { 'Preview (WhatIf)' } else { 'Deploy' })" -ForegroundColor Cyan
Write-Host ""

# Check Azure login
Write-Host " Checking Azure authentication..." -ForegroundColor Yellow
try {
    $account = az account show --output json | ConvertFrom-Json
    Write-Host " Logged in as: $($account.user.name)" -ForegroundColor Green
    Write-Host " Subscription: $($account.name) ($($account.id))" -ForegroundColor Cyan
}
catch {
    Write-Error " Not logged into Azure. Please run 'az login' first."
    exit 1
}

Write-Host ""

# Define resource names
$resourceGroupName = "CareerCoach-QA-RG"
$keyVaultName = "careercoach-qa-kv"
$cosmosDbName = "careercoach-qa-cosmos"
$storageAccountName = "careercoachstorageqa"
$functionAppName = "careercoach-func-qa"
$appInsightsName = "careercoach-insights-qa"

# Resource creation functions
function New-ResourceGroup {
    Write-Host "📁 Creating Resource Group: $resourceGroupName" -ForegroundColor Yellow
    
    if ($WhatIf) {
        Write-Host " Would create resource group: $resourceGroupName in $Location" -ForegroundColor Cyan
        return $true
    }
    
    try {
        $result = az group create --name $resourceGroupName --location $Location --output json | ConvertFrom-Json
        Write-Host " Resource Group created: $($result.name)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Error " Failed to create Resource Group: $_"
        return $false
    }
}

function New-KeyVault {
    Write-Host "🔐 Creating Key Vault: $keyVaultName" -ForegroundColor Yellow
    
    if ($WhatIf) {
        Write-Host " Would create Key Vault: $keyVaultName" -ForegroundColor Cyan
        return $true
    }
    
    try {
        $result = az keyvault create `
            --name $keyVaultName `
            --resource-group $resourceGroupName `
            --location $Location `
            --enable-rbac-authorization `
            --output json | ConvertFrom-Json
            
        Write-Host " Key Vault created: $($result.name)" -ForegroundColor Green
        Write-Host "🔗 Vault URI: $($result.properties.vaultUri)" -ForegroundColor Cyan
        return $true
    }
    catch {
        Write-Error " Failed to create Key Vault: $_"
        return $false
    }
}

function New-CosmosDb {
    Write-Host "🗄️ Creating Cosmos DB: $cosmosDbName" -ForegroundColor Yellow
    
    if ($WhatIf) {
        Write-Host " Would create Cosmos DB: $cosmosDbName (MongoDB API)" -ForegroundColor Cyan
        return $true
    }
    
    try {
        $result = az cosmosdb create `
            --name $cosmosDbName `
            --resource-group $resourceGroupName `
            --kind MongoDB `
            --locations regionName=$Location failoverPriority=0 isZoneRedundant=false `
            --default-consistency-level "Session" `
            --enable-automatic-failover false `
            --max-staleness-prefix 100 `
            --max-interval 5 `
            --output json | ConvertFrom-Json
            
        Write-Host " Cosmos DB created: $($result.name)" -ForegroundColor Green
        Write-Host "🔗 MongoDB Connection: $($result.connectionStrings[0].connectionString)" -ForegroundColor Cyan
        return $true
    }
    catch {
        Write-Error " Failed to create Cosmos DB: $_"
        return $false
    }
}

function New-StorageAccount {
    Write-Host " Creating Storage Account: $storageAccountName" -ForegroundColor Yellow
    
    if ($WhatIf) {
        Write-Host " Would create Storage Account: $storageAccountName" -ForegroundColor Cyan
        return $true
    }
    
    try {
        $result = az storage account create `
            --name $storageAccountName `
            --resource-group $resourceGroupName `
            --location $Location `
            --sku Standard_LRS `
            --kind StorageV2 `
            --access-tier Hot `
            --output json | ConvertFrom-Json
            
        Write-Host " Storage Account created: $($result.name)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Error " Failed to create Storage Account: $_"
        return $false
    }
}

function New-ApplicationInsights {
    Write-Host " Creating Application Insights: $appInsightsName" -ForegroundColor Yellow
    
    if ($WhatIf) {
        Write-Host " Would create Application Insights: $appInsightsName" -ForegroundColor Cyan
        return $true
    }
    
    try {
        $result = az monitor app-insights component create `
            --app $appInsightsName `
            --location $Location `
            --resource-group $resourceGroupName `
            --application-type web `
            --output json | ConvertFrom-Json
            
        Write-Host " Application Insights created: $($result.name)" -ForegroundColor Green
        Write-Host "🔑 Instrumentation Key: $($result.instrumentationKey)" -ForegroundColor Cyan
        return $true
    }
    catch {
        Write-Error " Failed to create Application Insights: $_"
        return $false
    }
}

function New-FunctionApp {
    Write-Host " Creating Function App: $functionAppName" -ForegroundColor Yellow
    
    if ($WhatIf) {
        Write-Host " Would create Function App: $functionAppName" -ForegroundColor Cyan
        return $true
    }
    
    try {
        $result = az functionapp create `
            --resource-group $resourceGroupName `
            --consumption-plan-location $Location `
            --runtime python `
            --runtime-version 3.11 `
            --functions-version 4 `
            --name $functionAppName `
            --storage-account $storageAccountName `
            --app-insights $appInsightsName `
            --output json | ConvertFrom-Json
            
        Write-Host " Function App created: $($result.name)" -ForegroundColor Green
        Write-Host " Default Hostname: $($result.defaultHostName)" -ForegroundColor Cyan
        return $true
    }
    catch {
        Write-Error " Failed to create Function App: $_"
        return $false
    }
}

# Execute deployment
$deploymentResults = @{}

Write-Host " Starting QA Environment Deployment..." -ForegroundColor Green
Write-Host ""

# Step 1: Resource Group
$deploymentResults["ResourceGroup"] = New-ResourceGroup

# Step 2: Key Vault
if ($deploymentResults["ResourceGroup"]) {
    $deploymentResults["KeyVault"] = New-KeyVault
} else {
    Write-Host "⏭️ Skipping Key Vault due to Resource Group failure" -ForegroundColor Yellow
    $deploymentResults["KeyVault"] = $false
}

# Step 3: Storage Account (needed for Function App)
if ($deploymentResults["ResourceGroup"]) {
    $deploymentResults["StorageAccount"] = New-StorageAccount
} else {
    Write-Host "⏭️ Skipping Storage Account due to Resource Group failure" -ForegroundColor Yellow
    $deploymentResults["StorageAccount"] = $false
}

# Step 4: Application Insights
if ($deploymentResults["ResourceGroup"]) {
    $deploymentResults["ApplicationInsights"] = New-ApplicationInsights
} else {
    Write-Host "⏭️ Skipping Application Insights due to Resource Group failure" -ForegroundColor Yellow
    $deploymentResults["ApplicationInsights"] = $false
}

# Step 5: Cosmos DB
if ($deploymentResults["ResourceGroup"]) {
    $deploymentResults["CosmosDb"] = New-CosmosDb
} else {
    Write-Host "⏭️ Skipping Cosmos DB due to Resource Group failure" -ForegroundColor Yellow
    $deploymentResults["CosmosDb"] = $false
}

# Step 6: Function App (depends on Storage and App Insights)
if ($deploymentResults["ResourceGroup"] -and $deploymentResults["StorageAccount"] -and $deploymentResults["ApplicationInsights"]) {
    $deploymentResults["FunctionApp"] = New-FunctionApp
} else {
    Write-Host "⏭️ Skipping Function App due to dependency failures" -ForegroundColor Yellow
    $deploymentResults["FunctionApp"] = $false
}

# Deployment Summary
Write-Host ""
Write-Host " QA Environment Deployment Summary" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

$successCount = 0
$totalCount = $deploymentResults.Count

foreach ($resource in $deploymentResults.GetEnumerator()) {
    $status = if ($resource.Value) { " Success" } else { " Failed" }
    $color = if ($resource.Value) { "Green" } else { "Red" }
    
    Write-Host "$($resource.Key): $status" -ForegroundColor $color
    
    if ($resource.Value) { $successCount++ }
}

Write-Host ""
Write-Host "Success Rate: $successCount/$totalCount ($([math]::Round(($successCount/$totalCount)*100, 1))%)" -ForegroundColor Cyan

if ($successCount -eq $totalCount) {
    Write-Host ""
    Write-Host " QA Environment Deployment Completed Successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 Resource Group: $resourceGroupName" -ForegroundColor Cyan
    Write-Host "🔗 Location: $Location" -ForegroundColor Cyan
    Write-Host " Estimated Monthly Cost: ~$50-100 (QA tier)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host " Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Configure Key Vault access policies" -ForegroundColor White
    Write-Host "2. Add environment secrets to Key Vault" -ForegroundColor White
    Write-Host "3. Deploy application code to Function App" -ForegroundColor White
    Write-Host "4. Set up monitoring and alerts" -ForegroundColor White
    Write-Host "5. Run integration tests" -ForegroundColor White
} else {
    Write-Host ""
    Write-Warning " Some resources failed to deploy. Check the errors above and retry failed components."
    exit 1
}