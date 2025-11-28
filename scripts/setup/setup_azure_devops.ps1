# Azure DevOps Project Setup Script
# Creates Area Paths and Iteration Paths for CareerCoach.ai

Write-Host " CareerCoach.ai Azure DevOps Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Configuration - UPDATE THESE VALUES
$organization = "CareerCoachai"  # e.g., "contoso"
$project = "CareerCoach.ai"
$pat = $env:AZURE_DEVOPS_PAT  # Set via environment variable - Create at https://dev.azure.com/{org}/_usersSettings/tokens

Write-Host "  SETUP REQUIRED:" -ForegroundColor Yellow
Write-Host "1. Update `$organization with your Azure DevOps organization name" -ForegroundColor Yellow
Write-Host "2. Update `$pat with your Personal Access Token" -ForegroundColor Yellow
Write-Host "3. Run this script in PowerShell" -ForegroundColor Yellow
Write-Host ""
Write-Host "To create a PAT: https://dev.azure.com/$organization/_usersSettings/tokens" -ForegroundColor Cyan
Write-Host "Required Scopes: Work Items (Read, Write)" -ForegroundColor Cyan
Write-Host ""

# Check if organization and PAT are configured
if ($organization -eq "YOUR_ORG_NAME" -or $pat -eq "YOUR_PERSONAL_ACCESS_TOKEN") {
    Write-Host " ERROR: Please configure organization and PAT in this script first!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Edit this file and update:" -ForegroundColor Yellow
    Write-Host "  Line 9: `$organization = `"YOUR_ORG_NAME`"" -ForegroundColor Yellow
    Write-Host "  Line 11: `$pat = `"YOUR_PERSONAL_ACCESS_TOKEN`"" -ForegroundColor Yellow
    exit 1
}

# Encode PAT for API calls
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$($pat)"))
$headers = @{
    Authorization = "Basic $base64AuthInfo"
    "Content-Type" = "application/json"
}

$baseUrl = "https://dev.azure.com/$organization/$project"

Write-Host " Project: $project" -ForegroundColor Green
Write-Host "🏢 Organization: $organization" -ForegroundColor Green
Write-Host ""

# Function to create Area Path
function Create-AreaPath {
    param (
        [string]$path
    )
    
    $body = @{
        name = $path
    } | ConvertTo-Json

    try {
        $uri = "$baseUrl/_apis/wit/classificationnodes/areas?api-version=7.0"
        $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
        Write-Host " Created Area Path: $path" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "  Area Path may already exist: $path" -ForegroundColor Yellow
        return $false
    }
}

# Function to create Iteration Path
function Create-IterationPath {
    param (
        [string]$path,
        [datetime]$startDate,
        [datetime]$endDate
    )
    
    $body = @{
        name = $path
        attributes = @{
            startDate = $startDate.ToString("yyyy-MM-dd")
            finishDate = $endDate.ToString("yyyy-MM-dd")
        }
    } | ConvertTo-Json

    try {
        $uri = "$baseUrl/_apis/wit/classificationnodes/iterations?api-version=7.0"
        $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
        Write-Host " Created Iteration: $path ($($startDate.ToString('MM/dd')) - $($endDate.ToString('MM/dd')))" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "  Iteration may already exist: $path" -ForegroundColor Yellow
        return $false
    }
}

# Create Area Paths
Write-Host "📁 Creating Area Paths..." -ForegroundColor Cyan
Write-Host ""

$areaPaths = @(
    "AI-Foundation",
    "AI-Foundation\OpenAI-Integration",
    "AI-Foundation\LangChain-Framework",
    "AI-Foundation\Security-Authentication",
    "AI-Intelligence",
    "AI-Intelligence\Matching-Algorithm",
    "AI-Intelligence\Analytics-Engine",
    "AI-Intelligence\Performance-Monitoring",
    "Content-Intelligence",
    "Content-Intelligence\Framework-Automation",
    "Content-Intelligence\Coaching-Systems",
    "Content-Intelligence\Progress-Tracking",
    "Premium-Features",
    "Premium-Features\Predictive-Modeling",
    "Premium-Features\Advanced-Analytics",
    "Premium-Features\Mobile-Optimization"
)

