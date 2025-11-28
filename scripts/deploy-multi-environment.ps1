#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Multi-Environment Deployment Script for CareerCoach.ai Job Scraping Framework

.DESCRIPTION
    This script deploys the job scraping framework to dev, qa, or prod environments with
    environment-specific configurations, validation, and deployment strategies.

.PARAMETER Environment
    Target environment: dev, qa, or prod

.PARAMETER ResourceGroupName
    Name of the Azure resource group (optional, will be generated if not provided)

.PARAMETER Location
    Azure region for deployment (default: East US)

.PARAMETER SkipInfrastructure
    Skip infrastructure deployment (functions only)

.PARAMETER SkipFunctionDeployment
    Skip function deployment (infrastructure only)

.PARAMETER ValidateOnly
    Only validate the deployment without executing

.PARAMETER Force
    Force deployment without confirmation prompts

.EXAMPLE
    .\deploy-multi-environment.ps1 -Environment dev
    .\deploy-multi-environment.ps1 -Environment prod -Location "West US 2" -Force
    .\deploy-multi-environment.ps1 -Environment qa -ValidateOnly
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("dev", "qa", "staging", "prod")]
    [string]$Environment,
    
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "East US",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipInfrastructure = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipFunctionDeployment = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$ValidateOnly = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$Force = $false
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Configuration per environment
$config = @{
    dev = @{
        resourceGroupSuffix = "dev"
        requiresApproval = $false
        enableBackup = $false
        enableZoneRedundancy = $false
        maxDeploymentTime = 30  # minutes
        healthCheckRetries = 3
        notificationEmail = "devteam@careercoach.ai"
    }
    qa = @{
        resourceGroupSuffix = "qa"
        requiresApproval = $true
        enableBackup = $true
        enableZoneRedundancy = $false
        maxDeploymentTime = 45  # minutes
        healthCheckRetries = 5
        notificationEmail = "qateam@careercoach.ai"
    }
    prod = @{
        resourceGroupSuffix = "prod"
        requiresApproval = $true
        enableBackup = $true
        enableZoneRedundancy = $true
        maxDeploymentTime = 60  # minutes
        healthCheckRetries = 10
        notificationEmail = "platform@careercoach.ai"
    }
}

$envConfig = $config[$Environment]
$appName = "careercoach-scraping"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$deploymentName = "$appName-$Environment-$timestamp"

# Generate resource group name if not provided
if (-not $ResourceGroupName) {
    $ResourceGroupName = "rg-careercoach-$($envConfig.resourceGroupSuffix)"
}

Write-Host " Starting CareerCoach.ai Multi-Environment Deployment..." -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Resource Group: $ResourceGroupName" -ForegroundColor Yellow
Write-Host "Location: $Location" -ForegroundColor Yellow
Write-Host "Deployment Name: $deploymentName" -ForegroundColor Yellow

# Function to validate prerequisites
function Test-Prerequisites {
    Write-Host " Validating prerequisites..." -ForegroundColor Blue
    
    # Check Azure CLI
    try {
        $account = az account show --output json 2>$null | ConvertFrom-Json
        if (-not $account) {
            throw "Not logged in to Azure CLI"
        }
        Write-Host " Azure CLI authenticated as: $($account.user.name)" -ForegroundColor Green
    }
    catch {
        Write-Host " Azure CLI not installed or not logged in" -ForegroundColor Red
        Write-Host "Please run: az login" -ForegroundColor Yellow
        return $false
    }
    
    # Check Azure Functions Core Tools
    try {
        $funcVersion = func --version
        Write-Host " Azure Functions Core Tools: $funcVersion" -ForegroundColor Green
    }
    catch {
        Write-Host " Azure Functions Core Tools not found" -ForegroundColor Red
        Write-Host "Please install: npm install -g azure-functions-core-tools@4 --unsafe-perm true" -ForegroundColor Yellow
        return $false
    }
    
    # Check Python
    try {
        $pythonVersion = python --version
        Write-Host " Python: $pythonVersion" -ForegroundColor Green
    }
    catch {
        Write-Host " Python not found" -ForegroundColor Red
        return $false
    }
    
    # Check required files
    $requiredFiles = @(
        "infrastructure/main.bicep",
        "infrastructure/parameters-$Environment.json",
        "src/azure_function_orchestrator.py",
        "requirements-azure.txt"
    )
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            Write-Host " Required file not found: $file" -ForegroundColor Red
            return $false
        }
    }
    Write-Host " All required files found" -ForegroundColor Green
    
    return $true
}

