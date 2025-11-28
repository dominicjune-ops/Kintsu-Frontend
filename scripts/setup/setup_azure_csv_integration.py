#!/usr/bin/env python3
"""
Quick Setup Script for Azure DevOps CSV Integration
CareerCoach.ai Transparency Initiative
"""

import os
import json
import sys
from datetime import datetime

def create_environment_file():
    """Create .env file template for Azure DevOps integration"""
    env_content = """# Azure DevOps CSV Integration Environment Variables
# CareerCoach.ai Transparency Configuration

# Azure DevOps Settings
AZURE_DEVOPS_ORG=your-organization-name
AZURE_DEVOPS_PROJECT=CareerCoach.ai
AZURE_DEVOPS_PAT=your-personal-access-token

# File Paths
CSV_INPUT_PATH=./csv/careercoach_roadmap.csv
CSV_OUTPUT_PATH=./csv/exports/
REPORT_OUTPUT_PATH=./reports/
LOG_FILE_PATH=./logs/azure_devops_sync.log

# Notification Settings
NOTIFICATION_EMAIL=admin@careercoach.ai
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK

# Sync Settings
AUTO_SYNC_ENABLED=true
DRY_RUN_DEFAULT=true
SYNC_FREQUENCY=daily
BACKUP_BEFORE_SYNC=true

# Transparency Settings
GENERATE_PUBLIC_ROADMAP=true
STAKEHOLDER_VISIBILITY=true
AUDIT_LOGGING=true
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(" Created .env file template")
    print(" Please edit .env file with your Azure DevOps credentials")

def create_sample_csv():
    """Create sample CSV file showing expected format"""
    csv_content = """Title,Type,State,Priority,Epic,Feature,Story Points,Acceptance Criteria,Technical Notes,Business Impact,Dependencies,Risk Level
"Resume Tailoring Engine",Epic,New,1,"AI-Powered Resume Optimization","Resume Processing",40,"Implement AI-powered resume tailoring with OpenAI integration","Use FastAPI endpoints with multipart file handling","High user engagement and competitive differentiation","OpenAI API, File storage",Medium
"Resume Upload & Processing",Feature,New,1,"AI-Powered Resume Optimization","Resume Processing",13,"Support PDF/DOCX/TXT uploads with content extraction","Implement secure file handling and validation","Enable core functionality for resume optimization","python-multipart library",Low  
"AI Resume Tailoring",Feature,New,1,"AI-Powered Resume Optimization","AI Processing",21,"Tailor resumes for job descriptions with ATS scoring","OpenAI GPT integration with fallback mechanisms","Improve application success rates","OpenAI API availability",High
"Cover Letter Generation",Feature,New,2,"AI-Powered Resume Optimization","AI Processing",8,"Generate personalized cover letters from resume data","Template-based generation with company research","Streamline application process","Resume tailoring feature",Medium
"Optimization History",Feature,New,2,"AI-Powered Resume Optimization","Analytics",5,"Track user optimization history and analytics","Database schema for history tracking","Provide insights and reusability","Database optimization",Low
"User Analytics Dashboard",User Story,New,2,"Platform Enhancement","Analytics Dashboard",8,"Display user engagement and success metrics","Real-time dashboard with performance monitoring","Business insights for growth","Performance monitoring system",Medium
"Mobile Responsive Design",User Story,New,3,"Platform Enhancement","UI/UX",5,"Ensure platform works on mobile devices","Responsive CSS and mobile-first design","Increase user accessibility","Frontend framework updates",Low
"API Rate Limiting",Task,New,2,"Platform Enhancement","Infrastructure",3,"Implement rate limiting for API endpoints","Use Redis for rate limiting with sliding window","Prevent abuse and ensure stability","Redis infrastructure",Medium
"Security Audit",Task,New,1,"Platform Enhancement","Security",5,"Conduct comprehensive security review","Review authentication, input validation, data handling","Ensure production security standards","Security tools and expertise",High
"Performance Optimization",Task,Active,1,"Platform Enhancement","Performance",8,"Optimize database queries and API responses","Index optimization and query analysis","Improve user experience and scalability","Database monitoring tools",Medium"""
    
    # Create csv directory if it doesn't exist
    os.makedirs('csv', exist_ok=True)
    
    with open('csv/sample_careercoach_roadmap.csv', 'w') as f:
        f.write(csv_content)
    
    print(" Created sample CSV file: csv/sample_careercoach_roadmap.csv")
    print(" Use this as a template for your roadmap data")

def create_directory_structure():
    """Create necessary directory structure"""
    directories = [
        'csv',
        'csv/exports',
        'reports', 
        'logs',
        'config',
        'scripts'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def create_config_file():
    """Create configuration file for transparency settings"""
    config = {
        "transparency": {
            "enabled": True,
            "public_roadmap": True,
            "stakeholder_access": True,
            "audit_logging": True
        },
        "sync": {
            "auto_sync": True,
            "dry_run_default": True,
            "frequency": "daily",
            "backup_enabled": True
        },
        "notifications": {
            "email_enabled": True,
            "slack_enabled": False,
            "webhook_enabled": False
        },
        "quality_gates": {
            "required_fields": ["title", "description", "acceptance_criteria"],
            "validation_enabled": True,
            "auto_reject_invalid": False
        },
        "azure_devops": {
            "api_version": "7.1",
            "timeout": 30,
            "retry_attempts": 3
        }
    }
    
    with open('config/transparency_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(" Created transparency configuration: config/transparency_config.json")

def create_quick_test_script():
    """Create quick test script for validation"""
    test_script = """#!/usr/bin/env python3
