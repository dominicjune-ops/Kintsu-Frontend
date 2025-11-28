# CareerCoach.ai Canonical Validation Deployment Script
# This PowerShell script sets up and runs canonical validation across your entire stack

param(
    [Parameter(Mandatory=$true)]
    [string]$JobDataFile,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("linkedin", "indeed", "ziprecruiter", "google_jobs", "bing_jobs")]
    [string]$Connector,
    
    [Parameter(Mandatory=$false)]
    [string]$CommitSha,
    
    [Parameter(Mandatory=$false)]
    [switch]$FailFast,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipIntegration,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputDir = "validation-results"
)

# Script configuration
$ErrorActionPreference = "Continue"
$VerbosePreference = "Continue"

Write-Host " CareerCoach.ai Canonical Validation Pipeline" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Ensure output directory exists
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    Write-Host "📁 Created output directory: $OutputDir" -ForegroundColor Green
}

# Generate timestamped output files
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$validationResultsFile = Join-Path $OutputDir "validation-results-$timestamp.json"
$integrationResultsFile = Join-Path $OutputDir "integration-results-$timestamp.json"

Write-Host " Validation results will be saved to: $validationResultsFile" -ForegroundColor Yellow

# Step 1: Run canonical validation
Write-Host "`n STEP 1: Running Canonical Validation Checklist" -ForegroundColor Cyan
Write-Host "-" * 50 -ForegroundColor Cyan

$validationArgs = @(
    "scripts/canonical_validation.py",
    "--input", $JobDataFile,
    "--output", $validationResultsFile
)

if ($Connector) {
    $validationArgs += "--connector", $Connector
    Write-Host "🔌 Connector: $Connector" -ForegroundColor Yellow
}

if ($FailFast) {
    $validationArgs += "--fail-fast"
    Write-Host " Fail-fast mode enabled" -ForegroundColor Yellow
}

Write-Host "▶️ Running validation..." -ForegroundColor White

try {
    $validationResult = python @validationArgs
    $validationExitCode = $LASTEXITCODE
    
    Write-Host $validationResult
    
    if ($validationExitCode -eq 0) {
        Write-Host " Canonical validation PASSED" -ForegroundColor Green
    } else {
        Write-Host " Canonical validation FAILED" -ForegroundColor Red
        
        if ($FailFast) {
            Write-Host "🛑 Exiting due to validation failure (fail-fast mode)" -ForegroundColor Red
            exit $validationExitCode
        }
    }
} catch {
    Write-Host " Error running canonical validation: $_" -ForegroundColor Red
    if ($FailFast) {
        exit 1
    }
}

