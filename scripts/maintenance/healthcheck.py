#!/usr/bin/env python3
"""
Comprehensive Health Check for CareerCoach.ai Platform
Verifies all systems, databases, APIs, and integrations
"""

import os
import sys
import sqlite3
import asyncio
import psutil
from datetime import datetime
from pathlib import Path

def print_header(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)

def print_status(item, status, details=""):
    """Print formatted status line"""
    emoji = "" if status else ""
    print(f"{emoji} {item:<40} {details}")

def check_system_resources():
    """Check system resource usage"""
    print_header("SYSTEM RESOURCES")
    
    # Memory usage
    memory = psutil.virtual_memory()
    memory_ok = memory.percent < 80
    print_status("Memory Usage", memory_ok, f"{memory.percent:.1f}% used")
    
    # Disk usage
    disk = psutil.disk_usage(".")
    disk_ok = disk.percent < 90
    print_status("Disk Usage", disk_ok, f"{disk.percent:.1f}% used")
    
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_ok = cpu_percent < 80
    print_status("CPU Usage", cpu_ok, f"{cpu_percent:.1f}% used")
    
    return memory_ok and disk_ok and cpu_ok

def check_python_environment():
    """Check Python environment and packages"""
    print_header("PYTHON ENVIRONMENT")
    
    # Python version
    python_version = sys.version.split()[0]
    python_ok = sys.version_info >= (3, 8)
    print_status("Python Version", python_ok, f"v{python_version}")
    
    # Virtual environment
    venv_ok = sys.prefix != sys.base_prefix
    print_status("Virtual Environment", venv_ok, "Active" if venv_ok else "Not active")
    
    # Key packages
    key_packages = [
        "fastapi", "uvicorn", "sqlalchemy", "pydantic", 
        "aiohttp", "psutil", "structlog", "notion_client"
    ]
    
    all_packages_ok = True
    for package in key_packages:
        try:
            __import__(package)
            print_status(f"Package: {package}", True, "Installed")
        except ImportError:
            print_status(f"Package: {package}", False, "Not found")
            all_packages_ok = False
    
    return python_ok and venv_ok and all_packages_ok

def check_databases():
    """Check database files and connections"""
    print_header("DATABASE SYSTEMS")
    
    databases = [
        ("careercoach.db", "Main Application Database"),
        ("careercoach_performance.db", "Performance Metrics Database")
    ]
    
    all_dbs_ok = True
    for db_file, description in databases:
        if os.path.exists(db_file):
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                table_count = len(tables)
                
                # Check for key tables
                expected_tables = ['job_postings', 'performance_metrics', 'system_alerts', 'resume_analysis']
                has_tables = all(any(table[0] == expected for table in tables) for expected in expected_tables)
                
                print_status(description, has_tables, f"{table_count} tables found")
                
                if has_tables:
                    # Count records
                    for expected_table in expected_tables:
                        if any(table[0] == expected_table for table in tables):
                            cursor.execute(f"SELECT COUNT(*) FROM {expected_table};")
                            count = cursor.fetchone()[0]
                            print(f"       {expected_table}: {count} records")
                
                conn.close()
            except Exception as e:
                print_status(description, False, f"Error: {e}")
                all_dbs_ok = False
        else:
            print_status(description, False, "File not found")
            all_dbs_ok = False
    
    return all_dbs_ok

def check_application_imports():
    """Check core application module imports"""
    print_header("APPLICATION MODULES")
    
    modules_to_test = [
        ("core.production_app", "Main FastAPI Application"),
        ("src.data_pipeline_service", "Data Pipeline Service"),
        ("src.performance_monitor", "Performance Monitor"),
        ("src.data_archival", "Data Archival Manager"),
        ("src.index_manager", "Database Index Manager"),
        ("integrations.azure.azure_devops_csv_integrator", "Azure DevOps Integration")
    ]
    
    all_imports_ok = True
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print_status(description, True, "Import successful")
        except ImportError as e:
            print_status(description, False, f"Import failed: {e}")
            all_imports_ok = False
    
    return all_imports_ok