\"\"\"
Quick Test Script for Azure DevOps CSV Integration
\"\"\"

import os
import sys
from azure_devops_csv_integrator import AzureDevOpsCSVIntegrator

def test_csv_integration():
    \"\"\"Test CSV integration without making changes\"\"\"
    
    # Check environment variables
    required_vars = ['AZURE_DEVOPS_ORG', 'AZURE_DEVOPS_PROJECT', 'AZURE_DEVOPS_PAT']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f" Missing environment variables: {', '.join(missing_vars)}")
        print(" Please set these in your .env file")
        return False
    
    # Test CSV file exists
    csv_file = os.getenv('CSV_INPUT_PATH', 'csv/sample_careercoach_roadmap.csv')
    if not os.path.exists(csv_file):
        print(f" CSV file not found: {csv_file}")
        print(" Please create your CSV file or use the sample")
        return False
    
    # Initialize integrator
    try:
        integrator = AzureDevOpsCSVIntegrator(
            organization=os.getenv('AZURE_DEVOPS_ORG'),
            project=os.getenv('AZURE_DEVOPS_PROJECT'), 
            personal_access_token=os.getenv('AZURE_DEVOPS_PAT')
        )
        
        # Test CSV reading
        csv_data = integrator.read_csv_file(csv_file)
        print(f" Successfully read {len(csv_data)} items from CSV")
        
        # Test transformation
        work_items = integrator.transform_csv_to_work_items(csv_data)
        print(f" Successfully transformed {len(work_items)} work items")
        
        # Test dry run sync
        results = integrator.sync_csv_to_azure_devops(csv_file, dry_run=True)
        print(f" Dry run completed: {results['total_items']} items would be processed")
        
        return True
        
    except Exception as e:
        print(f" Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("  python-dotenv not installed, using system environment")
    
    print(" Testing Azure DevOps CSV Integration...")
    success = test_csv_integration()
    
    if success:
        print("\\n All tests passed! You're ready to sync CSV data to Azure DevOps")
        print("\\n💡 Next steps:")
        print("   1. Review your CSV data")
        print("   2. Run with --dry-run to preview changes")
        print("   3. Execute actual sync when ready")
    else:
        print("\\n Tests failed. Please fix the issues above before proceeding.")
        sys.exit(1)
"""
    
    with open('scripts/test_integration.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print(" Created test script: scripts/test_integration.py")

def create_requirements_file():
    """Create requirements file for dependencies"""
    requirements = """# Azure DevOps CSV Integration Requirements
requests>=2.31.0
python-dotenv>=1.0.0
pandas>=2.0.0
openpyxl>=3.1.0

# Optional: For enhanced CSV processing
chardet>=5.2.0
python-dateutil>=2.8.2

# Optional: For notifications
slack-sdk>=3.21.0

# Optional: For enhanced logging
structlog>=23.2.0
"""
    
    with open('requirements-azure-csv.txt', 'w') as f:
        f.write(requirements)
    
    print(" Created requirements file: requirements-azure-csv.txt")
    print("💡 Install with: pip install -r requirements-azure-csv.txt")

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*60)
    print(" Azure DevOps CSV Integration Setup Complete!")
    print("="*60)
    
    print("\n Next Steps:")
    print("1. Edit .env file with your Azure DevOps credentials")
    print("2. Install dependencies: pip install -r requirements-azure-csv.txt") 
    print("3. Review sample CSV format: csv/sample_careercoach_roadmap.csv")
    print("4. Test integration: python scripts/test_integration.py")
    print("5. Run dry sync: python azure_devops_csv_integrator.py --dry-run --csv-file csv/your_file.csv")
    
    print("\n🔐 Azure DevOps Setup:")
    print("1. Generate Personal Access Token (PAT) in Azure DevOps")
    print("2. Grant these permissions: Work Items (Read, Write, Manage)")
    print("3. Add PAT to .env file as AZURE_DEVOPS_PAT")
    
    print("\n For Transparency:")
    print("1. Configure stakeholder access in Azure DevOps")
    print("2. Set up automated reporting schedule")
    print("3. Enable audit logging for compliance")
    
    print("\n📞 Support:")
    print("- Documentation: AZURE_DEVOPS_CSV_TRANSPARENCY.md")
    print("- Configuration: config/transparency_config.json")
    print("- Logs: logs/azure_devops_sync.log")

def main():
    """Main setup function"""
    print(" Setting up Azure DevOps CSV Integration for CareerCoach.ai")
    print("💡 This will create files and directories for transparency management")
    
    create_directory_structure()
    create_environment_file()
    create_sample_csv()
    create_config_file() 
    create_quick_test_script()
    create_requirements_file()
    print_next_steps()

if __name__ == "__main__":
    main()