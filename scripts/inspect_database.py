"""Utility script to inspect database schema and tables."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import inspect, text
from database.config import engine, async_engine
from database.models import User, Resume, Job, Application


def inspect_schema():
    """Inspect database schema using synchronous engine."""
    inspector = inspect(engine)
    
    print("=== Database Schema Inspection ===\n")
    print(f"Database URL: {engine.url}\n")
    
    # Get all table names
    tables = inspector.get_table_names()
    print(f"Tables ({len(tables)}):")
    for table in tables:
        print(f"  - {table}")
    print()
    
    # Inspect each table
    for table_name in tables:
        print(f"\n=== Table: {table_name} ===")
        
        # Get columns
        columns = inspector.get_columns(table_name)
        print(f"\nColumns ({len(columns)}):")
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            default = f" DEFAULT {col['default']}" if col['default'] else ""
            print(f"  - {col['name']}: {col['type']} {nullable}{default}")
        
        # Get indexes
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print(f"\nIndexes ({len(indexes)}):")
            for idx in indexes:
                unique = "UNIQUE " if idx['unique'] else ""
                cols = ", ".join(idx['column_names'])
                print(f"  - {unique}{idx['name']}: ({cols})")
        
        # Get foreign keys
        foreign_keys = inspector.get_foreign_keys(table_name)
        if foreign_keys:
            print(f"\nForeign Keys ({len(foreign_keys)}):")
            for fk in foreign_keys:
                constrained = ", ".join(fk['constrained_columns'])
                referred = f"{fk['referred_table']}.{', '.join(fk['referred_columns'])}"
                print(f"  - {fk['name']}: {constrained} -> {referred}")


async def test_database_connection():
    """Test async database connection."""
    print("\n=== Testing Database Connection ===\n")
    
    async with async_engine.connect() as conn:
        result = await conn.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        print(f" Connection test: {row[0]}")
    
    print(" Database connection successful!\n")


def count_records():
    """Count records in each table."""
    print("\n=== Record Counts ===\n")
    
    with engine.connect() as conn:
        for table in ["users", "resumes", "jobs", "applications"]:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            print(f"  {table}: {count} records")


if __name__ == "__main__":
    # Inspect schema
    inspect_schema()
    
    # Count records
    count_records()
    
    # Test async connection
    asyncio.run(test_database_connection())
    
    print("\n Database inspection complete!")
