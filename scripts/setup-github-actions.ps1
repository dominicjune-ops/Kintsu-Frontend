# Azure Service Principal Setup for GitHub Actions
# Run this script to create credentials for automated deployment

# Step 1: Get your subscription ID
Write-Host "Getting Azure subscription ID..." -ForegroundColor Cyan
$subscriptionId = "386dfda9-d2e3-411a-9041-87b0d8971f4a"
Write-Host "Using Subscription ID: $subscriptionId" -ForegroundColor Green

# Step 2: Create service principal with contributor role
Write-Host "`nCreating service principal..." -ForegroundColor Cyan
Write-Host "Command to run:" -ForegroundColor Yellow
Write-Host "az ad sp create-for-rbac --name 'careercoach-github-actions' --role contributor --scopes /subscriptions/$subscriptionId/resourceGroups/careercoach-rg --sdk-auth" -ForegroundColor White

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "NEXT STEPS:" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "1. Run the command above in your terminal"
Write-Host "2. Copy the entire JSON output"
Write-Host "3. Go to GitHub: https://github.com/dominicjune-ops/CareerCoach.ai/settings/secrets/actions"
Write-Host "4. Click 'New repository secret'"
Write-Host "5. Name: AZURE_CREDENTIALS"
Write-Host "6. Value: Paste the entire JSON"
Write-Host "7. Click 'Add secret'"
Write-Host "`nOnce done, every push to main will automatically deploy to Azure!" -ForegroundColor Green
