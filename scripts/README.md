# Import Scripts

This directory contains automation scripts for importing Airtable data into Supabase.

## Scripts Overview

| Script | Purpose | Language | Usage |
|--------|---------|----------|-------|
| `export_from_airtable.py` | Fetch data from Airtable and create CSVs | Python | `python export_from_airtable.py` |
| `import_to_supabase.py` | Import CSVs into Supabase staging tables | Python | `python import_to_supabase.py` |
| `validate_import.py` | Run post-import validation checks | Python | `python validate_import.py` |
| `map_foreign_keys.py` | Map Airtable record IDs to Supabase UUIDs | Python | `python map_foreign_keys.py` |

## Prerequisites

### Python Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `python-dotenv` - Environment variable management
- `requests` - Airtable API calls
- `psycopg2-binary` - PostgreSQL database connection
- `supabase-py` - Supabase client library
- `pandas` - Data manipulation (optional)

### Environment Variables

Create a `.env` file in the project root:

```env
# Airtable
AIRTABLE_API_KEY=patXXXXXXXXXXXX
AIRTABLE_BASE_ID=appE0ZM639JihQ4h5

# Supabase
SUPABASE_URL=https://ktitfajlacjysacdsfxf.supabase.co
SUPABASE_ANON_KEY=eyXXXXXXXXXXXX
SUPABASE_SERVICE_ROLE_KEY=eyXXXXXXXXXXXX
SUPABASE_DB_URL=postgresql://postgres.ktitfajlacjysacdsfxf:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

** Security Warning**: Never commit `.env` to git! Add it to `.gitignore`.

## Usage

### Step 1: Export from Airtable

```bash
python scripts/export_from_airtable.py
```

**What it does:**
1. Connects to Airtable using API key
2. Fetches all records from specified tables (with pagination)
3. Transforms data (clean values, convert arrays, format dates)
4. Generates CSV files in `data/airtable-exports/`
5. Creates mapping files for foreign key resolution

**Output:**
- `data/airtable-exports/candidates.csv`
- `data/airtable-exports/job_postings.csv`
- `data/airtable-exports/applications.csv`
- `data/airtable-exports/mappings.json` (FK mappings)

### Step 2: Import to Supabase

```bash
python scripts/import_to_supabase.py
```

**What it does:**
1. Connects to Supabase using service role key (bypasses RLS)
2. Creates staging tables if they don't exist
3. Imports CSV files using PostgreSQL COPY command
4. Reports row counts and any errors

**Options:**
```bash
# Import specific table only
python scripts/import_to_supabase.py --table candidates

# Dry run (validate without importing)
python scripts/import_to_supabase.py --dry-run

# Skip staging (import directly to production)
python scripts/import_to_supabase.py --direct
```

### Step 3: Map Foreign Keys

```bash
python scripts/map_foreign_keys.py
```

**What it does:**
1. Reads mapping.json from Step 1
2. Queries Supabase for inserted records
3. Maps Airtable record IDs → Supabase UUIDs
4. Updates applications table with correct candidate_id and job_posting_id

### Step 4: Validate Import

```bash
python scripts/validate_import.py
```

**What it does:**
1. Checks record counts match expectations
2. Validates foreign key integrity
3. Checks for NULL values in required fields
4. Identifies data quality issues
5. Generates validation report

**Output:**
```
 Candidates: 5 records imported
 Job Postings: 2 records imported
 Applications: 7 records imported
 Foreign key integrity: OK
  Found 2 records with missing phone numbers
 Validation complete - 0 critical issues
