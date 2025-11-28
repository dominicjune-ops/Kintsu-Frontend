#!/bin/bash

# Google Cloud Scheduler Setup for CareerCoach.ai Job Scraper
# This script sets up a Cloud Run Job that runs every 6 hours

# Configuration
PROJECT_ID="vernal-vine-476117-v4"
REGION="us-central1"
JOB_NAME="careercoach-job-scraper"
SERVICE_ACCOUNT="careercoach-scraper@${PROJECT_ID}.iam.gserviceaccount.com"
SCHEDULE="0 */6 * * *"  # Every 6 hours
DESCRIPTION="CareerCoach.ai scheduled job scraper"

echo " Setting up scheduled job scraper for CareerCoach.ai"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Schedule: Every 6 hours"

# 1. Build container image
echo "📦 Building container image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$JOB_NAME:latest --project $PROJECT_ID

# 2. Create Cloud Run Job
echo " Creating Cloud Run Job..."
gcloud run jobs create $JOB_NAME \
    --image gcr.io/$PROJECT_ID/$JOB_NAME:latest \
    --region $REGION \
    --project $PROJECT_ID \
    --max-retries 3 \
    --parallelism 1 \
    --task-count 1 \
    --task-timeout 3600 \
    --memory 1Gi \
    --cpu 1 \
    --set-env-vars "ENVIRONMENT=production" \
    --service-account $SERVICE_ACCOUNT

# 3. Create Cloud Scheduler job
echo "⏰ Creating Cloud Scheduler job..."
gcloud scheduler jobs create http ${JOB_NAME}-scheduler \
    --location $REGION \
    --schedule "$SCHEDULE" \
    --uri "https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/${JOB_NAME}:run" \
    --http-method POST \
    --headers "Authorization=Bearer $(gcloud auth print-access-token)" \
    --description "$DESCRIPTION" \
    --project $PROJECT_ID

echo " Scheduled scraper setup complete!"
echo ""
echo " The scraper will now run every 6 hours and collect jobs from:"
echo "   • Google Jobs (aggregates Indeed, LinkedIn, Glassdoor)"
echo "   • Software Engineer positions"
echo "   • Data Scientist roles"
echo "   • Remote opportunities"
echo "   • High-salary positions (100K+)"
echo ""
echo " Monitor with:"
echo "   gcloud run jobs describe $JOB_NAME --region $REGION"
echo "   gcloud scheduler jobs describe ${JOB_NAME}-scheduler --location $REGION"
echo ""
echo " Next steps:"
echo "   1. Set up MongoDB Atlas for job storage"
echo "   2. Add user notification system"
echo "   3. Implement job matching algorithm"