"""
Database Index Creation Script

Executes all performance-optimized indexes for CareerCoach.ai database.
Run this script to create composite indexes and improve query performance.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from database.config import engine


# Index definitions for optimal query performance
INDEXES = [
    # User indexes
    """
    CREATE INDEX IF NOT EXISTS idx_users_email 
    ON users(email);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_users_created_at 
    ON users(created_at DESC);
    """,
    
    # Resume indexes
    """
    CREATE INDEX IF NOT EXISTS idx_resumes_user_id 
    ON resumes(user_id);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_resumes_created_at 
    ON resumes(created_at DESC);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_resumes_user_created 
    ON resumes(user_id, created_at DESC);
    """,
    
    # Job indexes
    """
    CREATE INDEX IF NOT EXISTS idx_jobs_company 
    ON jobs(company);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_jobs_location 
    ON jobs(location);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_jobs_title 
    ON jobs(title);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_jobs_posted_date 
    ON jobs(posted_date DESC);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_jobs_company_location 
    ON jobs(company, location);
    """,
    
    # Application indexes
    """
    CREATE INDEX IF NOT EXISTS idx_applications_user_id 
    ON applications(user_id);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_applications_job_id 
    ON applications(job_id);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_applications_status 
    ON applications(status);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_applications_user_status 
    ON applications(user_id, status);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_applications_created_at 
    ON applications(created_at DESC);
    """,
    
    # Subscription indexes
    """
    CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id 
    ON subscriptions(user_id);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_subscriptions_status 
    ON subscriptions(status);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_subscriptions_tier 
    ON subscriptions(tier);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_subscriptions_user_status 
    ON subscriptions(user_id, status);
    """,
    
    # Mentor indexes
    """
    CREATE INDEX IF NOT EXISTS idx_mentors_status 
    ON mentors(status);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_mentors_rating 
    ON mentors(average_rating DESC);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_mentors_status_rating 
    ON mentors(status, average_rating DESC);
    """,
    
    # Mentor session indexes
    """
    CREATE INDEX IF NOT EXISTS idx_mentor_sessions_mentor_id 
    ON mentor_sessions(mentor_id);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_mentor_sessions_user_id 
    ON mentor_sessions(user_id);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_mentor_sessions_status 
    ON mentor_sessions(status);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_mentor_sessions_scheduled 
    ON mentor_sessions(scheduled_start);
    """,
    
    # API rate limit indexes
    """
    CREATE INDEX IF NOT EXISTS idx_rate_limits_user_endpoint 
    ON rate_limits(user_id, endpoint);
    """,
    
    """
    CREATE INDEX IF NOT EXISTS idx_rate_limits_timestamp 
    ON rate_limits(timestamp);
    """,
]


def create_indexes():
    """Execute all index creation statements"""
    print(" Creating database indexes...")
    
    created = 0
    failed = 0
    
    with engine.connect() as conn:
        for idx, index_sql in enumerate(INDEXES, 1):
            try:
                conn.execute(text(index_sql))
                conn.commit()
                created += 1
                print(f" [{idx}/{len(INDEXES)}] Index created successfully")
            except Exception as e:
                failed += 1
                print(f" [{idx}/{len(INDEXES)}] Failed: {str(e)[:100]}")
    
    print(f"\n Summary:")
    print(f"   Created: {created}/{len(INDEXES)}")
    print(f"   Failed: {failed}/{len(INDEXES)}")
    
    if failed == 0:
        print(" All indexes created successfully!")
    else:
        print(f"  {failed} indexes failed (may already exist)")


def analyze_tables():
    """Run ANALYZE on all tables to update statistics"""
    print("\n Analyzing tables for query planner...")
    
    tables = [
        "users", "resumes", "jobs", "applications",
        "subscriptions", "mentors", "mentor_sessions",
        "rate_limits"
    ]
    
    with engine.connect() as conn:
        for table in tables:
            try:
                conn.execute(text(f"ANALYZE {table}"))
                print(f" Analyzed: {table}")
            except Exception as e:
                print(f" Failed to analyze {table}: {str(e)[:50]}")


def check_index_usage():
    """Query index usage statistics"""
    print("\n Checking index usage statistics...")
    
    query = text("""
        SELECT 
            schemaname,
            tablename,
            indexname,
            idx_scan as scans,
            idx_tup_read as tuples_read,
            idx_tup_fetch as tuples_fetched
        FROM pg_stat_user_indexes
        WHERE schemaname = 'public'
        ORDER BY idx_scan DESC
        LIMIT 20;
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query)
            rows = result.fetchall()
            
            if rows:
                print(f"\n{'Table':<20} {'Index':<30} {'Scans':<10} {'Tuples Read':<15}")
                print("-" * 80)
                for row in rows:
                    print(f"{row[1]:<20} {row[2]:<30} {row[3]:<10} {row[4]:<15}")
            else:
                print("No index usage statistics available yet.")
    except Exception as e:
        print(f" Failed to retrieve index stats: {str(e)}")


def check_missing_indexes():
    """Identify tables that might benefit from additional indexes"""
    print("\n Checking for potential missing indexes...")
    
    # Query for sequential scans on large tables
    query = text("""
        SELECT 
            schemaname,
            tablename,
            seq_scan,
            seq_tup_read,
            idx_scan,
            n_live_tup as rows
        FROM pg_stat_user_tables
        WHERE schemaname = 'public'
        AND seq_scan > 100
        AND n_live_tup > 1000
        ORDER BY seq_scan DESC;
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query)
            rows = result.fetchall()
            
            if rows:
                print(f"\n{'Table':<20} {'Seq Scans':<12} {'Rows Read':<15} {'Index Scans':<12} {'Total Rows':<12}")
                print("-" * 80)
                for row in rows:
                    print(f"{row[1]:<20} {row[2]:<12} {row[3]:<15} {row[4]:<12} {row[5]:<12}")
                print("\n  Tables with high sequential scans may benefit from additional indexes.")
            else:
                print(" No obvious missing indexes detected.")
    except Exception as e:
        print(f" Failed to check missing indexes: {str(e)}")


if __name__ == "__main__":
    print(" CareerCoach.ai Database Optimization")
    print("=" * 50)
    
    # Create all indexes
    create_indexes()
    
    # Analyze tables
    analyze_tables()
    
    # Check index usage
    check_index_usage()
    
    # Check for missing indexes
    check_missing_indexes()
    
    print("\n Database optimization complete!")
