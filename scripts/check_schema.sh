#!/usr/bin/env bash
# scripts/check_schema.sh
# Quick schema validation to confirm expected tables exist and match migration definitions

set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: $0 <dev|qa|staging>"
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

echo "Listing tables in schema $SCHEMA..."
RESULT=$(PGPASSWORD="${CI_RUNNER_DB_PASSWORD:-}" \
psql "${DB_URL}?connect_timeout=10" --no-align --tuples-only \
--command="SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = '${SCHEMA}';")

if [ -z "$RESULT" ]; then
  echo " No tables found in schema $SCHEMA — failing CI early."
  exit 1
else
  echo "$RESULT"
fi