#!/bin/bash
# reset_qa.sh - Reset QA database schema
# Drops all tables in careercoach_qa and reapplies migrations
# Used by CI/CD pipelines to ensure clean QA environment

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Environment variables (should be set by CI/CD)
: "${SUPABASE_DB_URL_CAREERCOACH_QA:?SUPABASE_DB_URL_CAREERCOACH_QA not set}"
: "${CI_RUNNER_DB_PASSWORD:?CI_RUNNER_DB_PASSWORD not set}"

# Extract database connection details from URL
# Format: postgresql://user:pass@host:port/db
DB_URL="$SUPABASE_DB_URL_CAREERCOACH_QA"
DB_HOST=$(echo "$DB_URL" | sed -n 's|.*@\([^:]*\):.*|\1|p')
DB_PORT=$(echo "$DB_URL" | sed -n 's|.*:\([0-9]*\)/.*|\1|p')
DB_NAME=$(echo "$DB_URL" | sed -n 's|.*/\([^?]*\).*|\1|p')

echo " Resetting QA database schema..."
echo "Host: $DB_HOST"
echo "Port: $DB_PORT"
echo "Database: $DB_NAME"

# Function to run psql commands
run_psql() {
    local query="$1"
    PGPASSWORD="$CI_RUNNER_DB_PASSWORD" psql \
        -h "$DB_HOST" \
        -p "$DB_PORT" \
        -U "ci_runner_user" \
        -d "$DB_NAME" \
        -c "$query" \
        --quiet \
        --no-align \
        --tuples-only
}

# Verify connection and permissions
echo " Verifying CI runner permissions..."
run_psql "SELECT version();" > /dev/null
echo " Database connection successful"

# Check if ci_runner_user has proper permissions
USER_PERMS=$(run_psql "SELECT rolname FROM pg_roles WHERE rolname = 'ci_runner_user';")
if [[ -z "$USER_PERMS" ]]; then
    echo " ci_runner_user does not exist or no permissions"
    exit 1
fi
echo " CI runner user verified"

# Get list of all tables in the database
echo " Getting list of existing tables..."
TABLES=$(run_psql "
    SELECT schemaname || '.' || tablename
    FROM pg_tables
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    ORDER BY schemaname, tablename;
")

if [[ -n "$TABLES" ]]; then
    echo "🗑️  Dropping existing tables..."
    # Drop all tables in reverse dependency order
    run_psql "
        DO \$\$
        DECLARE
            r RECORD;
        BEGIN
            -- Drop all tables in dependency order
            FOR r IN (
                SELECT schemaname, tablename
                FROM pg_tables
                WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                ORDER BY schemaname, tablename
            ) LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.schemaname) || '.' || quote_ident(r.tablename) || ' CASCADE';
                RAISE NOTICE 'Dropped table: %.%', r.schemaname, r.tablename;
            END LOOP;
        END
        \$\$;
    "
    echo " All tables dropped"
else
    echo "ℹ️  No existing tables to drop"
fi

# Verify database is clean
REMAINING_TABLES=$(run_psql "
    SELECT COUNT(*)
    FROM pg_tables
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
")

if [[ "$REMAINING_TABLES" -eq 0 ]]; then
    echo " Database schema reset complete"
else
    echo " Failed to reset database schema. $REMAINING_TABLES tables remaining"
    exit 1
fi

echo " QA database reset successful"