```

## GitHub Actions Integration

The scripts are designed to run in GitHub Actions workflows.

### Workflow: Manual Import

`.github/workflows/import-airtable-data.yml`

**Triggers:**
- Manual trigger (workflow_dispatch)
- Push to `data/airtable-exports/` directory

**Steps:**
1. Checkout code
2. Setup Python
3. Install dependencies
4. Run export script (fetches latest from Airtable)
5. Run import script (loads into Supabase)
6. Run validation script
7. Upload validation report as artifact

**Required Secrets:**
- `AIRTABLE_API_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_DB_URL`

### Workflow: Scheduled Sync

`.github/workflows/sync-airtable-daily.yml`

**Triggers:**
- Scheduled: Daily at 2 AM UTC
- Manual trigger

**Steps:**
1. Export latest data from Airtable
2. Check for changes (compare with last commit)
3. If changes detected:
   - Commit new CSVs to repo
   - Trigger import workflow
   - Send notification (optional)

## Script Details

### export_from_airtable.py

**Key Functions:**
- `fetch_airtable_table(table_name)` - Fetch all records with pagination
- `transform_candidate(record)` - Transform candidate record to CSV row
- `transform_job_posting(record)` - Transform job posting record
- `transform_application(record)` - Transform application record
- `create_fk_mappings(candidates, jobs, apps)` - Build FK mapping dictionary

**Features:**
- Automatic pagination for large tables
- Field type detection (string, array, date, number)
- JSONB preservation of all Airtable fields
- ENUM value validation and mapping
- UTF-8 encoding
- Progress indicators

### import_to_supabase.py

**Key Functions:**
- `create_staging_tables()` - Create staging tables with relaxed constraints
- `import_csv_to_staging(table, csv_file)` - Use PostgreSQL COPY command
- `transform_staging_to_production()` - Apply business logic and move to prod
- `verify_import()` - Check row counts

**Features:**
- Transaction support (rollback on error)
- Batch inserts for performance
- Connection pooling
- Error handling and logging
- Dry-run mode for testing

### map_foreign_keys.py

**Key Functions:**
- `load_mappings()` - Load Airtable→Supabase mappings
- `get_candidate_uuid(airtable_id)` - Lookup candidate UUID
- `get_job_posting_uuid(airtable_id)` - Lookup job posting UUID
- `update_application_fks()` - Update applications with proper FKs

**Features:**
- Handles missing FK references gracefully
- Reports unmatched records
- Updates in batches
- Verifies FK constraints after update

### validate_import.py

**Key Functions:**
- `check_record_counts()` - Compare expected vs actual counts
- `check_fk_integrity()` - Find orphaned records
- `check_required_fields()` - Find NULL in NOT NULL columns
- `check_data_quality()` - Run custom validation rules
- `generate_report()` - Create markdown report

**Features:**
- Comprehensive validation suite
- Generates actionable reports
- Identifies data quality issues
- Exports results as JSON/markdown

## Troubleshooting

### "Authentication failed" error
- Check `SUPABASE_SERVICE_ROLE_KEY` is correct
- Ensure using service role key, not anon key
- Verify key hasn't expired

### "Table does not exist" error
- Run SQL scripts first to create tables
- Check schema: tables should be in `public` schema
- Run `\dt public.*` to list tables

### "Foreign key violation" error
- Import candidates and job_postings before applications
- Run `map_foreign_keys.py` to update FK references
- Check mapping.json has correct record IDs

### "CSV parsing error"
- Check CSV encoding is UTF-8
- Ensure no unescaped quotes in data
- Validate CSV with `csvlint` or pandas

### Import is very slow
- Use COPY instead of INSERT for bulk imports
- Disable indexes temporarily during import
- Use connection pooling (port 6543)
- Consider batching large imports

## Best Practices

1. **Always test in dev/staging first**
2. **Backup production before running scripts**
3. **Use staging tables for imports**
4. **Validate data before promoting to production**
5. **Log all operations for audit trail**
6. **Use transactions for atomicity**
7. **Monitor script execution times**
8. **Set up alerts for failures**

## Contact

For script issues or feature requests:
- See `MIGRATION_SUMMARY.md` - Overall migration plan
- See `/sql/README.md` - Database schema documentation
- See `/data/airtable-exports/README.md` - CSV format details
