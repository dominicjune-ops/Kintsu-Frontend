"""
Shared pytest fixtures for CareerCoach.ai test suite
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch
import json
from typing import Dict, Any, List


# ============================================================================
# TEST DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_user():
    """Sample user data for testing"""
    return {
        "id": "test-user-123",
        "email": "testuser@example.com",
        "name": "Test User",
        "created_at": datetime.now().isoformat(),
        "subscription_tier": "premium"
    }


@pytest.fixture
def sample_resume_data():
    """Sample resume data for parsing tests"""
    return {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "phone": "+1-555-0123",
        "location": "San Francisco, CA",
        "summary": "Experienced software engineer with 5 years in Python and cloud technologies",
        "skills": ["Python", "JavaScript", "AWS", "Docker", "PostgreSQL"],
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "start_date": "2020-01",
                "end_date": "present",
                "description": "Lead backend development using Python and AWS"
            },
            {
                "title": "Software Engineer",
                "company": "StartUp Inc",
                "location": "Remote",
                "start_date": "2018-06",
                "end_date": "2020-01",
                "description": "Full-stack development with React and Node.js"
            }
        ],
        "education": [
            {
                "degree": "BS Computer Science",
                "institution": "University of California",
                "graduation_year": "2018"
            }
        ]
    }


@pytest.fixture
def sample_job_posting():
    """Sample job posting for matching tests"""
    return {
        "id": "job-456",
        "title": "Senior Python Developer",
        "company": "Innovative Tech",
        "location": "San Francisco, CA",
        "description": "We're looking for a senior Python developer with AWS experience...",
        "requirements": [
            "5+ years Python experience",
            "AWS cloud services",
            "Docker containerization",
            "PostgreSQL database"
        ],
        "salary_min": 120000,
        "salary_max": 180000,
        "posted_date": datetime.now().isoformat(),
        "job_type": "full-time",
        "remote": False
    }


@pytest.fixture
def sample_job_list():
    """List of sample job postings"""
    return [
        {
            "id": f"job-{i}",
            "title": f"Software Engineer {i}",
            "company": f"Company {i}",
            "location": "Remote" if i % 2 == 0 else "San Francisco, CA",
            "salary_min": 100000 + (i * 10000),
            "salary_max": 150000 + (i * 10000),
            "skills": ["Python", "AWS"] if i % 2 == 0 else ["JavaScript", "React"]
        }
        for i in range(1, 6)
    ]


@pytest.fixture
def sample_cover_letter():
    """Sample cover letter data"""
    return {
        "job_id": "job-456",
        "user_id": "test-user-123",
        "content": "Dear Hiring Manager,\n\nI am writing to express...",
        "tone": "professional",
        "length": "medium"
    }


@pytest.fixture
def sample_interview_data():
    """Sample interview preparation data"""
    return {
        "job_id": "job-456",
        "company": "Innovative Tech",
        "position": "Senior Python Developer",
        "interview_type": "technical",
        "questions": [
            "Explain the difference between lists and tuples in Python",
            "How would you optimize a slow database query?",
            "Describe your experience with AWS services"
        ]
    }


# ============================================================================
# MOCK FIXTURES
# ============================================================================

@pytest.fixture
def mock_db():
    """Mock database connection"""
    db = Mock()
    db.query.return_value = Mock()
    db.execute.return_value = Mock(rowcount=1)
    db.commit.return_value = None
    return db


@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client"""
    client = Mock()
    
    # Mock table operations
    table_mock = Mock()
    table_mock.select.return_value = table_mock
    table_mock.insert.return_value = table_mock
    table_mock.update.return_value = table_mock
    table_mock.delete.return_value = table_mock
    table_mock.eq.return_value = table_mock
    table_mock.execute.return_value = Mock(data=[{"id": 1}])
    
    client.table.return_value = table_mock
    client.auth.sign_in.return_value = Mock(user={"id": "test-user-123"})
    
    return client


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client"""
    client = Mock()
    
    # Mock chat completions
    response = Mock()
    response.choices = [
        Mock(message=Mock(content="This is a test response"))
    ]
    response.usage = Mock(total_tokens=100)
    
    client.chat.completions.create.return_value = response
    
    return client


@pytest.fixture
def mock_stripe_client():
    """Mock Stripe client"""
    client = Mock()
    
    # Mock payment methods
    client.PaymentIntent.create.return_value = Mock(
        id="pi_test_123",
        status="succeeded"
    )
    
    client.Customer.create.return_value = Mock(
        id="cus_test_123"
    )
    
    client.Subscription.create.return_value = Mock(
        id="sub_test_123",
        status="active"
    )
    
    return client


@pytest.fixture
def mock_redis_client():
    """Mock Redis client"""
    client = Mock()
    client.get.return_value = None
    client.set.return_value = True
    client.delete.return_value = 1
    client.exists.return_value = False
    return client


@pytest.fixture
def mock_service_bus_connection():
    """Mock Azure Service Bus connection"""
    connection = MagicMock()
    connection.send = MagicMock()
    connection.close = MagicMock()
    return connection


@pytest.fixture
def indeed_connector(mock_service_bus_connection):
    """Mock Indeed connector"""
    from src.connectors.indeed_connector import IndeedConnector
    return IndeedConnector(
        service_bus_connection=mock_service_bus_connection
    )


# ============================================================================
# API & REQUEST FIXTURES
# ============================================================================

@pytest.fixture
def mock_api_request():
    """Mock API request object"""
    request = Mock()
    request.headers = {
        "Authorization": "Bearer test-token-123",
        "Content-Type": "application/json"
    }
    request.json = {
        "user_id": "test-user-123",
        "action": "search_jobs"
    }
    request.method = "POST"
    request.path = "/api/jobs/search"
    return request


@pytest.fixture
def mock_authenticated_user():
    """Mock authenticated user from request"""
    return {
        "id": "test-user-123",
        "email": "testuser@example.com",
        "role": "premium",
        "token": "test-token-123"
    }


# ============================================================================
# FILE & DOCUMENT FIXTURES
# ============================================================================

@pytest.fixture
def sample_pdf_content():
    """Sample PDF content (as bytes)"""
    # This is a minimal PDF structure
    return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 2\ntrailer\n<<\n/Size 2\n/Root 1 0 R\n>>\nstartxref\n%%EOF"


@pytest.fixture
def sample_docx_content():
    """Sample DOCX content (as bytes)"""
    # Minimal DOCX structure
    return b"PK\x03\x04" + b"\x00" * 100  # DOCX header


@pytest.fixture
def sample_text_resume():
    """Sample plain text resume"""
    return """
