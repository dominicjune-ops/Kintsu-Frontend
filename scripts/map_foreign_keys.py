"""
Map Airtable record IDs to Supabase UUIDs for foreign key relationships.

This script:
1. Queries Supabase for inserted candidates and job postings
2. Creates mapping from Airtable IDs to Supabase UUIDs
3. Updates applications table with correct foreign keys

Usage:
    python scripts/map_foreign_keys.py
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Load environment variables
load_dotenv()

SUPABASE_DB_URL = os.getenv('SUPABASE_DB_URL')

if not SUPABASE_DB_URL:
    print(" Error: SUPABASE_DB_URL must be set in .env file")
    sys.exit(1)


def get_db_connection():
    """Create database connection."""
    try:
        conn = psycopg2.connect(SUPABASE_DB_URL)
        return conn
    except Exception as e:
        print(f" Database connection failed: {e}")
        sys.exit(1)


def create_fk_mapping_tables(conn):
    """Create temporary tables for FK mappings."""
    print(" Creating FK mapping tables...")
    
    cur = conn.cursor()
    
    # Create candidate mapping table
    cur.execute("""
        CREATE TEMP TABLE candidate_mapping AS
        SELECT 
            candidate_id::TEXT as airtable_id,
            id as supabase_uuid
        FROM public.candidates;
    """)
    
    candidate_count = cur.rowcount
    print(f"   Mapped {candidate_count} candidates")
    
    # Create job posting mapping table (by company + title)
    # Since job_postings don't have Airtable IDs, we'll map by position
    cur.execute("""
        CREATE TEMP TABLE job_posting_mapping AS
        SELECT 
            ROW_NUMBER() OVER (ORDER BY created_at) as row_num,
            id as supabase_uuid,
            job_title,
            company_name
        FROM public.job_postings;
    """)
    
    job_count = cur.rowcount
    print(f"   Mapped {job_count} job postings")
    
    conn.commit()
    cur.close()
    
    return candidate_count, job_count


def update_applications_fks(conn):
    """Update applications with correct candidate_id and job_posting_id."""
    print("\n🔗 Updating application foreign keys...")
    
    cur = conn.cursor()
    
    # First, add temporary columns to applications if they don't exist
    cur.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'applications_staging' 
                AND column_name = 'candidate_uuid'
            ) THEN
                ALTER TABLE applications_staging ADD COLUMN candidate_uuid UUID;
                ALTER TABLE applications_staging ADD COLUMN job_posting_uuid UUID;
            END IF;
        END $$;
    """)
    
    # Map candidate Airtable IDs to UUIDs
    cur.execute("""
        UPDATE applications_staging a
        SET candidate_uuid = cm.supabase_uuid
        FROM candidate_mapping cm
        WHERE a.candidate_airtable_id = cm.airtable_id;
    """)
    
    mapped_candidates = cur.rowcount
    print(f"   Mapped {mapped_candidates} application candidates")
    
    # For job postings, we need to map by position in staging table
    # This assumes job postings are in the same order in CSV
    cur.execute("""
        WITH numbered_apps AS (
            SELECT 
                *,
                ROW_NUMBER() OVER (ORDER BY application_date) as row_num
            FROM applications_staging
            WHERE job_posting_airtable_id IS NOT NULL 
            AND job_posting_airtable_id != ''
        )
        UPDATE applications_staging a
        SET job_posting_uuid = jpm.supabase_uuid
        FROM numbered_apps na
        JOIN job_posting_mapping jpm ON jpm.row_num = na.row_num
        WHERE a.application_name = na.application_name;
    """)
    
    mapped_jobs = cur.rowcount
    print(f"   Mapped {mapped_jobs} application job postings")
    
    conn.commit()
    cur.close()
    
    return mapped_candidates, mapped_jobs


