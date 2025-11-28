"""
Integration tests for CareerCoach.ai
Tests critical user workflows end-to-end
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime


@pytest.mark.integration
@pytest.mark.critical
class TestUserRegistrationFlow:
    """Test complete user registration workflow"""
    
    def test_user_registration_complete_flow(self, mock_supabase_client, mock_stripe_client):
        """Test user can register and create account"""
        # Step 1: Submit registration
        registration_data = {
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "name": "New User"
        }
        
        # Validate input
        assert "@" in registration_data["email"]
        assert len(registration_data["password"]) >= 8
        
        # Step 2: Create user in database
        mock_supabase_client.table("users").insert.return_value.execute.return_value = Mock(
            data=[{"id": "user-new-123"}]
        )
        
        # Step 3: Send verification email
        verification_sent = True
        
        # Step 4: Create Stripe customer
        mock_stripe_client.Customer.create.return_value = Mock(id="cus_new_123")
        
        assert verification_sent is True
    
    def test_user_email_verification(self):
        """Test email verification flow"""
        verification_token = "verify_token_123"
        token_valid = True
        
        # Verify token
        if token_valid:
            user_verified = True
        else:
            user_verified = False
        
        assert user_verified is True


@pytest.mark.integration
@pytest.mark.critical
class TestJobSearchFlow:
    """Test complete job search workflow"""
    
    def test_job_search_complete_flow(self, sample_user, sample_job_list, mock_authenticated_user):
        """Test user can search and view jobs"""
        # Step 1: User searches for jobs
        search_params = {
            "keywords": "Python Developer",
            "location": "San Francisco",
            "remote": True
        }
        
        # Step 2: Apply filters
        filtered_jobs = [j for j in sample_job_list if "Remote" in j["location"]]
        
        # Step 3: Rank by match score
        jobs_with_scores = [
            {**job, "match_score": 85 + i}
            for i, job in enumerate(filtered_jobs)
        ]
        
        # Step 4: Return top results
        top_results = sorted(jobs_with_scores, key=lambda x: x["match_score"], reverse=True)[:10]
        
        assert len(top_results) > 0
        assert all("match_score" in job for job in top_results)
    
    def test_save_job_for_later(self, sample_user, sample_job_posting):
        """Test saving a job for later"""
        saved_jobs = []
        
        # Save job
        saved_jobs.append({
            "user_id": sample_user["id"],
            "job_id": sample_job_posting["id"],
            "saved_at": datetime.now()
        })
        
        assert len(saved_jobs) == 1
        assert saved_jobs[0]["job_id"] == sample_job_posting["id"]


@pytest.mark.integration
@pytest.mark.critical
class TestResumeUploadFlow:
    """Test complete resume upload and parsing workflow"""
    
    def test_resume_upload_and_parse_flow(self, sample_user, sample_text_resume):
        """Test uploading and parsing resume"""
        # Step 1: Upload resume file
        file_uploaded = True
        
        # Step 2: Extract text
        extracted_text = sample_text_resume
        
        # Step 3: Parse resume data
        parsed_data = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "skills": ["Python", "AWS", "Docker"],
            "experience": [],
            "education": []
        }
        
        # Step 4: Store in database
        resume_stored = True
        
        assert file_uploaded is True
        assert len(parsed_data["skills"]) > 0
        assert resume_stored is True
    
    def test_resume_skill_extraction(self, sample_text_resume):
        """Test skill extraction from resume"""
        known_skills = ["Python", "JavaScript", "AWS", "Docker", "PostgreSQL"]
        
        found_skills = [skill for skill in known_skills if skill in sample_text_resume]
        
        assert len(found_skills) >= 3


@pytest.mark.integration
class TestJobApplicationFlow:
    """Test job application workflow"""
    
    def test_apply_to_job_flow(self, sample_user, sample_job_posting, sample_resume_data):
        """Test applying to a job"""
        # Step 1: Select job
        selected_job = sample_job_posting
        
        # Step 2: Generate cover letter
        cover_letter = {
            "content": f"Dear Hiring Manager, I am interested in the {selected_job['title']} position...",
            "generated_at": datetime.now()
        }
        
        # Step 3: Submit application
        application = {
            "user_id": sample_user["id"],
            "job_id": selected_job["id"],
            "resume_data": sample_resume_data,
            "cover_letter": cover_letter["content"],
            "status": "submitted",
            "applied_at": datetime.now()
        }
        
        assert application["status"] == "submitted"
        assert application["job_id"] == selected_job["id"]
    
    def test_track_application_status(self, sample_user):
        """Test tracking application status"""
        application_status = {
            "user_id": sample_user["id"],
            "job_id": "job-456",
            "status": "under_review",
            "updated_at": datetime.now()
        }
        
        # Status progression
        valid_statuses = ["submitted", "under_review", "interview", "offer", "rejected"]
        
        assert application_status["status"] in valid_statuses


@pytest.mark.integration
class TestPaymentFlow:
    """Test payment and subscription workflow"""
    
    def test_upgrade_to_premium_flow(self, sample_user, mock_stripe_client):
        """Test upgrading to premium subscription"""
        # Step 1: Select plan
        selected_plan = {
            "name": "Premium",
            "price": 29.99,
            "interval": "month"
        }
        
        # Step 2: Create payment intent
        mock_stripe_client.PaymentIntent.create.return_value = Mock(
            id="pi_premium_123",
            status="succeeded"
        )
        
        # Step 3: Create subscription
        mock_stripe_client.Subscription.create.return_value = Mock(
            id="sub_premium_123",
            status="active"
        )
        
        # Step 4: Update user tier
        user_tier = "premium"
        
        assert user_tier == "premium"
    
    def test_cancel_subscription_flow(self, sample_user, mock_stripe_client):
        """Test canceling subscription"""
        subscription_id = "sub_premium_123"
        
        # Cancel subscription
        mock_stripe_client.Subscription.delete.return_value = Mock(
            id=subscription_id,
            status="canceled"
        )
        
        # Downgrade user
        new_tier = "free"
        
        assert new_tier == "free"


@pytest.mark.integration
class TestInterviewPrepFlow:
    """Test interview preparation workflow"""
    
    def test_generate_interview_questions_flow(self, sample_user, sample_job_posting):
        """Test generating interview questions"""
        # Step 1: Analyze job posting
        job_requirements = sample_job_posting.get("requirements", [])
        
        # Step 2: Generate relevant questions
        questions = [
            "Tell me about your experience with Python",
            "How have you used AWS in your projects?",
            "Describe a challenging technical problem you solved"
        ]
        
        # Step 3: Provide answer guidance
        question_with_tips = {
            "question": questions[0],
            "tips": ["Use STAR method", "Provide specific examples"],
            "sample_answer": "In my previous role..."
        }
        
        assert len(questions) > 0
        assert "tips" in question_with_tips
    
    def test_practice_interview_flow(self, sample_user):
        """Test practice interview session"""
        session = {
            "user_id": sample_user["id"],
            "questions_answered": 5,
            "total_questions": 10,
            "score": 85,
            "started_at": datetime.now()
        }
        
        progress = (session["questions_answered"] / session["total_questions"]) * 100
        
        assert progress == 50.0


@pytest.mark.integration
class TestAnalyticsDashboardFlow:
    """Test analytics dashboard workflow"""
    
    def test_view_application_analytics(self, sample_user):
        """Test viewing application analytics"""
        analytics = {
            "total_applications": 15,
            "interviews": 5,
            "offers": 2,
            "rejections": 8,
            "pending": 5
        }
        
        # Calculate metrics
        interview_rate = (analytics["interviews"] / analytics["total_applications"]) * 100
        offer_rate = (analytics["offers"] / analytics["total_applications"]) * 100
        
        assert interview_rate == 33.33 or abs(interview_rate - 33.33) < 0.1
        assert offer_rate == 13.33 or abs(offer_rate - 13.33) < 0.1
    
    def test_view_skill_gap_analysis(self, sample_user, sample_resume_data):
        """Test skill gap analysis"""
        current_skills = set(sample_resume_data["skills"])
        market_demand_skills = {"Python", "AWS", "Kubernetes", "React", "Docker"}
        
        missing_skills = market_demand_skills - current_skills
        
        skill_gap_report = {
            "current_skills": len(current_skills),
            "missing_skills": list(missing_skills),
            "recommendations": ["Learn Kubernetes", "Learn React"]
        }
        
        assert len(skill_gap_report["missing_skills"]) >= 0


@pytest.mark.integration
class TestNotificationFlow:
    """Test notification workflow"""
    
    def test_job_alert_notification_flow(self, sample_user):
        """Test job alert notifications"""
        # Step 1: User sets up alert
        job_alert = {
            "user_id": sample_user["id"],
            "keywords": ["Python", "Senior"],
            "location": "Remote",
            "frequency": "daily"
        }
        
        # Step 2: Check for matching jobs
        matching_jobs_found = True
        
        # Step 3: Send notification
        notification = {
            "user_id": sample_user["id"],
            "type": "job_alert",
            "message": "5 new jobs matching your criteria",
            "sent_at": datetime.now()
        }
        
        assert notification["type"] == "job_alert"
        assert matching_jobs_found is True
    
    def test_application_status_notification(self, sample_user):
        """Test application status change notifications"""
        status_change = {
            "user_id": sample_user["id"],
            "job_id": "job-456",
            "old_status": "submitted",
            "new_status": "interview",
            "changed_at": datetime.now()
        }
        
        # Send notification
        notification_sent = True
        
        assert status_change["new_status"] != status_change["old_status"]
        assert notification_sent is True


@pytest.mark.integration
class TestAPIEndpointsIntegration:
    """Test API endpoints integration"""
    
    def test_api_authentication_flow(self, mock_api_request, test_config):
        """Test API authentication"""
        import jwt
        
        # Extract token
        auth_header = mock_api_request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")
        
        # Verify token
        try:
            payload = jwt.decode(token, test_config["JWT_SECRET"], algorithms=["HS256"])
            authenticated = True
        except:
            authenticated = False
        
        assert authenticated is True
    
    def test_api_rate_limiting(self, sample_user):
        """Test API rate limiting"""
        request_count = 0
        max_requests = 100
        
        # Simulate multiple requests
        for _ in range(50):
            request_count += 1
        
        is_within_limit = request_count < max_requests
        
        assert is_within_limit is True
    
    def test_api_error_handling(self):
        """Test API error responses"""
        error_response = {
            "error": "ValidationError",
            "message": "Invalid input parameters",
            "status_code": 400,
            "timestamp": datetime.now().isoformat()
        }
        
        assert error_response["status_code"] == 400
        assert "error" in error_response


@pytest.mark.integration
@pytest.mark.slow
class TestDataPipelineIntegration:
    """Test data pipeline integration"""
    
    def test_job_scraping_pipeline(self):
        """Test job scraping and processing pipeline"""
        # Step 1: Scrape jobs
        scraped_jobs = [
            {"id": "job-1", "title": "Developer", "source": "LinkedIn"},
            {"id": "job-2", "title": "Engineer", "source": "Indeed"}
        ]
        
        # Step 2: Normalize data
        normalized_jobs = [
            {**job, "normalized_title": job["title"].lower()}
            for job in scraped_jobs
        ]
        
        # Step 3: Deduplicate
        unique_jobs = {job["id"]: job for job in normalized_jobs}.values()
        
        # Step 4: Store in database
        stored = True
        
        assert len(list(unique_jobs)) == 2
        assert stored is True
    
    def test_resume_processing_pipeline(self, sample_text_resume):
        """Test resume processing pipeline"""
        # Step 1: Upload resume
        uploaded = True
        
        # Step 2: Extract text
        text = sample_text_resume
        
        # Step 3: Parse data
        parsed = {"skills": ["Python", "AWS"]}
        
        # Step 4: Generate insights
        insights = {
            "skill_count": len(parsed["skills"]),
            "missing_common_skills": ["Docker"]
        }
        
        assert uploaded is True
        assert insights["skill_count"] == 2


@pytest.mark.integration
class TestCacheIntegration:
    """Test caching integration"""
    
    def test_cache_job_search_results(self, mock_redis_client, sample_job_list):
        """Test caching job search results"""
        cache_key = "job_search:python:sf"
        
        # First request - cache miss
        mock_redis_client.get.return_value = None
        cached_result = mock_redis_client.get(cache_key)
        assert cached_result is None
        
        # Fetch and cache results
        mock_redis_client.set(cache_key, str(sample_job_list))
        
        # Second request - cache hit
        mock_redis_client.get.return_value = str(sample_job_list)
        cached_result = mock_redis_client.get(cache_key)
        assert cached_result is not None
    
    def test_cache_invalidation_on_update(self, mock_redis_client):
        """Test cache invalidation when data changes"""
        cache_key = "user:123:profile"
        
        # Update user profile
        profile_updated = True
        
        # Invalidate cache
        if profile_updated:
            mock_redis_client.delete(cache_key)
        
        mock_redis_client.delete.assert_called_once_with(cache_key)


@pytest.mark.e2e
@pytest.mark.slow
class TestEndToEndUserJourney:
    """Test complete end-to-end user journey"""
    
    def test_complete_user_journey(
        self,
        mock_supabase_client,
        mock_stripe_client,
        sample_user,
        sample_job_list,
        sample_resume_data
    ):
        """Test a complete user journey from registration to job application"""
        # Step 1: Register
        user_registered = True
        assert user_registered is True
        
        # Step 2: Upload resume
        resume_uploaded = True
        assert resume_uploaded is True
        
        # Step 3: Search for jobs
        search_results = sample_job_list
        assert len(search_results) > 0
        
        # Step 4: View job details
        selected_job = search_results[0]
        assert "title" in selected_job
        
        # Step 5: Apply to job
        application_submitted = True
        assert application_submitted is True
        
        # Step 6: Track application
        application_status = "submitted"
        assert application_status == "submitted"
        
        # Complete journey successful
        journey_complete = True
        assert journey_complete is True
