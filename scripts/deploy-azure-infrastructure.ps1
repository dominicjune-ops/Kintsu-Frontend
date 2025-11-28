#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Deploy CareerCoach.ai Job Scraping Framework to Azure

.DESCRIPTION
    This script deploys the complete job scraping framework including:
    - Azure Functions for orchestration
    - Storage accounts for data and queues
    - Cosmos DB for job storage
    - Application Insights for monitoring
    - Key Vault for secrets management

.PARAMETER ResourceGroupName
    Name of the Azure resource group to deploy to

.PARAMETER Location
    Azure region for deployment (default: East US)

.PARAMETER Environment
    Environment name (dev, staging, prod)

.EXAMPLE
    .\deploy-azure-infrastructure.ps1 -ResourceGroupName "rg-careercoach-dev" -Environment "dev"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "East US",
    
    [Parameter(Mandatory=$true)]
    [string]$Environment,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipInfrastructure = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipFunctionDeployment = $false
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Configuration
$appName = "careercoach-scraping"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$deploymentName = "$appName-$Environment-$timestamp"

Write-Host " Starting CareerCoach.ai Job Scraping Framework deployment..." -ForegroundColor Green
Write-Host "Resource Group: $ResourceGroupName" -ForegroundColor Yellow
Write-Host "Location: $Location" -ForegroundColor Yellow
Write-Host "Environment: $Environment" -ForegroundColor Yellow

# Function to check if Azure CLI is installed and logged in
function Test-AzureCLI {
    try {
        $account = az account show --output json 2>$null | ConvertFrom-Json
        if (-not $account) {
            throw "Not logged in"
        }
        Write-Host " Azure CLI authenticated as: $($account.user.name)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host " Azure CLI not installed or not logged in" -ForegroundColor Red
        Write-Host "Please run: az login" -ForegroundColor Yellow
        return $false
    }
}

# Function to create resource group if it doesn't exist
function New-ResourceGroupIfNotExists {
    param($Name, $Location)
    
    $rg = az group show --name $Name --output json 2>$null | ConvertFrom-Json
    if (-not $rg) {
        Write-Host "📦 Creating resource group: $Name" -ForegroundColor Blue
        az group create --name $Name --location $Location --output none
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create resource group"
        }
        Write-Host " Resource group created successfully" -ForegroundColor Green
    } else {
        Write-Host " Resource group already exists" -ForegroundColor Green
    }
}

# Function to deploy Bicep template
function Deploy-Infrastructure {
    param($ResourceGroupName, $TemplateFile, $ParametersFile)
    
    Write-Host "  Deploying Azure infrastructure..." -ForegroundColor Blue
    
    $deployResult = az deployment group create `
        --resource-group $ResourceGroupName `
        --template-file $TemplateFile `
        --parameters $ParametersFile `
        --parameters environment=$Environment `
        --name $deploymentName `
        --output json
    
    if ($LASTEXITCODE -ne 0) {
        throw "Infrastructure deployment failed"
    }
    
    $deployment = $deployResult | ConvertFrom-Json
    Write-Host " Infrastructure deployed successfully" -ForegroundColor Green
    
    return $deployment
}

# Function to deploy Azure Functions
function Deploy-Functions {
    param($ResourceGroupName, $FunctionAppName)
    
    Write-Host " Deploying Azure Functions..." -ForegroundColor Blue
    
    # Build the function app
    Write-Host "📦 Building function app..." -ForegroundColor Blue
    
    # Install Python dependencies
    if (Test-Path "requirements-azure.txt") {
        python -m pip install -r requirements-azure.txt --target .python_packages/lib/site-packages
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install Python dependencies"
        }
    }
    
    # Deploy to Azure Functions
    func azure functionapp publish $FunctionAppName --python
    if ($LASTEXITCODE -ne 0) {
        throw "Function deployment failed"
    }
    
    Write-Host " Azure Functions deployed successfully" -ForegroundColor Green
}

