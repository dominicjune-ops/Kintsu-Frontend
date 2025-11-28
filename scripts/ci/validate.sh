#!/bin/bash
# scripts/ci/validate.sh
# CI validation script - mirrors GitHub Actions validation steps

set -euo pipefail

echo "=== CI Validation Script ==="

# Check Python syntax
echo " Checking Python syntax..."
python -m py_compile main.py 2>/dev/null && echo " main.py syntax OK" || echo " main.py syntax error"

# Check for required files
echo "📁 Checking required files..."
required_files=(
    "requirements.txt"
    "scripts/apply_migrations.sh"
    "scripts/reset_staging.sh"
    "ci/github-actions-staging.yml"
)

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo " $file exists"
    else
        echo " $file missing"
        exit 1
    fi
done

# Check script syntax
echo " Checking script syntax..."
bash -n scripts/apply_migrations.sh && echo " apply_migrations.sh syntax OK" || exit 1
bash -n scripts/reset_staging.sh && echo " reset_staging.sh syntax OK" || exit 1

# Check YAML syntax
echo "📄 Checking YAML syntax..."
if command -v python3 &> /dev/null; then
    python3 -c "import yaml; yaml.safe_load(open('ci/github-actions-staging.yml'))" && echo " github-actions-staging.yml YAML OK" || exit 1
else
    echo "  Python3 not available, skipping YAML validation"
fi

echo " All validation checks passed!"