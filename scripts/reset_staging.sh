#!/bin/bash
# scripts/reset_staging.sh
# Reset staging database schema for clean deployments

set -euo pipefail

# Parse arguments
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo " DRY RUN MODE - No actual database changes will be made"
fi

echo "=== Resetting Staging Database Schema ==="

# Validate environment variables
if [[ -z "${SUPABASE_DB_URL_CAREERCOACH_STAGING:-}" ]]; then
    echo " Error: SUPABASE_DB_URL_CAREERCOACH_STAGING environment variable not set"
    exit 1
fi

if [[ -z "${CI_RUNNER_DB_PASSWORD:-}" ]]; then
    echo " Error: CI_RUNNER_DB_PASSWORD environment variable not set"
    exit 1
fi

# Extract database connection details from URL
DB_URL="$SUPABASE_DB_URL_CAREERCOACH_STAGING"
DB_HOST=$(echo "$DB_URL" | sed -n 's|.*://\([^:]*\):\([^@]*\)@\(.*\):\([0-9]*\)/\(.*\)|\3|p')
DB_PORT=$(echo "$DB_URL" | sed -n 's|.*://\([^:]*\):\([^@]*\)@\(.*\):\([0-9]*\)/\(.*\)|\4|p')
DB_NAME=$(echo "$DB_URL" | sed -n 's|.*://\([^:]*\):\([^@]*\)@\(.*\):\([0-9]*\)/\(.*\)|\5|p')
DB_USER=$(echo "$DB_URL" | sed -n 's|.*://\([^:]*\):\([^@]*\)@\(.*\):\([0-9]*\)/\(.*\)|\1|p')

echo " Connecting to staging database: $DB_HOST:$DB_PORT/$DB_NAME"

# Test database connection
echo "Testing database connection..."
if ! PGPASSWORD="$CI_RUNNER_DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -c "SELECT 1;" \
    --quiet \
    --no-align \
    --tuples-only; then
    echo " Error: Cannot connect to staging database"
    exit 1
fi

echo " Database connection successful"

# Get list of all tables (excluding system tables)
echo " Discovering existing tables..."
TABLES=$(PGPASSWORD="$CI_RUNNER_DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -c "SELECT tablename FROM pg_tables WHERE schemaname = 'public';" \
    --quiet \
    --no-align \
    --tuples-only)

if [[ -z "$TABLES" ]]; then
    echo "ℹ️  No tables found in staging database"
else
    echo "🗑️  Dropping existing tables..."
    echo "$TABLES" | while read -r table; do
        if [[ -n "$table" ]]; then
            if [[ "$DRY_RUN" == "true" ]]; then
                echo "  [DRY RUN] Would drop table: $table"
            else
                echo "  Dropping table: $table"
                PGPASSWORD="$CI_RUNNER_DB_PASSWORD" psql \
                    -h "$DB_HOST" \
                    -p "$DB_PORT" \
                    -U "$DB_USER" \
                    -d "$DB_NAME" \
                    -c "DROP TABLE IF EXISTS \"$table\" CASCADE;" \
                    --quiet
            fi
        fi
    done
fi

# Verify clean state
echo " Verifying clean database state..."
REMAINING_TABLES=$(PGPASSWORD="$CI_RUNNER_DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -c "SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public';" \
    --quiet \
    --no-align \
    --tuples-only)

if [[ "$REMAINING_TABLES" -eq 0 ]]; then
    echo " Staging database schema reset complete"
    echo " Tables remaining: $REMAINING_TABLES"
else
    echo "  Warning: $REMAINING_TABLES tables still exist after reset"
    exit 1
fi

echo " Staging environment ready for migration"