# Function to configure application settings
function Set-ApplicationSettings {
    param($ResourceGroupName, $FunctionAppName, $Settings)
    
    Write-Host "⚙️  Configuring application settings..." -ForegroundColor Blue
    
    foreach ($setting in $Settings.GetEnumerator()) {
        az functionapp config appsettings set `
            --resource-group $ResourceGroupName `
            --name $FunctionAppName `
            --settings "$($setting.Key)=$($setting.Value)" `
            --output none
        
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Failed to set setting: $($setting.Key)"
        }
    }
    
    Write-Host " Application settings configured" -ForegroundColor Green
}

# Function to setup monitoring
function Setup-Monitoring {
    param($ResourceGroupName, $FunctionAppName, $AppInsightsName)
    
    Write-Host " Setting up monitoring and alerts..." -ForegroundColor Blue
    
    # Get Application Insights instrumentation key
    $appInsights = az monitor app-insights component show `
        --app $AppInsightsName `
        --resource-group $ResourceGroupName `
        --output json | ConvertFrom-Json
    
    if (-not $appInsights) {
        throw "Application Insights not found"
    }
    
    # Create alert rules
    $alertRules = @(
        @{
            name = "High Error Rate"
            description = "Alert when error rate exceeds 10%"
            condition = "exceptions/count > 10"
            severity = 2
        },
        @{
            name = "Low Job Count"
            description = "Alert when no jobs are scraped in 1 hour"
            condition = "customMetrics/scraping_jobs_scraped_total < 1"
            severity = 1
        },
        @{
            name = "Function App Down"
            description = "Alert when function app is down"
            condition = "availabilityResults/count < 1"
            severity = 0
        }
    )
    
    foreach ($rule in $alertRules) {
        try {
            az monitor metrics alert create `
                --name $rule.name `
                --resource-group $ResourceGroupName `
                --description $rule.description `
                --severity $rule.severity `
                --condition $rule.condition `
                --scopes "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$ResourceGroupName/providers/Microsoft.Web/sites/$FunctionAppName" `
                --output none
        }
        catch {
            Write-Warning "Failed to create alert rule: $($rule.name)"
        }
    }
    
    Write-Host " Monitoring and alerts configured" -ForegroundColor Green
}