# Step 2: Run cross-platform integration (unless skipped)
if (!$SkipIntegration) {
    Write-Host "`n⚙️ STEP 2: Cross-Platform Integration" -ForegroundColor Cyan
    Write-Host "-" * 50 -ForegroundColor Cyan
    
    if (Test-Path $validationResultsFile) {
        $integrationArgs = @(
            "scripts/cross_platform_integration.py",
            "--validation-results", $validationResultsFile
        )
        
        if ($CommitSha) {
            $integrationArgs += "--commit-sha", $CommitSha
            Write-Host "🔗 GitHub commit SHA: $CommitSha" -ForegroundColor Yellow
        }
        
        Write-Host "▶️ Running cross-platform integration..." -ForegroundColor White
        
        try {
            $integrationResult = python @integrationArgs
            $integrationExitCode = $LASTEXITCODE
            
            Write-Host $integrationResult
            
            # Save integration results
            $integrationSummary = @{
                timestamp = (Get-Date -Format "o")
                validation_file = $validationResultsFile
                commit_sha = $CommitSha
                integration_exit_code = $integrationExitCode
                success = ($integrationExitCode -eq 0)
            }
            
            $integrationSummary | ConvertTo-Json -Depth 4 | Out-File $integrationResultsFile -Encoding UTF8
            
            if ($integrationExitCode -eq 0) {
                Write-Host " Cross-platform integration completed successfully" -ForegroundColor Green
            } else {
                Write-Host " Some platform integrations failed (check logs)" -ForegroundColor Yellow
            }
        } catch {
            Write-Host " Error running cross-platform integration: $_" -ForegroundColor Red
        }
    } else {
        Write-Host " Skipping integration - validation results file not found" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n STEP 2: Cross-Platform Integration SKIPPED" -ForegroundColor Yellow
}

# Step 3: Generate summary report
Write-Host "`n STEP 3: Validation Summary" -ForegroundColor Cyan
Write-Host "-" * 50 -ForegroundColor Cyan

if (Test-Path $validationResultsFile) {
    try {
        $validationData = Get-Content $validationResultsFile -Raw | ConvertFrom-Json
        
        Write-Host "📄 Job ID: $($validationData.job_id)" -ForegroundColor White
        Write-Host "⏰ Timestamp: $($validationData.timestamp)" -ForegroundColor White
        Write-Host " Overall Status: " -NoNewline -ForegroundColor White
        
        if ($validationData.overall_status -eq "PASS") {
            Write-Host " COMPLIANT" -ForegroundColor Green
        } else {
            Write-Host " NON-COMPLIANT" -ForegroundColor Red
        }
        
        Write-Host "`n Category Breakdown:" -ForegroundColor White
        
        foreach ($category in $validationData.validation_results.PSObject.Properties) {
            $categoryName = $category.Name -replace "_", " " | ForEach-Object { (Get-Culture).TextInfo.ToTitleCase($_) }
            $status = $category.Value.status
            $errorCount = $category.Value.errors.Count
            
            if ($status -eq "PASS") {
                Write-Host "    $categoryName" -ForegroundColor Green
            } else {
                Write-Host "    $categoryName ($errorCount errors)" -ForegroundColor Red
            }
        }
        
        # Show errors if validation failed
        if ($validationData.overall_status -eq "FAIL") {
            Write-Host "`n Error Details:" -ForegroundColor Yellow
            
            foreach ($category in $validationData.validation_results.PSObject.Properties) {
                if ($category.Value.errors.Count -gt 0) {
                    $categoryName = $category.Name -replace "_", " " | ForEach-Object { (Get-Culture).TextInfo.ToTitleCase($_) }
                    Write-Host "    $categoryName" -ForegroundColor Yellow
                    
                    foreach ($error in $category.Value.errors) {
                        Write-Host "      • $error" -ForegroundColor Red
                    }
                }
            }
        }
        
    } catch {
        Write-Host " Error reading validation results: $_" -ForegroundColor Red
    }
} else {
    Write-Host " Validation results file not found" -ForegroundColor Red
}

# Step 4: Output file locations and next steps
Write-Host "`n📁 Generated Files:" -ForegroundColor Cyan
Write-Host "-" * 50 -ForegroundColor Cyan

if (Test-Path $validationResultsFile) {
    Write-Host " Validation Results: $validationResultsFile" -ForegroundColor Green
} else {
    Write-Host " Validation Results: File not created" -ForegroundColor Red
}

if (Test-Path $integrationResultsFile) {
    Write-Host " Integration Results: $integrationResultsFile" -ForegroundColor Green
} else {
    Write-Host " Integration Results: Not created (skipped or failed)" -ForegroundColor Yellow
}

# Step 5: Next steps and commands
Write-Host "`n Quick Commands for Manual Testing:" -ForegroundColor Cyan
Write-Host "-" * 50 -ForegroundColor Cyan

Write-Host "# Re-run validation only:" -ForegroundColor Gray
Write-Host "python scripts/canonical_validation.py --input `"$JobDataFile`" --output validation-results.json$(if ($Connector) { " --connector $Connector" })" -ForegroundColor White

Write-Host "`n# Re-run integration only:" -ForegroundColor Gray  
Write-Host "python scripts/cross_platform_integration.py --validation-results `"$validationResultsFile`"$(if ($CommitSha) { " --commit-sha $CommitSha" })" -ForegroundColor White

Write-Host "`n# Run specific platform integration:" -ForegroundColor Gray
Write-Host "python scripts/cross_platform_integration.py --validation-results `"$validationResultsFile`" --platform notion" -ForegroundColor White

Write-Host "`n# Run connector-specific tests:" -ForegroundColor Gray
if ($Connector) {
    Write-Host "python -m pytest tests/connectors/test_$($Connector)_connector.py -v" -ForegroundColor White
} else {
    Write-Host "python -m pytest tests/connectors/ -v" -ForegroundColor White
}

# Final exit code determination
$finalExitCode = 0

if (Test-Path $validationResultsFile) {
    try {
        $validationData = Get-Content $validationResultsFile -Raw | ConvertFrom-Json
        if ($validationData.overall_status -ne "PASS") {
            $finalExitCode = 1
        }
    } catch {
        $finalExitCode = 1
    }
} else {
    $finalExitCode = 1
}

Write-Host "`n" + "=" * 60 -ForegroundColor Cyan

if ($finalExitCode -eq 0) {
    Write-Host " CANONICAL VALIDATION PIPELINE COMPLETED SUCCESSFULLY!" -ForegroundColor Green
} else {
    Write-Host " CANONICAL VALIDATION PIPELINE COMPLETED WITH ISSUES" -ForegroundColor Red
}

Write-Host "=" * 60 -ForegroundColor Cyan

exit $finalExitCode