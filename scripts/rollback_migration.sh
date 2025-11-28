#!/usr/bin/env bash
# scripts/rollback_migration.sh
# Rollback specific migrations with audit tracking

set -euo pipefail

if [ $# -ne 2 ]; then
  echo "Usage: $0 <prod|staging> <migration_filename.sql>"
  exit 1
fi

ENV_NAME="$1"
MIG_FILE="$2"

case "$ENV_NAME" in
  prod)
    DB_URL="${SUPABASE_DB_URL_CAREERCOACH_PROD:?missing SUPABASE_DB_URL_CAREERCOACH_PROD}"
    SCHEMA="careercoach_prod"
    ;;
  staging)
    DB_URL="${SUPABASE_DB_URL_CAREERCOACH_STAGING:?missing SUPABASE_DB_URL_CAREERCOACH_STAGING}"
    SCHEMA="careercoach_staging"
    ;;
  *)
    echo "Rollback only supported for prod|staging"
    exit 1
    ;;
esac

echo "Rolling back $MIG_FILE in $SCHEMA..."

PGPASSWORD="${CI_RUNNER_DB_PASSWORD:-}" psql "$DB_URL" \
  -v schema="$SCHEMA" \
  -c "SET search_path TO ${SCHEMA}, public;" \
  -f "rollbacks/${MIG_FILE}"

# Record rollback in audit table
PGPASSWORD="${CI_RUNNER_DB_PASSWORD:-}" psql "$DB_URL" -c \
  "UPDATE public.schema_migrations
   SET rolled_back_at = now()
   WHERE schema_name='${SCHEMA}' AND filename='${MIG_FILE}';"

echo "Rollback complete for $MIG_FILE in $SCHEMA."