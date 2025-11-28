# 📦 Azure Artifacts Setup Script
# PowerShell script to configure Azure Artifacts for CareerCoach.ai

param(
    [Parameter(Mandatory=$true)]
    [string]$PAT,
    
    [Parameter(Mandatory=$false)]
    [string]$FeedName = "careercoach-packages",
    
    [Parameter(Mandatory=$false)]
    [string]$Organization = "CareerCoachai",
    
    [Parameter(Mandatory=$false)]
    [string]$Project = "CareerCoach.ai"
)

Write-Host "`n🎁 Azure Artifacts Setup for CareerCoach.ai" -ForegroundColor Cyan
Write-Host "=" -Repeat 60 -ForegroundColor Cyan

# Construct feed URLs
$pypiUrl = "https://pkgs.dev.azure.com/$Organization/$Project/_packaging/$FeedName/pypi/simple/"
$npmUrl = "https://pkgs.dev.azure.com/$Organization/$Project/_packaging/$FeedName/npm/registry/"

Write-Host "`n Configuration:" -ForegroundColor Yellow
Write-Host "   Organization: $Organization"
Write-Host "   Project: $Project"
Write-Host "   Feed: $FeedName"
Write-Host "   PyPI URL: $pypiUrl"
Write-Host "   npm URL: $npmUrl"

# Step 1: Install Azure Artifacts keyring for Python
Write-Host "`n🐍 Step 1: Installing Azure Artifacts keyring..." -ForegroundColor Green
try {
    python -m pip install --upgrade keyring artifacts-keyring --quiet
    Write-Host "    Azure Artifacts keyring installed" -ForegroundColor Green
} catch {
    Write-Host "     Warning: Could not install keyring. Manual authentication may be needed." -ForegroundColor Yellow
}

# Step 2: Create pip.conf
Write-Host "`n Step 2: Creating pip.conf..." -ForegroundColor Green
$pipConfig = @"
[global]
# Azure Artifacts feed for CareerCoach.ai
index-url = $pypiUrl
extra-index-url = https://pypi.org/simple

[install]
trusted-host = pkgs.dev.azure.com
"@

$pipConfig | Out-File -FilePath "pip.conf" -Encoding UTF8
Write-Host "    pip.conf created" -ForegroundColor Green

# Step 3: Create .npmrc
Write-Host "`n Step 3: Creating .npmrc..." -ForegroundColor Green
$npmConfig = @"
registry=$npmUrl
always-auth=true
"@

$npmConfig | Out-File -FilePath ".npmrc" -Encoding UTF8
Write-Host "    .npmrc created" -ForegroundColor Green

# Step 4: Update .gitignore
Write-Host "`n Step 4: Updating .gitignore..." -ForegroundColor Green
$gitignoreEntries = @"

# Azure Artifacts credentials
pip.conf
.npmrc
.pypirc
.artifacts-credprovider/
"@

if (Test-Path ".gitignore") {
    Add-Content -Path ".gitignore" -Value $gitignoreEntries
    Write-Host "    .gitignore updated" -ForegroundColor Green
} else {
    $gitignoreEntries | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "    .gitignore created" -ForegroundColor Green
}

# Step 5: Test pip connection
Write-Host "`n Step 5: Testing pip connection..." -ForegroundColor Green
try {
    $env:PIP_INDEX_URL = $pypiUrl
    python -m pip list --format=freeze | Select-Object -First 1 | Out-Null
    Write-Host "    pip connection successful" -ForegroundColor Green
} catch {
    Write-Host "     Warning: Could not test pip connection" -ForegroundColor Yellow
}

# Step 6: Display next steps
Write-Host "`n Setup Complete!" -ForegroundColor Green
Write-Host "`n Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Create feed in Azure DevOps:" -ForegroundColor White
Write-Host "      https://dev.azure.com/$Organization/_artifacts" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Configure feed settings:" -ForegroundColor White
Write-Host "      - Name: $FeedName" -ForegroundColor Gray
Write-Host "      - Visibility: Organization" -ForegroundColor Gray
Write-Host "      - Upstream sources:  PyPI,  npmjs" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. Install packages:" -ForegroundColor White
Write-Host "      pip install -r requirements.txt" -ForegroundColor Gray
Write-Host ""
Write-Host "   4. (Optional) Install npm packages:" -ForegroundColor White
Write-Host "      npm install" -ForegroundColor Gray

Write-Host "`n🔗 Useful Links:" -ForegroundColor Cyan
Write-Host "   Feed URL: https://dev.azure.com/$Organization/_artifacts/feed/$FeedName" -ForegroundColor Gray
Write-Host "   Documentation: ./AZURE_ARTIFACTS_SETUP.md" -ForegroundColor Gray

Write-Host "`n Azure Artifacts is ready to use!" -ForegroundColor Green
Write-Host "=" -Repeat 60 -ForegroundColor Cyan
