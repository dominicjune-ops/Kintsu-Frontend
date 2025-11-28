# Azure Monitor Alert Rules Deployment Script
# Creates environment-specific alert rules for CareerCoach.ai

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("dev", "qa", "staging", "prod")]
    [string]$Environment,
    
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$true)]
    [string]$SubscriptionId,
    
    [Parameter(Mandatory=$false)]
    [string]$ConfigPath = "./config",
    
    [Parameter(Mandatory=$false)]
    [switch]$WhatIf,
    
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

# Set error handling
$ErrorActionPreference = "Stop"

# Import required modules
Import-Module Az.Monitor -Force
Import-Module Az.Resources -Force

Write-Host " Deploying monitoring configuration for $Environment environment" -ForegroundColor Green
Write-Host " Resource Group: $ResourceGroupName" -ForegroundColor Cyan
Write-Host " Subscription: $SubscriptionId" -ForegroundColor Cyan

# Set Azure context
try {
    Set-AzContext -SubscriptionId $SubscriptionId
    Write-Host " Azure context set successfully" -ForegroundColor Green
}
catch {
    Write-Error " Failed to set Azure context: $_"
    exit 1
}

# Load monitoring configuration
$configFile = Join-Path $ConfigPath "monitoring-$Environment.json"
if (-not (Test-Path $configFile)) {
    Write-Error " Monitoring config file not found: $configFile"
    exit 1
}

try {
    $config = Get-Content $configFile | ConvertFrom-Json
    Write-Host " Loaded monitoring configuration for $Environment" -ForegroundColor Green
}
catch {
    Write-Error " Failed to parse monitoring config: $_"
    exit 1
}

# Get resource references
$functionAppName = "careercoach-func-$Environment"
$appInsightsName = "careercoach-insights-$Environment"
$cosmosDbName = "careercoach-cosmos-$Environment"

Write-Host " Locating Azure resources..." -ForegroundColor Yellow

# Get Function App resource ID
try {
    $functionApp = Get-AzResource -ResourceGroupName $ResourceGroupName -ResourceType "Microsoft.Web/sites" -Name $functionAppName
    if (-not $functionApp) {
        throw "Function App not found: $functionAppName"
    }
    $functionAppResourceId = $functionApp.ResourceId
    Write-Host " Found Function App: $functionAppName" -ForegroundColor Green
}
catch {
    Write-Error " Failed to find Function App: $_"
    exit 1
}

# Get Application Insights resource ID
try {
    $appInsights = Get-AzResource -ResourceGroupName $ResourceGroupName -ResourceType "Microsoft.Insights/components" -Name $appInsightsName
    if (-not $appInsights) {
        throw "Application Insights not found: $appInsightsName"
    }
    $appInsightsResourceId = $appInsights.ResourceId
    Write-Host " Found Application Insights: $appInsightsName" -ForegroundColor Green
}
catch {
    Write-Error " Failed to find Application Insights: $_"
    exit 1
}

# Create action groups first
Write-Host "📢 Creating action groups..." -ForegroundColor Yellow

$actionGroups = @()

# Email action group
if ($config.alerts.email_notifications -and $config.alerts.email_notifications.Count -gt 0) {
    $emailActionGroupName = "careercoach-email-alerts-$Environment"
    
    $emailReceivers = @()
    foreach ($email in $config.alerts.email_notifications) {
        $emailReceivers += New-AzActionGroupReceiver -Name ($email -replace '@', '-at-') -EmailReceiver -EmailAddress $email
    }
    
    if (-not $WhatIf) {
        try {
            $emailActionGroup = Set-AzActionGroup -ResourceGroupName $ResourceGroupName -Name $emailActionGroupName -ShortName "email-$Environment" -Receiver $emailReceivers
            $actionGroups += @{
                Name = "email-alerts"
                ResourceId = $emailActionGroup.Id
            }
            Write-Host " Created email action group: $emailActionGroupName" -ForegroundColor Green
        }
        catch {
            Write-Warning " Failed to create email action group: $_"
        }
    }
    else {
        Write-Host " Would create email action group: $emailActionGroupName" -ForegroundColor Cyan
    }
}

