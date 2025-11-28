"""Seed database with development and testing data."""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
import uuid

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from database.config import get_db, SessionLocal
from database.models import User, Resume, Job, Application, ApplicationStatus, ApplicationPriority


def create_demo_user(db):
    """Create a demo user account."""
    user = User(
        email="demo@careercoach.ai",
        full_name="Demo User",
        phone="+1-555-0123",
        location="San Francisco, CA",
        bio="Experienced software engineer looking for new opportunities in AI/ML space.",
        linkedin_url="https://linkedin.com/in/demouser",
        portfolio_url="https://demouser.dev",
        is_active=True,
        is_verified=True,
        preferred_job_types="full_time,remote",
        preferred_locations="San Francisco,Remote,New York",
        target_salary_min=120000,
        target_salary_max=180000
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f" Created demo user: {user.email} (ID: {user.id})")
    return user


def create_demo_resume(db, user: User):
    """Create a demo resume for the user."""
    resume_content = b"DEMO RESUME - This would be actual PDF/DOCX binary content"
    
    resume = Resume(
        user_id=user.id,
        filename="demo_resume.pdf",
        title="Senior Software Engineer Resume",
        version=1,
        is_tailored=False,
        is_default=True,
        content=resume_content,
        content_type="application/pdf",
        file_size=len(resume_content),
        parsed_text="John Doe\nSenior Software Engineer\n\nEXPERIENCE\n- 5 years at Tech Corp\n- 3 years at Startup Inc\n\nSKILLS\n- Python, JavaScript, React\n- AWS, Docker, Kubernetes\n- Machine Learning, Data Science",
        parsed_data={
            "name": "Demo User",
            "title": "Senior Software Engineer",
            "experience_years": 8,
            "skills": ["Python", "JavaScript", "React", "AWS", "Docker", "Kubernetes", "Machine Learning"],
            "experience": [
                {"company": "Tech Corp", "duration": "5 years", "role": "Senior Engineer"},
                {"company": "Startup Inc", "duration": "3 years", "role": "Full Stack Engineer"}
            ],
            "education": [
                {"degree": "BS Computer Science", "school": "University of California", "year": 2015}
            ]
        },
        ats_score=85,
        ats_feedback={
            "strengths": ["Strong technical skills", "Good experience", "Clean formatting"],
            "improvements": ["Add more keywords", "Quantify achievements", "Include certifications"]
        }
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    print(f" Created demo resume: {resume.filename} (ID: {resume.id})")
    return resume


def create_sample_jobs(db):
    """Create sample job postings."""
    jobs_data = [
        {
            "title": "Senior Python Developer",
            "company": "Tech Corp",
            "location": "San Francisco, CA",
            "remote": True,
            "remote_type": "hybrid",
            "job_type": "full_time",
            "experience_level": "senior",
            "salary_min": 140000,
            "salary_max": 180000,
            "description": "We're looking for an experienced Python developer to join our AI team...",
            "source": "company_website",
            "posted_date": datetime.now(timezone.utc).date() - timedelta(days=5)
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AI Startup",
            "location": "Remote",
            "remote": True,
            "remote_type": "fully_remote",
            "job_type": "full_time",
            "experience_level": "mid",
            "salary_min": 120000,
            "salary_max": 160000,
            "description": "Join our team building cutting-edge ML models...",
            "source": "linkedin",
            "posted_date": datetime.now(timezone.utc).date() - timedelta(days=3)
        },
        {
            "title": "Full Stack Engineer",
            "company": "Growth Company",
            "location": "New York, NY",
            "remote": True,
            "remote_type": "hybrid",
            "job_type": "full_time",
            "experience_level": "mid",
            "salary_min": 110000,
            "salary_max": 150000,
            "description": "Build amazing user experiences with React and Node.js...",
            "source": "indeed",
            "posted_date": datetime.now(timezone.utc).date() - timedelta(days=7)
        },
        {
            "title": "DevOps Engineer",
            "company": "Cloud Services Inc",
            "location": "Austin, TX",
            "remote": True,
            "remote_type": "hybrid",
            "job_type": "full_time",
            "experience_level": "senior",
            "salary_min": 130000,
            "salary_max": 170000,
            "description": "Manage infrastructure and deployment pipelines...",
            "source": "company_website",
            "posted_date": datetime.now(timezone.utc).date() - timedelta(days=2)
        },
        {
            "title": "Data Scientist",
            "company": "Analytics Firm",
            "location": "Boston, MA",
            "remote": False,
            "remote_type": "on_site",
            "job_type": "full_time",
            "experience_level": "mid",
            "salary_min": 115000,
            "salary_max": 145000,
            "description": "Analyze data and build predictive models...",
            "source": "google_jobs",
            "posted_date": datetime.now(timezone.utc).date() - timedelta(days=10)
        }
    ]
    
    jobs = []
    for job_data in jobs_data:
        job = Job(
            external_id=f"ext_{uuid.uuid4().hex[:8]}",
            is_active=True,
            salary_range=f"${job_data['salary_min']:,}-${job_data['salary_max']:,}",
            requirements={
                "required_skills": ["Python", "Git", "API Design"] if "Python" in job_data["title"] else ["JavaScript", "React", "Node.js"],
                "years_experience": 5 if job_data["experience_level"] == "senior" else 3,
                "education": "Bachelor's degree in Computer Science or related field"
            },
            keywords=["software", "development", "engineering", "tech"],
            required_skills=["Python", "AWS"] if "Python" in job_data["title"] else ["JavaScript", "React"],
            preferred_skills=["Docker", "Kubernetes", "Machine Learning"],
            source_url=f"https://example.com/jobs/{uuid.uuid4().hex[:8]}",
            **job_data
        )
        db.add(job)
        jobs.append(job)
    
    db.commit()
    for job in jobs:
        db.refresh(job)
        print(f" Created job: {job.title} at {job.company} (ID: {job.id})")
    
    return jobs


def create_demo_applications(db, user: User, resume: Resume, jobs: list[Job]):
    """Create demo applications."""
    applications_data = [
        {
            "job": jobs[0],  # Senior Python Developer
            "status": ApplicationStatus.INTERVIEWING,
            "priority": ApplicationPriority.HIGH,
            "applied_date": datetime.now(timezone.utc) - timedelta(days=10),
            "first_response_date": datetime.now(timezone.utc) - timedelta(days=7),
            "interview_date": datetime.now(timezone.utc) + timedelta(days=2),
            "notes": "Great opportunity! Had initial screening, technical interview scheduled.",
            "match_score": 92,
            "salary_expectation_min": 150000,
            "salary_expectation_max": 180000
        },
        {
            "job": jobs[1],  # Machine Learning Engineer
            "status": ApplicationStatus.APPLIED,
            "priority": ApplicationPriority.HIGH,
            "applied_date": datetime.now(timezone.utc) - timedelta(days=5),
            "notes": "Interesting ML role, waiting for response.",
            "match_score": 88,
            "salary_expectation_min": 130000,
            "salary_expectation_max": 160000
        },
        {
            "job": jobs[2],  # Full Stack Engineer
            "status": ApplicationStatus.SCREENING,
            "priority": ApplicationPriority.MEDIUM,
            "applied_date": datetime.now(timezone.utc) - timedelta(days=8),
            "first_response_date": datetime.now(timezone.utc) - timedelta(days=5),
            "follow_up_date": datetime.now(timezone.utc) + timedelta(days=3),
            "notes": "Recruiter screening completed, waiting for next steps.",
            "match_score": 78,
            "salary_expectation_min": 120000,
            "salary_expectation_max": 150000
        },
        {
            "job": jobs[3],  # DevOps Engineer
            "status": ApplicationStatus.OFFER,
            "priority": ApplicationPriority.URGENT,
            "applied_date": datetime.now(timezone.utc) - timedelta(days=15),
            "first_response_date": datetime.now(timezone.utc) - timedelta(days=12),
            "interview_date": datetime.now(timezone.utc) - timedelta(days=5),
            "offer_date": datetime.now(timezone.utc) - timedelta(days=1),
            "decision_deadline": datetime.now(timezone.utc) + timedelta(days=7),
            "notes": "Received offer! Need to review and decide.",
            "match_score": 85,
            "salary_expectation_min": 140000,
            "salary_expectation_max": 170000,
            "salary_offered": "$155,000",
            "salary_offered_amount": 155000
        },
        {
            "job": jobs[4],  # Data Scientist
            "status": ApplicationStatus.REJECTED,
            "priority": ApplicationPriority.LOW,
            "applied_date": datetime.now(timezone.utc) - timedelta(days=20),
            "first_response_date": datetime.now(timezone.utc) - timedelta(days=15),
            "notes": "Not selected for this role. They wanted someone with more DS experience.",
            "match_score": 72,
            "salary_expectation_min": 120000,
            "salary_expectation_max": 145000
        }
    ]
    
    for app_data in applications_data:
        job = app_data.pop("job")
        application = Application(
            user_id=user.id,
            job_id=job.id,
            resume_id=resume.id,
            cover_letter=f"Dear Hiring Manager,\n\nI am excited to apply for the {job.title} position at {job.company}...",
            tracking_number=f"APP-{uuid.uuid4().hex[:8].upper()}",
            application_url=f"https://example.com/applications/{uuid.uuid4().hex[:8]}",
            contact_person="Jane Recruiter" if app_data["status"] != ApplicationStatus.APPLIED else None,
            contact_email=f"recruiter@{job.company.lower().replace(' ', '')}.com" if app_data["status"] != ApplicationStatus.APPLIED else None,
            match_reasoning=f"Strong match for {job.title} based on Python and AWS experience." if "Python" in job.title else f"Good fit for {job.title} role.",
            **app_data
        )
        db.add(application)
    
    db.commit()
    print(f" Created {len(applications_data)} demo applications")


def seed_database():
    """Seed database with demo data."""
    print("\n=== Seeding Database ===\n")
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"  Database already has {existing_users} users. Skipping seed.")
            print("   To re-seed, drop the database first: python scripts/drop_database.py")
            return
        
        # Create demo data
        user = create_demo_user(db)
        resume = create_demo_resume(db, user)
        jobs = create_sample_jobs(db)
        create_demo_applications(db, user, resume, jobs)
        
        print("\n Database seeded successfully!")
        print(f"\nDemo User Credentials:")
        print(f"  Email: {user.email}")
        print(f"  User ID: {user.id}")
        
    except Exception as e:
        print(f"\n Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