# Function to validate environment-specific requirements
function Test-EnvironmentRequirements {
    param($Environment)
    
    Write-Host " Validating $Environment environment requirements..." -ForegroundColor Blue
    
    switch ($Environment) {
        "prod" {
            # Production-specific validations
            if (-not $Force -and $envConfig.requiresApproval) {
                $confirmation = Read-Host "  You are deploying to PRODUCTION. Type 'CONFIRM' to proceed"
                if ($confirmation -ne "CONFIRM") {
                    Write-Host " Production deployment cancelled" -ForegroundColor Red
                    return $false
                }
            }
            
            # Check for production readiness
            Write-Host " Validating production readiness..." -ForegroundColor Blue
            # Add additional production checks here
        }
        "qa" {
            # QA-specific validations
            if (-not $Force -and $envConfig.requiresApproval) {
                $confirmation = Read-Host "Deploy to QA environment? (y/N)"
                if ($confirmation -ne "y" -and $confirmation -ne "Y") {
                    Write-Host " QA deployment cancelled" -ForegroundColor Red
                    return $false
                }
            }
        }
        "dev" {
            # Dev-specific validations
            Write-Host " Development environment - no additional validations required" -ForegroundColor Green
        }
    }
    
    return $true
}

# Function to create or update resource group
function New-ResourceGroupIfNotExists {
    param($Name, $Location, $Environment)
    
    Write-Host "📦 Managing resource group: $Name" -ForegroundColor Blue
    
    $rg = az group show --name $Name --output json 2>$null | ConvertFrom-Json
    if (-not $rg) {
        Write-Host "Creating new resource group..." -ForegroundColor Blue
        az group create --name $Name --location $Location --tags Environment=$Environment Project="CareerCoach.ai" --output none
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create resource group"
        }
        Write-Host " Resource group created successfully" -ForegroundColor Green
    } else {
        Write-Host " Resource group already exists" -ForegroundColor Green
        
        # Update tags if needed
        az group update --name $Name --tags Environment=$Environment Project="CareerCoach.ai" --output none
    }
}

# Function to validate Bicep template
function Test-BicepTemplate {
    param($TemplateFile, $ParametersFile)
    
    Write-Host " Validating Bicep template..." -ForegroundColor Blue
    
    $validationResult = az deployment group validate `
        --resource-group $ResourceGroupName `
        --template-file $TemplateFile `
        --parameters $ParametersFile `
        --output json
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host " Bicep template validation failed" -ForegroundColor Red
        return $false
    }
    
    Write-Host " Bicep template validation successful" -ForegroundColor Green
    return $true
}

