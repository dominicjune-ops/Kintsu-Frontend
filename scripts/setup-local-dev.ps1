# CareerCoach.ai Local Development Environment Setup
# Run this script to set up your complete local development environment

Write-Host "🏠 Setting up CareerCoach.ai Local Development Environment" -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Green
Write-Host ""

# Check prerequisites
Write-Host " Checking prerequisites..." -ForegroundColor Yellow

# Check Docker
try {
    $dockerVersion = docker --version
    Write-Host " Docker: $dockerVersion" -ForegroundColor Green
}
catch {
    Write-Error " Docker not found. Please install Docker Desktop first."
    Write-Host "Download: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check Python
try {
    $pythonVersion = python --version
    Write-Host " Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Error " Python not found. Please install Python 3.11+ first."
    Write-Host "Download: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Create config directories
Write-Host "📁 Creating configuration directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "config\grafana\dashboards" | Out-Null
New-Item -ItemType Directory -Force -Path "config\grafana\datasources" | Out-Null
New-Item -ItemType Directory -Force -Path "data\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "data\processed" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

Write-Host " Directories created" -ForegroundColor Green

# Create MongoDB initialization script
Write-Host "🗄️ Creating MongoDB initialization..." -ForegroundColor Yellow
@"
// MongoDB initialization script for CareerCoach.ai local development

// Switch to CareerCoach database
db = db.getSiblingDB('careercoach_dev');

// Create collections
db.createCollection('job_postings');
db.createCollection('user_profiles');
db.createCollection('applications');
db.createCollection('resumes');
db.createCollection('companies');

// Create indexes for better performance
db.job_postings.createIndex({ "title": "text", "description": "text", "company": "text" });
db.job_postings.createIndex({ "posted_date": -1 });
db.job_postings.createIndex({ "location": 1 });
db.job_postings.createIndex({ "salary_range": 1 });

db.user_profiles.createIndex({ "email": 1 }, { unique: true });
db.user_profiles.createIndex({ "skills": 1 });

db.applications.createIndex({ "user_id": 1, "job_id": 1 });
db.applications.createIndex({ "application_date": -1 });

db.resumes.createIndex({ "user_id": 1 });
db.resumes.createIndex({ "upload_date": -1 });

db.companies.createIndex({ "name": 1 }, { unique: true });

// Insert sample data
db.job_postings.insertMany([
    {
        "_id": ObjectId(),
        "title": "Senior Python Developer",
        "company": "TechCorp",
        "location": "Remote",
        "salary_range": { "min": 80000, "max": 120000 },
        "description": "Looking for a senior Python developer with experience in web scraping and data processing.",
        "requirements": ["Python", "Django", "PostgreSQL", "Redis"],
        "posted_date": new Date(),
        "status": "active",
        "source": "manual"
    },
    {
        "_id": ObjectId(),
        "title": "Data Scientist",
        "company": "DataFlow Inc",
        "location": "San Francisco, CA",
        "salary_range": { "min": 90000, "max": 140000 },
        "description": "Seeking a data scientist to work on machine learning models for job matching.",
        "requirements": ["Python", "Machine Learning", "TensorFlow", "SQL"],
        "posted_date": new Date(),
        "status": "active",
        "source": "indeed"
    }
]);

db.companies.insertMany([
    {
        "_id": ObjectId(),
        "name": "TechCorp",
        "website": "https://techcorp.com",
        "industry": "Technology",
        "size": "51-200 employees",
        "description": "Leading technology company specializing in web development."
    },
    {
        "_id": ObjectId(),
        "name": "DataFlow Inc",
        "website": "https://dataflow.com",
        "industry": "Data Analytics",
        "size": "11-50 employees",
        "description": "Data analytics company focused on job market insights."
    }
]);

print(" CareerCoach.ai database initialized with sample data");
"@ | Out-File -FilePath "config\mongo-init.js" -Encoding UTF8

Write-Host " MongoDB initialization script created" -ForegroundColor Green

# Start Docker services
Write-Host ""
Write-Host "🐳 Starting Docker services..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Gray

docker-compose -f docker-compose-local.yml up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host " Docker services started successfully!" -ForegroundColor Green
} else {
    Write-Error " Failed to start Docker services"
    exit 1
}

# Summary
Write-Host ""
Write-Host " Local Development Environment Ready!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""
Write-Host " Service URLs:" -ForegroundColor Cyan
Write-Host "    Grafana Dashboard: http://localhost:3000 (admin/localdev123)" -ForegroundColor White
Write-Host "    Prometheus Metrics: http://localhost:9090" -ForegroundColor White
Write-Host "    MinIO Storage: http://localhost:9001 (careercoach/localdev123)" -ForegroundColor White
Write-Host "    Elasticsearch: http://localhost:9200" -ForegroundColor White
Write-Host "   🗄️ MongoDB: mongodb://localhost:27017" -ForegroundColor White
Write-Host "    Redis: localhost:6379" -ForegroundColor White
Write-Host ""
Write-Host " Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Start the API server: python app.py" -ForegroundColor White
Write-Host "   2. Access API docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   3. View monitoring: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host " Cost: FREE (runs entirely on your machine)" -ForegroundColor Green