def check_api_endpoints():
    """Test core API endpoints"""
    print_header("API ENDPOINTS")
    
    try:
        from core.production_app import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test key endpoints
        endpoints = [
            ("/", "Root Dashboard"),
            ("/dashboard", "Analytics Dashboard"),
            ("/performance", "Performance Dashboard"),
            ("/api/stats", "Statistics API"),
            ("/docs", "API Documentation")
        ]
        
        all_endpoints_ok = True
        for endpoint, description in endpoints:
            try:
                response = client.get(endpoint)
                success = response.status_code == 200
                print_status(description, success, f"HTTP {response.status_code}")
                if not success:
                    all_endpoints_ok = False
            except Exception as e:
                print_status(description, False, f"Error: {e}")
                all_endpoints_ok = False
        
        # Count total routes
        total_routes = len([r for r in app.routes if hasattr(r, 'path')])
        print(f"\n Total API Routes: {total_routes}")
        
        return all_endpoints_ok
        
    except Exception as e:
        print_status("FastAPI Application", False, f"Failed to load: {e}")
        return False

def check_configuration():
    """Check configuration files and environment"""
    print_header("CONFIGURATION")
    
    config_files = [
        ("config/settings.py", "Main Settings"),
        ("config/environment_config.py", "Environment Config"),
        ("config/monitoring_config.py", "Monitoring Config"),
        ("AUTHENTICATION_GUIDE.md", "Authentication Guide"),
        ("requirements.txt", "Dependencies List")
    ]
    
    all_config_ok = True
    for config_file, description in config_files:
        exists = os.path.exists(config_file)
        print_status(description, exists, "Found" if exists else "Missing")
        if not exists:
            all_config_ok = False
    
    # Check environment variables
    env_vars = [
        ("OPENAI_API_KEY", "OpenAI Integration"),
        ("NOTION_TOKEN", "Notion Integration"),
        ("AZURE_DEVOPS_PAT", "Azure DevOps Integration")
    ]
    
    for env_var, description in env_vars:
        has_var = bool(os.getenv(env_var))
        print_status(f"ENV: {description}", has_var, "Set" if has_var else "Not set")
    
    return all_config_ok

def check_project_structure():
    """Verify project structure organization"""
    print_header("PROJECT STRUCTURE")
    
    expected_dirs = [
        "core", "src", "integrations", "tests", "docs", 
        "data", "config", "infrastructure", "static", "templates"
    ]
    
    all_dirs_ok = True
    for directory in expected_dirs:
        exists = os.path.isdir(directory)
        print_status(f"Directory: {directory}/", exists, "Present" if exists else "Missing")
        if not exists:
            all_dirs_ok = False
    
    return all_dirs_ok

def main():
    """Run comprehensive health check"""
    print(" CareerCoach.ai Platform Health Check")
    print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all checks
    checks = [
        ("System Resources", check_system_resources),
        ("Python Environment", check_python_environment),
        ("Database Systems", check_databases),
        ("Application Modules", check_application_imports),
        ("API Endpoints", check_api_endpoints),
        ("Configuration", check_configuration),
        ("Project Structure", check_project_structure)
    ]
    
    results = {}
    for check_name, check_function in checks:
        try:
            results[check_name] = check_function()
        except Exception as e:
            print_status(check_name, False, f"Check failed: {e}")
            results[check_name] = False
    
    # Summary
    print_header("HEALTH CHECK SUMMARY")
    
    all_passed = all(results.values())
    passed_count = sum(results.values())
    total_count = len(results)
    
    for check_name, status in results.items():
        print_status(check_name, status, "PASS" if status else "FAIL")
    
    print(f"\n Overall Status: {passed_count}/{total_count} checks passed")
    
    if all_passed:
        print("\n All systems are healthy and operational!")
        print(" CareerCoach.ai platform is ready for use")
    else:
        print("\n  Some issues detected. Please review the failed checks above.")
        print(" Refer to AUTHENTICATION_GUIDE.md for configuration help")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)