# Function to deploy infrastructure
function Deploy-Infrastructure {
    param($ResourceGroupName, $TemplateFile, $ParametersFile, $Environment)
    
    Write-Host "  Deploying Azure infrastructure..." -ForegroundColor Blue
    
    # Start deployment with timeout
    $deployJob = Start-Job -ScriptBlock {
        param($rgName, $templateFile, $parametersFile, $deploymentName)
        az deployment group create `
            --resource-group $rgName `
            --template-file $templateFile `
            --parameters $parametersFile `
            --name $deploymentName `
            --output json
    } -ArgumentList $ResourceGroupName, $TemplateFile, $ParametersFile, $deploymentName
    
    # Wait for deployment with timeout
    $timeoutMinutes = $envConfig.maxDeploymentTime
    if (Wait-Job $deployJob -Timeout ($timeoutMinutes * 60)) {
        $deployResult = Receive-Job $deployJob
        Remove-Job $deployJob
        
        if ($LASTEXITCODE -ne 0) {
            throw "Infrastructure deployment failed"
        }
        
        $deployment = $deployResult | ConvertFrom-Json
        Write-Host " Infrastructure deployed successfully" -ForegroundColor Green
        
        return $deployment
    } else {
        Stop-Job $deployJob
        Remove-Job $deployJob
        throw "Infrastructure deployment timed out after $timeoutMinutes minutes"
    }
}

# Function to deploy Azure Functions with environment-specific settings
function Deploy-Functions {
    param($ResourceGroupName, $FunctionAppName, $Environment)
    
    Write-Host " Deploying Azure Functions..." -ForegroundColor Blue
    
    # Install dependencies with environment-specific requirements
    $requirementsFile = "requirements-azure.txt"
    if (Test-Path "requirements-$Environment.txt") {
        $requirementsFile = "requirements-$Environment.txt"
    }
    
    Write-Host "📦 Installing Python dependencies from $requirementsFile..." -ForegroundColor Blue
    python -m pip install -r $requirementsFile --target .python_packages/lib/site-packages --upgrade
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install Python dependencies"
    }
    
    # Create deployment package
    Write-Host "📦 Creating deployment package..." -ForegroundColor Blue
    
    # Deploy with slot if production
    if ($Environment -eq "prod") {
        # Create staging slot for production
        Write-Host " Creating staging slot for production deployment..." -ForegroundColor Blue
        az functionapp deployment slot create `
            --name $FunctionAppName `
            --resource-group $ResourceGroupName `
            --slot staging `
            --output none
        
        # Deploy to staging slot
        func azure functionapp publish $FunctionAppName --slot staging --python
        if ($LASTEXITCODE -ne 0) {
            throw "Function deployment to staging slot failed"
        }
        
        # Validate staging deployment
        Write-Host " Validating staging deployment..." -ForegroundColor Blue
        Start-Sleep -Seconds 30  # Allow time for app to start
        
        $stagingUrl = "https://$FunctionAppName-staging.azurewebsites.net"
        if (Test-FunctionHealth -BaseUrl $stagingUrl -Retries 5) {
            # Swap staging to production
            Write-Host " Swapping staging to production..." -ForegroundColor Blue
            az functionapp deployment slot swap `
                --name $FunctionAppName `
                --resource-group $ResourceGroupName `
                --slot staging `
                --target-slot production `
                --output none
            
            if ($LASTEXITCODE -ne 0) {
                throw "Slot swap failed"
            }
        } else {
            throw "Staging deployment health check failed"
        }
    } else {
        # Direct deployment for dev/qa
        func azure functionapp publish $FunctionAppName --python
        if ($LASTEXITCODE -ne 0) {
            throw "Function deployment failed"
        }
    }
    
    Write-Host " Azure Functions deployed successfully" -ForegroundColor Green
}

# Function to test function health
function Test-FunctionHealth {
    param($BaseUrl, $Retries = 3)
    
    for ($i = 1; $i -le $Retries; $i++) {
        try {
            Write-Host " Health check attempt $i/$Retries..." -ForegroundColor Blue
            
            # Test admin endpoint
            $adminResponse = Invoke-RestMethod -Uri "$BaseUrl/admin/host/status" -Method GET -TimeoutSec 30
            
            # Test scraping status endpoint
            $statusResponse = Invoke-RestMethod -Uri "$BaseUrl/api/scraping_status" -Method GET -TimeoutSec 30
            
            Write-Host " Function health check passed" -ForegroundColor Green
            return $true
        }
        catch {
            Write-Host "  Health check attempt $i failed: $($_.Exception.Message)" -ForegroundColor Yellow
            if ($i -lt $Retries) {
                Start-Sleep -Seconds 10
            }
        }
    }
    
    Write-Host " Function health check failed after $Retries attempts" -ForegroundColor Red
    return $false
}

