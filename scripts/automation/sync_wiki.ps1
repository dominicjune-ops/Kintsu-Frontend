# Wiki Sync Launcher Script
# Syncs wiki-content from main repo to Azure DevOps wiki

$pat = Read-Host "Enter Azure DevOps PAT" -AsSecureString
$env:AZURE_DEVOPS_PAT = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($pat))
$env:AZURE_DEVOPS_ORG = 'CareerCoachai'
$env:AZURE_DEVOPS_PROJECT = 'CareerCoach.ai'

Write-Host '[INFO] Running wiki sync to Azure DevOps'

try {
    & ".\scripts\sync_wiki_to_azure.ps1" -AutoPush $true
    Write-Host '[SUCCESS] Wiki sync completed'
} catch {
    Write-Host '[ERROR] Wiki sync failed with exception:'
    Write-Host $_.Exception.Message
} finally {
    Remove-Item Env:AZURE_DEVOPS_PAT -ErrorAction SilentlyContinue
    Remove-Item Env:AZURE_DEVOPS_ORG -ErrorAction SilentlyContinue
    Remove-Item Env:AZURE_DEVOPS_PROJECT -ErrorAction SilentlyContinue
    Write-Host '[INFO] Cleared environment variables from session'
}