# Function to run post-deployment tests
function Test-Deployment {
    param($FunctionAppName, $ResourceGroupName)
    
    Write-Host " Running post-deployment tests..." -ForegroundColor Blue
    
    # Get function app URL
    $functionApp = az functionapp show `
        --name $FunctionAppName `
        --resource-group $ResourceGroupName `
        --output json | ConvertFrom-Json
    
    $baseUrl = "https://$($functionApp.defaultHostName)"
    
    # Test health endpoint (if exists)
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/api/health" -Method GET -TimeoutSec 30
        Write-Host " Health check passed" -ForegroundColor Green
    }
    catch {
        Write-Warning "Health check endpoint not available or failed"
    }
    
    # Test scraping status endpoint
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/api/scraping_status" -Method GET -TimeoutSec 30
        Write-Host " Scraping status endpoint accessible" -ForegroundColor Green
    }
    catch {
        Write-Warning "Scraping status endpoint not accessible"
    }
    
    Write-Host " Basic deployment tests completed" -ForegroundColor Green
}

# Main deployment flow
try {
    # Validate prerequisites
    if (-not (Test-AzureCLI)) {
        exit 1
    }
    
    # Check if Azure Functions Core Tools is installed
    try {
        func --version | Out-Null
        Write-Host " Azure Functions Core Tools found" -ForegroundColor Green
    }
    catch {
        Write-Host " Azure Functions Core Tools not found" -ForegroundColor Red
        Write-Host "Please install: npm install -g azure-functions-core-tools@4 --unsafe-perm true" -ForegroundColor Yellow
        exit 1
    }
    
    # Create resource group
    New-ResourceGroupIfNotExists -Name $ResourceGroupName -Location $Location
    
    # Deploy infrastructure
    if (-not $SkipInfrastructure) {
        if (Test-Path "infrastructure/main.bicep") {
            $deployment = Deploy-Infrastructure -ResourceGroupName $ResourceGroupName -TemplateFile "infrastructure/main.bicep" -ParametersFile "infrastructure/parameters-$Environment.json"
            
            # Extract outputs
            $outputs = $deployment.properties.outputs
            $functionAppName = $outputs.functionAppName.value
            $storageAccountName = $outputs.storageAccountName.value
            $cosmosAccountName = $outputs.cosmosAccountName.value
            $appInsightsName = $outputs.appInsightsName.value
        } else {
            throw "Bicep template not found: infrastructure/main.bicep"
        }
    } else {
        # If skipping infrastructure, we need to get resource names
        $functionAppName = "$appName-func-$Environment"
        $storageAccountName = "$appName$Environment"
        $cosmosAccountName = "$appName-cosmos-$Environment"
        $appInsightsName = "$appName-ai-$Environment"
    }
    
    Write-Host " Deployment Resources:" -ForegroundColor Cyan
    Write-Host "  Function App: $functionAppName" -ForegroundColor White
    Write-Host "  Storage Account: $storageAccountName" -ForegroundColor White
    Write-Host "  Cosmos DB: $cosmosAccountName" -ForegroundColor White
    Write-Host "  Application Insights: $appInsightsName" -ForegroundColor White
    
    # Get connection strings and keys
    $storageConnectionString = az storage account show-connection-string `
        --name $storageAccountName `
        --resource-group $ResourceGroupName `
        --query connectionString `
        --output tsv
    
    $cosmosConnectionString = az cosmosdb keys list `
        --name $cosmosAccountName `
        --resource-group $ResourceGroupName `
        --type connection-strings `
        --query "connectionStrings[0].connectionString" `
        --output tsv
    
    $appInsightsKey = az monitor app-insights component show `
        --app $appInsightsName `
        --resource-group $ResourceGroupName `
        --query instrumentationKey `
        --output tsv
    
    # Configure application settings
    $appSettings = @{
        "AzureWebJobsStorage" = $storageConnectionString
        "CosmosDBConnectionString" = $cosmosConnectionString
        "APPLICATIONINSIGHTS_CONNECTION_STRING" = "InstrumentationKey=$appInsightsKey"
        "ENVIRONMENT" = $Environment
        "WEBSITE_RUN_FROM_PACKAGE" = "1"
        "FUNCTIONS_WORKER_RUNTIME" = "python"
        "FUNCTIONS_EXTENSION_VERSION" = "~4"
    }
    
    Set-ApplicationSettings -ResourceGroupName $ResourceGroupName -FunctionAppName $functionAppName -Settings $appSettings
    
    # Deploy functions
    if (-not $SkipFunctionDeployment) {
        Deploy-Functions -ResourceGroupName $ResourceGroupName -FunctionAppName $functionAppName
    }
    
    # Setup monitoring
    Setup-Monitoring -ResourceGroupName $ResourceGroupName -FunctionAppName $functionAppName -AppInsightsName $appInsightsName
    
    # Run tests
    Test-Deployment -FunctionAppName $functionAppName -ResourceGroupName $ResourceGroupName
    
    Write-Host ""
    Write-Host " Deployment completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host " Resources created:" -ForegroundColor Cyan
    Write-Host "  Resource Group: $ResourceGroupName" -ForegroundColor White
    Write-Host "  Function App: https://$functionAppName.azurewebsites.net" -ForegroundColor White
    Write-Host "  Application Insights: https://portal.azure.com/#resource/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$ResourceGroupName/providers/Microsoft.Insights/components/$appInsightsName" -ForegroundColor White
    Write-Host ""
    Write-Host " Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Configure scraping sources in the Function App" -ForegroundColor White
    Write-Host "  2. Set up scheduled triggers for automatic scraping" -ForegroundColor White
    Write-Host "  3. Monitor the Application Insights dashboard" -ForegroundColor White
    Write-Host "  4. Test the scraping endpoints" -ForegroundColor White
    Write-Host ""
    
}
catch {
    Write-Host ""
    Write-Host " Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host " Troubleshooting tips:" -ForegroundColor Yellow
    Write-Host "  1. Check Azure CLI login: az account show" -ForegroundColor White
    Write-Host "  2. Verify resource group permissions" -ForegroundColor White
    Write-Host "  3. Check Azure Functions Core Tools: func --version" -ForegroundColor White
    Write-Host "  4. Review deployment logs in Azure Portal" -ForegroundColor White
    Write-Host ""
    exit 1
}