$pat = Read-Host "Enter Azure DevOps PAT" -AsSecureString
$env:AZURE_DEVOPS_PAT = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($pat))
$env:AZURE_DEVOPS_ORG = 'CareerCoachai'
$env:AZURE_DEVOPS_PROJECT = 'CareerCoach.ai'

Write-Host '[INFO] Running publish_azure_wiki.ps1 to update the Azure DevOps Wiki'

try {
    & ".\scripts\publish_azure_wiki.ps1"
} catch {
    Write-Host '[ERROR] Publish script failed with exception:'
    Write-Host $_.Exception.Message
} finally {
    Remove-Item Env:AZURE_DEVOPS_PAT -ErrorAction SilentlyContinue
    Remove-Item Env:AZURE_DEVOPS_ORG -ErrorAction SilentlyContinue
    Remove-Item Env:AZURE_DEVOPS_PROJECT -ErrorAction SilentlyContinue
    Write-Host '[INFO] Cleared environment variables from session'
}