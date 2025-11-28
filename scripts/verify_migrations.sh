#!/usr/bin/env bash
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

PGPASSWORD="${CI_RUNNER_DB_PASSWORD:-}" psql "$DB_URL" -x -c \
  "SELECT schema_name, filename, applied_at FROM public.schema_migrations WHERE schema_name='${SCHEMA}' ORDER BY applied_at DESC;"