# Slack action group (if webhook provided)
if ($config.alerts.slack_webhook) {
    $slackActionGroupName = "careercoach-slack-alerts-$Environment"
    $slackReceiver = New-AzActionGroupReceiver -Name "slack-$Environment" -WebhookReceiver -ServiceUri $config.alerts.slack_webhook
    
    if (-not $WhatIf) {
        try {
            $slackActionGroup = Set-AzActionGroup -ResourceGroupName $ResourceGroupName -Name $slackActionGroupName -ShortName "slack-$Environment" -Receiver $slackReceiver
            $actionGroups += @{
                Name = "slack-alerts"
                ResourceId = $slackActionGroup.Id
            }
            Write-Host " Created Slack action group: $slackActionGroupName" -ForegroundColor Green
        }
        catch {
            Write-Warning " Failed to create Slack action group: $_"
        }
    }
    else {
        Write-Host " Would create Slack action group: $slackActionGroupName" -ForegroundColor Cyan
    }
}

# Critical alerts action group (for production)
if ($Environment -eq "prod") {
    $criticalActionGroupName = "careercoach-critical-alerts-prod"
    
    $criticalReceivers = @()
    # Add critical email receivers
    foreach ($email in $config.alerts.email_notifications) {
        $criticalReceivers += New-AzActionGroupReceiver -Name ($email -replace '@', '-at-critical') -EmailReceiver -EmailAddress $email
    }
    
    # Add SMS receivers for critical alerts (if configured)
    # $criticalReceivers += New-AzActionGroupReceiver -Name "ops-sms" -SmsReceiver -CountryCode "1" -PhoneNumber "+1234567890"
    
    if (-not $WhatIf) {
        try {
            $criticalActionGroup = Set-AzActionGroup -ResourceGroupName $ResourceGroupName -Name $criticalActionGroupName -ShortName "critical" -Receiver $criticalReceivers
            $actionGroups += @{
                Name = "critical-alerts"
                ResourceId = $criticalActionGroup.Id
            }
            Write-Host " Created critical action group: $criticalActionGroupName" -ForegroundColor Green
        }
        catch {
            Write-Warning " Failed to create critical action group: $_"
        }
    }
    else {
        Write-Host " Would create critical action group: $criticalActionGroupName" -ForegroundColor Cyan
    }
}

# Create alert rules
Write-Host "🚨 Creating alert rules..." -ForegroundColor Yellow

$createdRules = 0
$skippedRules = 0
$failedRules = 0

