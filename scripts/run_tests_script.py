#!/usr/bin/env python3
"""
Comprehensive test runner for CareerCoach.ai
Provides various testing modes and reporting options
"""

import subprocess
import sys
import argparse
from datetime import datetime
from pathlib import Path


class TestRunner:
    """Test runner with multiple execution modes"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def run_quick_tests(self):
        """Run quick unit tests only"""
        print("🏃 Running quick unit tests...")
        cmd = [
            "pytest",
            "-m", "unit",
            "-v",
            "--tb=short",
            "--maxfail=5",
            "-x"  # Stop on first failure
        ]
        return subprocess.run(cmd)
    
    def run_critical_tests(self):
        """Run critical path tests only"""
        print(" Running critical path tests...")
        cmd = [
            "pytest",
            "-m", "critical",
            "-v",
            "--tb=short",
            "--maxfail=3"
        ]
        return subprocess.run(cmd)
    
    def run_coverage_tests(self):
        """Run tests with coverage report"""
        print(" Running tests with coverage...")
        cmd = [
            "pytest",
            "--cov=src",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=json",
            f"--cov-fail-under=30",
            "-v"
        ]
        return subprocess.run(cmd)
    
    def run_integration_tests(self):
        """Run integration tests"""
        print("🔗 Running integration tests...")
        cmd = [
            "pytest",
            "-m", "integration",
            "-v",
            "--tb=short"
        ]
        return subprocess.run(cmd)
    
    def run_e2e_tests(self):
        """Run end-to-end tests"""
        print("🎬 Running end-to-end tests...")
        cmd = [
            "pytest",
            "-m", "e2e",
            "-v",
            "--tb=long",
            "-s"  # Show print statements
        ]
        return subprocess.run(cmd)
    
    def run_smoke_tests(self):
        """Run smoke tests for quick validation"""
        print("💨 Running smoke tests...")
        cmd = [
            "pytest",
            "-m", "smoke",
            "-v",
            "--tb=short",
            "--maxfail=1"
        ]
        return subprocess.run(cmd)
    
    def run_all_tests(self):
        """Run all tests"""
        print(" Running all tests...")
        cmd = [
            "pytest",
            "-v",
            "--tb=short",
            "--maxfail=10"
        ]
        return subprocess.run(cmd)
    
    def run_parallel_tests(self):
        """Run tests in parallel"""
        print(" Running tests in parallel...")
        cmd = [
            "pytest",
            "-n", "auto",  # Auto-detect CPU count
            "-v",
            "--tb=short"
        ]
        return subprocess.run(cmd)
    
    def run_specific_module(self, module_name):
        """Run tests for specific module"""
        print(f" Running tests for {module_name}...")
        cmd = [
            "pytest",
            f"tests/unit/test_{module_name}.py",
            "-v",
            "--tb=short"
        ]
        return subprocess.run(cmd)
    
    def run_failed_tests(self):
        """Re-run only failed tests from last run"""
        print(" Re-running failed tests...")
        cmd = [
            "pytest",
            "--lf",  # Last failed
            "-v",
            "--tb=short"
        ]
        return subprocess.run(cmd)
    
    def run_with_html_report(self):
        """Run tests and generate HTML report"""
        print("📄 Running tests with HTML report...")
        cmd = [
            "pytest",
            "--html=test_report.html",
            "--self-contained-html",
            "-v"
        ]
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print(f"\n HTML report generated: test_report.html")
        return result
    
    def check_coverage_increase(self):
        """Check if coverage has increased"""
        print(" Checking coverage improvement...")
        cmd = [
            "pytest",
            "--cov=src",
            "--cov-report=term-missing",
            "-q"
        ]
        return subprocess.run(cmd)
    
    def run_performance_tests(self):
        """Run performance/slow tests"""
        print("  Running performance tests...")
        cmd = [
            "pytest",
            "-m", "slow",
            "-v",
            "--durations=10"  # Show 10 slowest tests
        ]
        return subprocess.run(cmd)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="CareerCoach.ai Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --quick           # Quick unit tests
  python run_tests.py --critical        # Critical path tests
  python run_tests.py --coverage        # Tests with coverage
  python run_tests.py --integration     # Integration tests
  python run_tests.py --e2e             # End-to-end tests
  python run_tests.py --smoke           # Smoke tests
  python run_tests.py --all             # All tests
  python run_tests.py --parallel        # Parallel execution
  python run_tests.py --module auth     # Specific module
  python run_tests.py --failed          # Re-run failed tests
  python run_tests.py --html            # Generate HTML report
        """
    )
    
    parser.add_argument("--quick", action="store_true", help="Run quick unit tests")
    parser.add_argument("--critical", action="store_true", help="Run critical tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--module", type=str, help="Run tests for specific module")
    parser.add_argument("--failed", action="store_true", help="Re-run failed tests")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    # Print banner
    print("=" * 70)
    print("   CareerCoach.ai Test Suite")
    print("=" * 70)
    print()
    
    # Execute selected test mode
    if args.quick:
        result = runner.run_quick_tests()
    elif args.critical:
        result = runner.run_critical_tests()
    elif args.coverage:
        result = runner.run_coverage_tests()
    elif args.integration:
        result = runner.run_integration_tests()
    elif args.e2e:
        result = runner.run_e2e_tests()
    elif args.smoke:
        result = runner.run_smoke_tests()
    elif args.all:
        result = runner.run_all_tests()
    elif args.parallel:
        result = runner.run_parallel_tests()
    elif args.module:
        result = runner.run_specific_module(args.module)
    elif args.failed:
        result = runner.run_failed_tests()
    elif args.html:
        result = runner.run_with_html_report()
    elif args.performance:
        result = runner.run_performance_tests()
    else:
        # Default: run coverage tests
        print("No mode specified, running coverage tests by default...")
        print("Use --help to see available options\n")
        result = runner.run_coverage_tests()
    
    # Print summary
    print()
    print("=" * 70)
    if result.returncode == 0:
        print(" Tests PASSED")
    else:
        print(" Tests FAILED")
    print("=" * 70)
    
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