JANE DOE
jane.doe@example.com | +1-555-0123
San Francisco, CA

SUMMARY
Experienced software engineer with 5 years in Python and cloud technologies

SKILLS
Python, JavaScript, AWS, Docker, PostgreSQL

EXPERIENCE
Senior Software Engineer | Tech Corp | 2020 - Present
- Lead backend development using Python and AWS
- Improved system performance by 40%

Software Engineer | StartUp Inc | 2018 - 2020
- Full-stack development with React and Node.js

EDUCATION
BS Computer Science | University of California | 2018
"""


# ============================================================================
# CONFIGURATION FIXTURES
# ============================================================================

@pytest.fixture
def test_config():
    """Test configuration"""
    return {
        "DATABASE_URL": "postgresql://test:test@localhost:5432/test_db",
        "REDIS_URL": "redis://localhost:6379/0",
        "OPENAI_API_KEY": "test-openai-key",
        "STRIPE_API_KEY": "test-stripe-key",
        "JWT_SECRET": "test-jwt-secret",
        "ENV": "test",
        "DEBUG": True
    }


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch, test_config):
    """Automatically mock environment variables for all tests"""
    for key, value in test_config.items():
        monkeypatch.setenv(key, str(value))


# ============================================================================
# TIME & DATE FIXTURES
# ============================================================================

@pytest.fixture
def frozen_time():
    """Freeze time for consistent date/time testing"""
    from freezegun import freeze_time
    with freeze_time("2024-01-15 12:00:00"):
        yield datetime(2024, 1, 15, 12, 0, 0)


@pytest.fixture
def recent_timestamp():
    """Recent timestamp for testing"""
    return datetime.now() - timedelta(hours=1)


# ============================================================================
# CLEANUP FIXTURES
# ============================================================================

@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file for testing"""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Test content")
    yield file_path
    # Cleanup happens automatically with tmp_path


@pytest.fixture
def mock_cleanup():
    """Track and cleanup mocks"""
    mocks = []
    
    def register_mock(mock_obj):
        mocks.append(mock_obj)
        return mock_obj
    
    yield register_mock
    
    # Cleanup
    for mock in mocks:
        if hasattr(mock, 'reset_mock'):
            mock.reset_mock()


# ============================================================================
# PYTEST MARKERS
# ============================================================================

def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests (fast)")
    config.addinivalue_line("markers", "integration: Integration tests (slower)")
    config.addinivalue_line("markers", "e2e: End-to-end tests (slowest)")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "smoke: Smoke tests for quick validation")
    config.addinivalue_line("markers", "critical: Critical path tests")
    config.addinivalue_line("markers", "requires_db: Tests that need database")
    config.addinivalue_line("markers", "requires_api: Tests that need external API")


# ============================================================================
# SESSION-LEVEL FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def session_config():
    """Session-level configuration that persists across all tests"""
    return {
        "test_run_id": f"test-run-{datetime.now().timestamp()}",
        "parallel_workers": 4
    }
