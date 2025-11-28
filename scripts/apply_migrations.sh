#!/usr/bin/env bash
set -euo pipefail

# Parse arguments
DRY_RUN=false
if [[ "${2:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo " DRY RUN MODE - No actual database changes will be made"
fi

if [ $# -lt 1 ]; then
  echo "Usage: $0 <dev|qa|staging> [--dry-run]"
  exit 1
fi

ENV_NAME="$1"
case "$ENV_NAME" in
  dev)
    DB_URL="${SUPABASE_DB_URL_CAREERCOACH_DEV:?missing SUPABASE_DB_URL_CAREERCOACH_DEV}"
    SCHEMA="careercoach_dev"
    ;;
  qa)
    DB_URL="${SUPABASE_DB_URL_CAREERCOACH_QA:?missing SUPABASE_DB_URL_CAREERCOACH_QA}"
    SCHEMA="careercoach_qa"
    ;;
  staging)
    DB_URL="${SUPABASE_DB_URL_CAREERCOACH_STAGING:?missing SUPABASE_DB_URL_CAREERCOACH_STAGING}"
    SCHEMA="careercoach_staging"
    ;;
  *)
    echo "Invalid env: $ENV_NAME"
    exit 1
    ;;
esac

# Ensure the audit table exists
if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] Would ensure migrations audit table exists..."
else
    echo "Ensuring migrations audit table exists..."
    PGPASSWORD="${CI_RUNNER_DB_PASSWORD:-}" psql "$DB_URL" -v ON_ERROR_STOP=1 -f migrations/common/0000_schema_migrations.sql
fi

# Enforce schema-first search_path for unqualified SQL
export PSQLRC="$(mktemp)"
echo '\set ON_ERROR_STOP on' > "$PSQLRC"

MIG_DIR="migrations/${ENV_NAME}"
if [ ! -d "$MIG_DIR" ]; then
  echo "No migration directory found: $MIG_DIR"
  exit 0
fi

# Apply in lexical order; skip already recorded files
for f in $(ls -1 "$MIG_DIR"/*.sql 2>/dev/null | sort); do
  fname="${f##*/}"

  # Skip if already recorded
  already=$(PGPASSWORD="${CI_RUNNER_DB_PASSWORD:-}" psql "$DB_URL" -t -A -c \
    "SELECT 1 FROM public.schema_migrations WHERE schema_name='${SCHEMA}' AND filename='${fname}'")
  if [[ "$already" == "1" ]]; then
    echo "Skipping already applied: $fname"
    continue
  fi

  echo "Applying $fname to schema $SCHEMA..."
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] Would apply migration: $fname"
  else
    PGPASSWORD="${CI_RUNNER_DB_PASSWORD:-}" psql "$DB_URL" \
      -v schema="$SCHEMA" \
      -c "SET search_path TO ${SCHEMA}, public;" \
      -f "$f"
  fi

  # Record application
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] Would record migration: $fname"
  else
    PGPASSWORD="${CI_RUNNER_DB_PASSWORD:-}" psql "$DB_URL" -v ON_ERROR_STOP=1 -c \
      "INSERT INTO public.schema_migrations(schema_name, filename) VALUES ('${SCHEMA}', '${fname}') ON CONFLICT DO NOTHING;"
  fi
done

echo "Migrations applied for $ENV_NAME."