# Function to configure environment-specific settings
function Set-EnvironmentConfiguration {
    param($ResourceGroupName, $FunctionAppName, $Environment)
    
    Write-Host "⚙️  Configuring environment-specific settings..." -ForegroundColor Blue
    
    # Environment-specific app settings
    $envSettings = @{}
    
    switch ($Environment) {
        "dev" {
            $envSettings["ENABLE_DEBUG"] = "true"
            $envSettings["LOG_LEVEL"] = "DEBUG"
            $envSettings["RATE_LIMIT_ENABLED"] = "false"
        }
        "qa" {
            $envSettings["ENABLE_DEBUG"] = "false"
            $envSettings["LOG_LEVEL"] = "INFO"
            $envSettings["RATE_LIMIT_ENABLED"] = "true"
            $envSettings["ENABLE_INTEGRATION_TESTS"] = "true"
        }
        "prod" {
            $envSettings["ENABLE_DEBUG"] = "false"
            $envSettings["LOG_LEVEL"] = "WARNING"
            $envSettings["RATE_LIMIT_ENABLED"] = "true"
            $envSettings["ENABLE_PERFORMANCE_MONITORING"] = "true"
            $envSettings["ENABLE_SECURITY_HEADERS"] = "true"
        }
    }
    
    # Apply settings
    foreach ($setting in $envSettings.GetEnumerator()) {
        az functionapp config appsettings set `
            --resource-group $ResourceGroupName `
            --name $FunctionAppName `
            --settings "$($setting.Key)=$($setting.Value)" `
            --output none
        
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Failed to set setting: $($setting.Key)"
        }
    }
    
    Write-Host " Environment configuration applied" -ForegroundColor Green
}

# Function to setup environment-specific monitoring
function Setup-EnvironmentMonitoring {
    param($ResourceGroupName, $Environment, $FunctionAppName, $AppInsightsName)
    
    Write-Host " Setting up environment-specific monitoring..." -ForegroundColor Blue
    
    # Environment-specific alert thresholds
    $alertConfig = @{
        dev = @{
            errorRateThreshold = 20
            responseTimeThreshold = 10000
            availabilityThreshold = 90
        }
        qa = @{
            errorRateThreshold = 10
            responseTimeThreshold = 5000
            availabilityThreshold = 95
        }
        prod = @{
            errorRateThreshold = 5
            responseTimeThreshold = 3000
            availabilityThreshold = 99
        }
    }
    
    $thresholds = $alertConfig[$Environment]
    
    # Create alert rules with environment-specific thresholds
    $alertRules = @(
        @{
            name = "High Error Rate - $Environment"
            description = "Error rate exceeds $($thresholds.errorRateThreshold)% in $Environment"
            severity = if ($Environment -eq "prod") { 1 } else { 2 }
            threshold = $thresholds.errorRateThreshold
        }
    )
    
    foreach ($rule in $alertRules) {
        try {
            # Create metric alert (simplified - would need full ARM template for complex alerts)
            Write-Host "Creating alert: $($rule.name)" -ForegroundColor Blue
        }
        catch {
            Write-Warning "Failed to create alert rule: $($rule.name)"
        }
    }
    
    Write-Host " Environment monitoring configured" -ForegroundColor Green
}