$areaCount = 0
foreach ($area in $areaPaths) {
    if (Create-AreaPath -path $area) {
        $areaCount++
    }
    Start-Sleep -Milliseconds 200
}

Write-Host ""
Write-Host "📁 Area Paths Created: $areaCount / $($areaPaths.Count)" -ForegroundColor Green
Write-Host ""

# Create Iteration Paths
Write-Host "📅 Creating Iteration Paths..." -ForegroundColor Cyan
Write-Host ""

# Define sprint dates (2-week sprints starting from today)
$today = Get-Date
$sprint1Start = $today
$sprint1End = $sprint1Start.AddDays(13)

$sprint2Start = $sprint1End.AddDays(1)
$sprint2End = $sprint2Start.AddDays(13)

$sprint3Start = $sprint2End.AddDays(1)
$sprint3End = $sprint3Start.AddDays(13)

$sprint4Start = $sprint3End.AddDays(1)
$sprint4End = $sprint4Start.AddDays(13)

$sprint5Start = $sprint4End.AddDays(1)
$sprint5End = $sprint5Start.AddDays(13)

$sprint6Start = $sprint5End.AddDays(1)
$sprint6End = $sprint6Start.AddDays(13)

$sprint7Start = $sprint6End.AddDays(1)
$sprint7End = $sprint7Start.AddDays(13)

$sprint8Start = $sprint7End.AddDays(1)
$sprint8End = $sprint8Start.AddDays(13)

# Create parent iteration
Create-IterationPath -path "2025-Q4-AI-Implementation" -startDate $sprint1Start -endDate $sprint8End
Start-Sleep -Milliseconds 500

# Create sprint iterations
$iterations = @(
    @{ name = "Sprint-1-Foundation-Setup"; start = $sprint1Start; end = $sprint1End }
    @{ name = "Sprint-2-Agent-Architecture"; start = $sprint2Start; end = $sprint2End }
    @{ name = "Sprint-3-Intelligence-Core"; start = $sprint3Start; end = $sprint3End }
    @{ name = "Sprint-4-Analytics-Integration"; start = $sprint4Start; end = $sprint4End }
    @{ name = "Sprint-5-Content-Automation"; start = $sprint5Start; end = $sprint5End }
    @{ name = "Sprint-6-Interactive-Coaching"; start = $sprint6Start; end = $sprint6End }
    @{ name = "Sprint-7-Predictive-Models"; start = $sprint7Start; end = $sprint7End }
    @{ name = "Sprint-8-Premium-Launch"; start = $sprint8Start; end = $sprint8End }
)

$iterationCount = 0
foreach ($iteration in $iterations) {
    if (Create-IterationPath -path $iteration.name -startDate $iteration.start -endDate $iteration.end) {
        $iterationCount++
    }
    Start-Sleep -Milliseconds 200
}

Write-Host ""
Write-Host "📅 Iteration Paths Created: $iterationCount / $($iterations.Count)" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "=================================" -ForegroundColor Cyan
Write-Host " Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host " Summary:" -ForegroundColor Cyan
Write-Host "  • Area Paths: $areaCount created" -ForegroundColor White
Write-Host "  • Iteration Paths: $($iterationCount + 1) created (including parent)" -ForegroundColor White
Write-Host ""
Write-Host " Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Go to: https://dev.azure.com/$organization/$project" -ForegroundColor White
Write-Host "  2. Navigate to: Boards > Queries" -ForegroundColor White
Write-Host "  3. Click: '...' menu > Import Work Items" -ForegroundColor White
Write-Host "  4. Select file: azure_devops_import.csv" -ForegroundColor White
Write-Host "  5. Click: Import" -ForegroundColor White
Write-Host ""
Write-Host "📄 Import file location:" -ForegroundColor Cyan
Write-Host "  $PSScriptRoot\azure_devops_import.csv" -ForegroundColor Yellow
Write-Host ""
Write-Host " Ready to import 28 work items!" -ForegroundColor Green
