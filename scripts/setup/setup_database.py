#!/usr/bin/env python3
"""
Database Setup and Initialization Script for CareerCoach.ai
Creates all required database tables and schema
"""

import os
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, Float, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# Define database models
Base = declarative_base()

class JobPosting(Base):
    __tablename__ = 'job_postings'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    description = Column(Text)
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    remote = Column(Boolean, default=False)
    job_type = Column(String(50))
    experience_level = Column(String(50))
    posted_date = Column(DateTime)
    url = Column(String(500))
    source = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class PerformanceMetric(Base):
    __tablename__ = 'performance_metrics'
    
    id = Column(Integer, primary_key=True)
    query_id = Column(String(100))
    query_text = Column(Text)
    execution_time = Column(Float)
    rows_affected = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    table_name = Column(String(100))
    operation_type = Column(String(50))
    cpu_usage = Column(Float)
    memory_usage = Column(Float)

class SystemAlert(Base):
    __tablename__ = 'system_alerts'
    
    id = Column(Integer, primary_key=True)
    alert_type = Column(String(50))
    severity = Column(String(20))
    message = Column(Text)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)

class ResumeAnalysis(Base):
    __tablename__ = 'resume_analysis'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))
    resume_text = Column(Text)
    job_posting_id = Column(Integer)
    ats_score = Column(Float)
    recommendations = Column(Text)  # JSON string
    tailored_resume = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_database_schema():
    """Create all database tables"""
    print("🗄️ Setting up CareerCoach.ai Database Schema...")
    
    # Create main database
    database_url = "sqlite:///careercoach.db"
    engine = create_engine(database_url, echo=True)
    
    # Create all tables
    Base.metadata.create_all(engine)
    print(" Created main database tables")
    
    # Create performance database
    perf_database_url = "sqlite:///careercoach_performance.db"
    perf_engine = create_engine(perf_database_url, echo=True)
    Base.metadata.create_all(perf_engine)
    print(" Created performance database tables")
    
    return engine, perf_engine

def populate_sample_data():
    """Add sample data for testing"""
    print(" Adding sample data...")
    
    engine = create_engine("sqlite:///careercoach.db")
    SessionLocal = sessionmaker(bind=engine)
    
    sample_jobs = [
        {
            "title": "Senior Python Developer",
            "company": "TechCorp Inc",
            "location": "San Francisco, CA",
            "description": "Build scalable web applications using Python, FastAPI, and modern technologies.",
            "salary_min": 120000,
            "salary_max": 180000,
            "remote": True,
            "job_type": "Full-time",
            "experience_level": "Senior",
            "url": "https://example.com/job1",
            "source": "CareerCoach.ai"
        },
        {
            "title": "Full Stack Engineer",
            "company": "StartupXYZ",
            "location": "Remote",
            "description": "Work with React, Node.js, and Python to build innovative products.",
            "salary_min": 100000,
            "salary_max": 150000,
            "remote": True,
            "job_type": "Full-time",
            "experience_level": "Mid-level",
            "url": "https://example.com/job2",
            "source": "CareerCoach.ai"
        },
        {
            "title": "Data Scientist",
            "company": "DataCorp",
            "location": "New York, NY",
            "description": "Analyze complex datasets using Python, SQL, and machine learning.",
            "salary_min": 110000,
            "salary_max": 160000,
            "remote": False,
            "job_type": "Full-time",
            "experience_level": "Senior",
            "url": "https://example.com/job3",
            "source": "CareerCoach.ai"
        }
    ]
    
    with SessionLocal() as session:
        for job_data in sample_jobs:
            job = JobPosting(**job_data)
            session.add(job)
        
        session.commit()
        print(f" Added {len(sample_jobs)} sample job postings")

def verify_database_setup():
    """Verify that databases are properly set up"""
    print("\n Verifying database setup...")
    
    databases = [
        ("careercoach.db", "Main database"),
        ("careercoach_performance.db", "Performance database")
    ]
    
    for db_file, description in databases:
        if os.path.exists(db_file):
            print(f" {description} found: {db_file}")
            
            # Check tables
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if tables:
                print(f"    Tables: {[table[0] for table in tables]}")
                
                # Count records in each table
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
                    count = cursor.fetchone()[0]
                    print(f"      {table[0]}: {count} records")
            else:
                print(f"     No tables found")
            
            conn.close()
        else:
            print(f" {description} not found: {db_file}")

def main():
    """Main setup function"""
    print(" CareerCoach.ai Database Setup Starting...\n")
    
    # Create database schema
    engine, perf_engine = create_database_schema()
    
    # Add sample data
    populate_sample_data()
    
    # Verify setup
    verify_database_setup()
    
    print("\n Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Update environment variables if needed")
    print("2. Test database connections in your application")
    print("3. Run performance monitoring tests")

if __name__ == "__main__":
    main()