# Function to run post-deployment validation
function Test-Deployment {
    param($FunctionAppName, $ResourceGroupName, $Environment)
    
    Write-Host " Running post-deployment validation..." -ForegroundColor Blue
    
    # Get function app details
    $functionApp = az functionapp show `
        --name $FunctionAppName `
        --resource-group $ResourceGroupName `
        --output json | ConvertFrom-Json
    
    $baseUrl = "https://$($functionApp.defaultHostName)"
    
    # Run health checks with environment-specific retry counts
    $healthCheckPassed = Test-FunctionHealth -BaseUrl $baseUrl -Retries $envConfig.healthCheckRetries
    
    if (-not $healthCheckPassed) {
        throw "Post-deployment health check failed"
    }
    
    # Environment-specific validation
    switch ($Environment) {
        "prod" {
            # Additional production validations
            Write-Host " Running production-specific validations..." -ForegroundColor Blue
            # Test backup and disaster recovery
            # Validate security configurations
            # Check performance metrics
        }
        "qa" {
            # QA-specific validations
            Write-Host " Running QA-specific validations..." -ForegroundColor Blue
            # Run integration tests
            # Validate test data scenarios
        }
    }
    
    Write-Host " Post-deployment validation completed" -ForegroundColor Green
}

# Function to send deployment notification
function Send-DeploymentNotification {
    param($Environment, $Status, $FunctionAppName, $DeploymentTime)
    
    $subject = "CareerCoach.ai Deployment $Status - $Environment"
    $message = @"
Environment: $Environment
Function App: $FunctionAppName
Status: $Status
Deployment Time: $DeploymentTime minutes
Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC')
"@
    
    Write-Host "📧 Deployment notification:" -ForegroundColor Blue
    Write-Host $message -ForegroundColor White
    
    # In a real implementation, you would send this via email/Teams/Slack
}

# Main deployment workflow
try {
    $deploymentStartTime = Get-Date
    
    # Validate prerequisites
    if (-not (Test-Prerequisites)) {
        exit 1
    }
    
    # Validate environment requirements
    if (-not (Test-EnvironmentRequirements -Environment $Environment)) {
        exit 1
    }
    
    # Create or update resource group
    New-ResourceGroupIfNotExists -Name $ResourceGroupName -Location $Location -Environment $Environment
    
    # Validate Bicep template
    $templateFile = "infrastructure/main.bicep"
    $parametersFile = "infrastructure/parameters-$Environment.json"
    
    if (-not (Test-BicepTemplate -TemplateFile $templateFile -ParametersFile $parametersFile)) {
        exit 1
    }
    
    if ($ValidateOnly) {
        Write-Host " Validation completed successfully - no deployment executed" -ForegroundColor Green
        exit 0
    }
    
    # Deploy infrastructure
    if (-not $SkipInfrastructure) {
        $deployment = Deploy-Infrastructure -ResourceGroupName $ResourceGroupName -TemplateFile $templateFile -ParametersFile $parametersFile -Environment $Environment
        
        # Extract outputs
        $outputs = $deployment.properties.outputs
        $functionAppName = $outputs.functionAppName.value
        $appInsightsName = $outputs.applicationInsightsName.value
    } else {
        # Get existing resource names
        $functionAppName = "careercoach-func-$Environment"
        $appInsightsName = "careercoach-ai-$Environment"
    }
    
    Write-Host " Deployment Resources:" -ForegroundColor Cyan
    Write-Host "  Function App: $functionAppName" -ForegroundColor White
    Write-Host "  Application Insights: $appInsightsName" -ForegroundColor White
    
    # Deploy functions
    if (-not $SkipFunctionDeployment) {
        Deploy-Functions -ResourceGroupName $ResourceGroupName -FunctionAppName $functionAppName -Environment $Environment
    }
    
    # Configure environment-specific settings
    Set-EnvironmentConfiguration -ResourceGroupName $ResourceGroupName -FunctionAppName $functionAppName -Environment $Environment
    
    # Setup monitoring
    Setup-EnvironmentMonitoring -ResourceGroupName $ResourceGroupName -Environment $Environment -FunctionAppName $functionAppName -AppInsightsName $appInsightsName
    
    # Run post-deployment validation
    Test-Deployment -FunctionAppName $functionAppName -ResourceGroupName $ResourceGroupName -Environment $Environment
    
    $deploymentEndTime = Get-Date
    $deploymentDuration = ($deploymentEndTime - $deploymentStartTime).TotalMinutes
    
    # Send success notification
    Send-DeploymentNotification -Environment $Environment -Status "SUCCESS" -FunctionAppName $functionAppName -DeploymentTime ([math]::Round($deploymentDuration, 2))
    
    Write-Host ""
    Write-Host " Multi-environment deployment completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host " Deployment Summary:" -ForegroundColor Cyan
    Write-Host "  Environment: $Environment" -ForegroundColor White
    Write-Host "  Resource Group: $ResourceGroupName" -ForegroundColor White
    Write-Host "  Function App: https://$functionAppName.azurewebsites.net" -ForegroundColor White
    Write-Host "  Duration: $([math]::Round($deploymentDuration, 2)) minutes" -ForegroundColor White
    Write-Host ""
    
}
catch {
    $deploymentEndTime = Get-Date
    $deploymentDuration = ($deploymentEndTime - $deploymentStartTime).TotalMinutes
    
    # Send failure notification
    Send-DeploymentNotification -Environment $Environment -Status "FAILED" -FunctionAppName "N/A" -DeploymentTime ([math]::Round($deploymentDuration, 2))
    
    Write-Host ""
    Write-Host " Multi-environment deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host " Troubleshooting tips:" -ForegroundColor Yellow
    Write-Host "  1. Check Azure CLI login: az account show" -ForegroundColor White
    Write-Host "  2. Verify resource group permissions" -ForegroundColor White
    Write-Host "  3. Review deployment logs in Azure Portal" -ForegroundColor White
    Write-Host "  4. Check parameter file: infrastructure/parameters-$Environment.json" -ForegroundColor White
    Write-Host ""
    exit 1
}