def insert_applications_to_production(conn):
    """Insert applications from staging to production with proper FKs."""
    print("\n📥 Inserting applications to production...")
    
    cur = conn.cursor()
    
    # Check if production table exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'applications'
        );
    """)
    
    if not cur.fetchone()[0]:
        print("    Production applications table doesn't exist. Run SQL migration first.")
        cur.close()
        return 0
    
    # Insert applications with mapped FKs
    cur.execute("""
        INSERT INTO public.applications (
            candidate_id,
            job_posting_id,
            application_name,
            application_date,
            status,
            application_method,
            notes,
            follow_up_date,
            interview_date,
            offer_date,
            offer_deadline,
            rejection_date,
            rejection_reason,
            application_data
        )
        SELECT 
            candidate_uuid,
            job_posting_uuid,
            application_name,
            NULLIF(application_date, '')::DATE,
            COALESCE(NULLIF(status, ''), 'submitted')::application_status_enum,
            COALESCE(NULLIF(application_method, ''), 'online_portal')::application_method_enum,
            notes,
            NULLIF(follow_up_date, '')::DATE,
            NULLIF(interview_date, '')::TIMESTAMP WITH TIME ZONE,
            NULLIF(offer_date, '')::DATE,
            NULLIF(offer_deadline, '')::DATE,
            NULLIF(rejection_date, '')::DATE,
            rejection_reason,
            COALESCE(NULLIF(application_data, '')::jsonb, '{}'::jsonb)
        FROM applications_staging
        WHERE candidate_uuid IS NOT NULL
        ON CONFLICT DO NOTHING;
    """)
    
    count = cur.rowcount
    conn.commit()
    cur.close()
    
    print(f"   Inserted {count} applications")
    return count


def verify_fk_integrity(conn):
    """Verify foreign key relationships are correct."""
    print("\n Verifying FK integrity...")
    
    cur = conn.cursor()
    
    # Check for orphaned applications
    cur.execute("""
        SELECT COUNT(*) 
        FROM public.applications a
        WHERE NOT EXISTS (
            SELECT 1 FROM public.candidates c WHERE c.id = a.candidate_id
        );
    """)
    
    orphaned_candidates = cur.fetchone()[0]
    if orphaned_candidates > 0:
        print(f"    Found {orphaned_candidates} applications with invalid candidate_id")
    else:
        print(f"   All applications have valid candidate_id")
    
    # Check for applications without job postings (OK, as FK is nullable)
    cur.execute("""
        SELECT COUNT(*) 
        FROM public.applications 
        WHERE job_posting_id IS NULL;
    """)
    
    without_job = cur.fetchone()[0]
    print(f"  ℹ️  {without_job} applications without job_posting_id (OK if intentional)")
    
    cur.close()


def main():
    print("=" * 60)
    print("🔗 FOREIGN KEY MAPPING")
    print("=" * 60)
    print()
    
    # Connect to database
    conn = get_db_connection()
    print(" Connected to Supabase\n")
    
    # Create FK mapping tables
    candidate_count, job_count = create_fk_mapping_tables(conn)
    
    if candidate_count == 0:
        print("\n  No candidates found. Import candidates first:")
        print("   python scripts/import_to_supabase.py --table candidates")
        conn.close()
        sys.exit(1)
    
    # Update applications with mapped FKs
    mapped_candidates, mapped_jobs = update_applications_fks(conn)
    
    # Insert applications to production
    inserted = insert_applications_to_production(conn)
    
    # Verify FK integrity
    verify_fk_integrity(conn)
    
    # Close connection
    conn.close()
    
    print("\n" + "=" * 60)
    print(" FK MAPPING COMPLETE!")
    print("=" * 60)
    print(f"Candidates mapped: {mapped_candidates}")
    print(f"Job postings mapped: {mapped_jobs}")
    print(f"Applications inserted: {inserted}")
    
    print("\n Next steps:")
    print("1. Run validation: python scripts/validate_import.py")
    print("2. Test queries in Supabase")


if __name__ == '__main__':
    main()