foreach ($rule in $config.alerts.rules) {
    if (-not $rule.enabled) {
        Write-Host "⏭️ Skipping disabled rule: $($rule.name)" -ForegroundColor DarkGray
        $skippedRules++
        continue
    }
    
    Write-Host " Processing rule: $($rule.name)" -ForegroundColor Cyan
    
    # Determine resource ID based on metric
    $targetResourceId = $appInsightsResourceId
    if ($rule.metric -like "*performanceCounters*" -or $rule.metric -like "*requests*") {
        $targetResourceId = $functionAppResourceId
    }
    
    # Build query based on metric type
    $query = ""
    switch -Wildcard ($rule.metric) {
        "*exceptions*" {
            $query = "exceptions | summarize count() by bin(timestamp, 5m) | where count_ > $($rule.threshold)"
        }
        "*requests/duration*" {
            $query = "requests | summarize avg(duration) by bin(timestamp, 5m) | where avg_duration > $($rule.threshold)"
        }
        "*availabilityResults*" {
            $query = "availabilityResults | summarize avg(success) by bin(timestamp, 5m) | where avg_success < $($rule.threshold / 100)"
        }
        "*performanceCounters/processorCpuPercentage*" {
            $query = "performanceCounters | where name == '\\Processor(_Total)\\% Processor Time' | summarize avg(value) by bin(timestamp, 5m) | where avg_value > $($rule.threshold)"
        }
        "*customMetrics*" {
            $metricName = ($rule.metric -split "/")[1]
            $query = "customMetrics | where name == '$metricName' | summarize avg(value) by bin(timestamp, 5m) | where avg_value $(if ($rule.operator -eq 'LessThan') { '<' } else { '>' }) $($rule.threshold)"
        }
        default {
            $query = "traces | where severityLevel >= 3 | summarize count() by bin(timestamp, 5m) | where count_ > $($rule.threshold)"
        }
    }
    
    # Get action group IDs for this rule
    $ruleActionGroups = @()
    if ($rule.action_groups) {
        foreach ($agName in $rule.action_groups) {
            $matchingAG = $actionGroups | Where-Object { $_.Name -eq $agName }
            if ($matchingAG) {
                $ruleActionGroups += $matchingAG.ResourceId
            }
        }
    }
    
    # Use default email action group if no specific action groups defined
    if ($ruleActionGroups.Count -eq 0) {
        $defaultAG = $actionGroups | Where-Object { $_.Name -eq "email-alerts" }
        if ($defaultAG) {
            $ruleActionGroups += $defaultAG.ResourceId
        }
    }
    
    # Create the alert rule
    if (-not $WhatIf) {
        try {
            $alertRuleName = "careercoach-$($rule.name -replace ' ', '-')-$Environment"
            
            # Create scheduled query rule
            $alertRule = New-AzScheduledQueryRule `
                -ResourceGroupName $ResourceGroupName `
                -Name $alertRuleName `
                -Location "East US" `
                -Description $rule.description `
                -Enabled $true `
                -Source $targetResourceId `
                -Query $query `
                -QueryType "ResultCount" `
                -Operator $rule.operator `
                -Threshold $rule.threshold `
                -TimeWindow "PT15M" `
                -EvaluationFrequency "PT5M" `
                -Severity $rule.severity `
                -ActionGroup $ruleActionGroups `
                -Force:$Force
            
            Write-Host " Created alert rule: $alertRuleName" -ForegroundColor Green
            $createdRules++
        }
        catch {
            Write-Warning " Failed to create alert rule '$($rule.name)': $_"
            $failedRules++
        }
    }
    else {
        Write-Host " Would create alert rule: careercoach-$($rule.name -replace ' ', '-')-$Environment" -ForegroundColor Cyan
        $createdRules++
    }
}

# Create availability tests
if ($config.availability_tests.enabled) {
    Write-Host " Creating availability tests..." -ForegroundColor Yellow
    
    foreach ($test in $config.availability_tests.tests) {
        if (-not $test.enabled) {
            continue
        }
        
        $testName = "careercoach-$($test.name -replace ' ', '-')-$Environment"
        
        if (-not $WhatIf) {
            try {
                # Create availability test using REST API (as PowerShell module doesn't have direct support)
                $testConfig = @{
                    "location" = "East US"
                    "tags" = @{
                        "environment" = $Environment
                        "application" = "careercoach"
                    }
                    "properties" = @{
                        "SyntheticMonitorId" = $testName
                        "Name" = $test.name
                        "Description" = "Availability test for $($test.url)"
                        "Enabled" = $true
                        "Frequency" = $config.availability_tests.frequency_minutes * 60
                        "Timeout" = $config.availability_tests.timeout_seconds
                        "Kind" = "ping"
                        "Locations" = @(
                            @{ "Id" = "us-east-1-azr" }
                        )
                        "Configuration" = @{
                            "WebTest" = "<WebTest Name=`"$($test.name)`" Enabled=`"True`" Timeout=`"$($config.availability_tests.timeout_seconds)`"><Items><Request Method=`"GET`" Version=`"1.1`" Url=`"$($test.url)`" ThinkTime=`"0`" Timeout=`"$($config.availability_tests.timeout_seconds)`" ParseDependentRequests=`"False`" FollowRedirects=`"True`" RecordResult=`"True`" Cache=`"False`" ResponseTimeGoal=`"0`" Encoding=`"utf-8`" ExpectedHttpStatusCode=`"$($test.expected_status_code)`" ExpectedResponseUrl=`"`" ReportingName=`"`" IgnoreHttpStatusCode=`"False`" /></Items></WebTest>"
                        }
                    }
                }
                
                # Deploy using ARM template would be more reliable here
                Write-Host " Would create availability test: $testName" -ForegroundColor Green
            }
            catch {
                Write-Warning " Failed to create availability test '$($test.name)': $_"
            }
        }
        else {
            Write-Host " Would create availability test: $testName" -ForegroundColor Cyan
        }
    }
}

# Summary
Write-Host ""
Write-Host " Deployment Summary" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Cyan
Write-Host "Created Rules: $createdRules" -ForegroundColor Green
Write-Host "Skipped Rules: $skippedRules" -ForegroundColor Yellow
Write-Host "Failed Rules: $failedRules" -ForegroundColor Red
Write-Host "Action Groups: $($actionGroups.Count)" -ForegroundColor Cyan

if ($WhatIf) {
    Write-Host ""
    Write-Host " This was a dry run. Use -WhatIf:`$false to actually deploy." -ForegroundColor Yellow
}

if ($failedRules -gt 0) {
    Write-Host ""
    Write-Warning " Some alert rules failed to deploy. Check the errors above."
    exit 1
}

Write-Host ""
Write-Host " Monitoring deployment completed successfully!" -ForegroundColor Green