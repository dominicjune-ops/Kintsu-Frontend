# Create QA Environment Key Vault
# Run this script after Azure login is complete

Write-Host "🔐 Creating CareerCoach QA Key Vault..." -ForegroundColor Green

# Check if logged in
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
$account = az account show 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error " Not logged into Azure. Please run 'az login' first."
    exit 1
}

Write-Host " Azure login confirmed" -ForegroundColor Green

# Create resource group if it doesn't exist
Write-Host "Creating resource group CareerCoach-QA-RG..." -ForegroundColor Yellow
az group create --name "CareerCoach-QA-RG" --location "westus" --output table

if ($LASTEXITCODE -eq 0) {
    Write-Host " Resource group created/verified" -ForegroundColor Green
} else {
    Write-Error " Failed to create resource group"
    exit 1
}

# Create Key Vault
Write-Host "Creating Key Vault careercoach-qa-kv..." -ForegroundColor Yellow
az keyvault create `
    --name "careercoach-qa-kv" `
    --resource-group "CareerCoach-QA-RG" `
    --location "westus" `
    --output table

if ($LASTEXITCODE -eq 0) {
    Write-Host " Key Vault created successfully!" -ForegroundColor Green
    Write-Host "🔑 Key Vault URL: https://careercoach-qa-kv.vault.azure.net/" -ForegroundColor Cyan
} else {
    Write-Error " Failed to create Key Vault"
    exit 1
}

Write-Host ""
Write-Host " QA Key Vault Setup Complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Set Key Vault access policies" -ForegroundColor White
Write-Host "2. Add secrets for QA environment" -ForegroundColor White
Write-Host "3. Configure application to use Key Vault" -ForegroundColor White