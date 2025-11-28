#!/usr/bin/env python3
"""
Environment Configuration Validator

Validates that all required environment variables are set and properly formatted.
Provides color-coded output for easy identification of issues.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_colored(message: str, color: str = Colors.RESET):
    """Print colored message to terminal."""
    print(f"{color}{message}{Colors.RESET}")


def check_env_file() -> bool:
    """Check if .env file exists."""
    env_path = project_root / ".env"
    if not env_path.exists():
        print_colored("ERROR: .env file not found!", Colors.RED)
        print_colored(f"  Expected location: {env_path}", Colors.YELLOW)
        print_colored("  Copy .env.example to .env and fill in your values", Colors.CYAN)
        return False

    print_colored("SUCCESS: .env file found", Colors.GREEN)
    return True


def load_env_file() -> Dict[str, str]:
    """Load environment variables from .env file."""
    env_vars = {}
    env_path = project_root / ".env"

    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()

        print_colored(f"SUCCESS: Loaded {len(env_vars)} environment variables", Colors.GREEN)
        return env_vars
    except Exception as e:
        print_colored(f"ERROR: Error loading .env file: {e}", Colors.RED)
        return {}


def validate_url(url: str) -> bool:
    """Validate URL format."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(url))


def validate_database_url(url: str) -> bool:
    """Validate PostgreSQL database URL format."""
    db_pattern = re.compile(
        r'^postgresql:\/\/.+:.+@.+:\d+\/.+$'
    )
    return bool(db_pattern.match(url))


def validate_api_key(key: str, prefix: str) -> bool:
    """Validate API key format."""
    if not key:
        return False
    if not key.startswith(prefix):
        return False
    if len(key) < 20:  # API keys should be reasonably long
        return False
    return True


# Required environment variables
REQUIRED_VARS = {
    "SUPABASE_URL": {
        "description": "Supabase project URL",
        "validator": lambda v: validate_url(v) and "supabase.co" in v,
        "example": "https://your-project.supabase.co"
    },
    "SUPABASE_ANON_KEY": {
        "description": "Supabase anonymous key",
        "validator": lambda v: len(v) > 50,
        "example": "eyJhbGciOiJIUzI1NiIs..."
    },
    "SUPABASE_SERVICE_ROLE_KEY": {
        "description": "Supabase service role key",
        "validator": lambda v: len(v) > 50,
        "example": "eyJhbGciOiJIUzI1NiIs..."
    },
    "SUPABASE_DB_URL": {
        "description": "Supabase database connection URL",
        "validator": validate_database_url,
        "example": "postgresql://postgres:pass@db.project.supabase.co:5432/postgres"
    },
    "JWT_SECRET_KEY": {
        "description": "JWT secret key for authentication",
        "validator": lambda v: len(v) >= 32,
        "example": "Generate with: python -c \"import secrets; print(secrets.token_hex(32))\""
    }
}

# Optional environment variables
OPTIONAL_VARS = {
    "OPENAI_API_KEY": {
        "description": "OpenAI API key",
        "validator": lambda v: validate_api_key(v, "sk-"),
        "required_for": "AI features"
    },
    "STRIPE_SECRET_KEY": {
        "description": "Stripe secret key",
        "validator": lambda v: validate_api_key(v, "sk_"),
        "required_for": "Payment processing"
    },
    "STRIPE_PUBLISHABLE_KEY": {
        "description": "Stripe publishable key",
        "validator": lambda v: validate_api_key(v, "pk_"),
        "required_for": "Payment processing"
    },
    "REDIS_URL": {
        "description": "Redis connection URL",
        "validator": lambda v: validate_url(v) or v.startswith("redis://"),
        "required_for": "Caching"
    },
    "SENTRY_DSN": {
        "description": "Sentry error tracking DSN",
        "validator": validate_url,
        "required_for": "Error tracking"
    },
    "POSTHOG_API_KEY": {
        "description": "PostHog analytics key",
        "validator": lambda v: validate_api_key(v, "phc_"),
        "required_for": "Analytics"
    }
}


def validate_required_vars(env_vars: Dict[str, str]) -> Tuple[List[str], List[str]]:
    """
    Validate required environment variables.

    Returns:
        Tuple of (valid_vars, invalid_vars)
    """
    valid = []
    invalid = []

    print_colored("\n" + "="*60, Colors.BLUE)
    print_colored("REQUIRED VARIABLES", Colors.BOLD + Colors.BLUE)
    print_colored("="*60, Colors.BLUE)

    for var_name, var_info in REQUIRED_VARS.items():
        value = env_vars.get(var_name) or os.getenv(var_name)

        if not value:
            print_colored(f"[X] {var_name}: MISSING", Colors.RED)
            print_colored(f"  {var_info['description']}", Colors.YELLOW)
            print_colored(f"  Example: {var_info.get('example', 'N/A')}", Colors.CYAN)
            invalid.append(var_name)
        elif not var_info['validator'](value):
            print_colored(f"[X] {var_name}: INVALID FORMAT", Colors.RED)
            print_colored(f"  {var_info['description']}", Colors.YELLOW)
            print_colored(f"  Example: {var_info.get('example', 'N/A')}", Colors.CYAN)
            invalid.append(var_name)
        else:
            print_colored(f"[OK] {var_name}: OK", Colors.GREEN)
            valid.append(var_name)

    return valid, invalid


def validate_optional_vars(env_vars: Dict[str, str]) -> Tuple[List[str], List[str]]:
    """
    Validate optional environment variables.

    Returns:
        Tuple of (valid_vars, missing_vars)
    """
    valid = []
    missing = []

    print_colored("\n" + "="*60, Colors.BLUE)
    print_colored("OPTIONAL VARIABLES", Colors.BOLD + Colors.BLUE)
    print_colored("="*60, Colors.BLUE)

    for var_name, var_info in OPTIONAL_VARS.items():
        value = env_vars.get(var_name) or os.getenv(var_name)

        if not value:
            print_colored(f"[ ] {var_name}: Not set", Colors.YELLOW)
            print_colored(f"  Required for: {var_info['required_for']}", Colors.CYAN)
            missing.append(var_name)
        elif not var_info['validator'](value):
            print_colored(f"[X] {var_name}: INVALID FORMAT", Colors.RED)
            print_colored(f"  {var_info['description']}", Colors.YELLOW)
        else:
            print_colored(f"[OK] {var_name}: OK", Colors.GREEN)
            valid.append(var_name)

    return valid, missing


def test_database_connection() -> bool:
    """Test database connectivity."""
    print_colored("\n" + "="*60, Colors.BLUE)
    print_colored("DATABASE CONNECTION TEST", Colors.BOLD + Colors.BLUE)
    print_colored("="*60, Colors.BLUE)

    try:
        from backend.core.database import check_db_connection, get_db_info

        if check_db_connection():
            db_info = get_db_info()
            print_colored(f"[OK] Database connection: SUCCESS", Colors.GREEN)
            print_colored(f"  Type: {db_info['type']}", Colors.CYAN)
            print_colored(f"  URL: {db_info['url']}", Colors.CYAN)
            return True
        else:
            print_colored("[X] Database connection: FAILED", Colors.RED)
            print_colored("  Check your SUPABASE_DB_URL configuration", Colors.YELLOW)
            return False
    except Exception as e:
        print_colored(f"[X] Database connection test failed: {e}", Colors.RED)
        return False


def print_summary(required_valid: List[str], required_invalid: List[str],
                 optional_valid: List[str], optional_missing: List[str],
                 db_connected: bool):
    """Print validation summary."""
    print_colored("\n" + "="*60, Colors.BLUE)
    print_colored("VALIDATION SUMMARY", Colors.BOLD + Colors.BLUE)
    print_colored("="*60, Colors.BLUE)

    print_colored(f"\nRequired Variables:", Colors.BOLD)
    print_colored(f"  [OK] Valid: {len(required_valid)}/{len(REQUIRED_VARS)}", Colors.GREEN)
    if required_invalid:
        print_colored(f"  [X] Invalid/Missing: {len(required_invalid)}", Colors.RED)

    print_colored(f"\nOptional Variables:", Colors.BOLD)
    print_colored(f"  [OK] Configured: {len(optional_valid)}/{len(OPTIONAL_VARS)}", Colors.GREEN)
    print_colored(f"  [ ] Not set: {len(optional_missing)}", Colors.YELLOW)

    print_colored(f"\nDatabase Connection:", Colors.BOLD)
    if db_connected:
        print_colored(f"  [OK] Connected", Colors.GREEN)
    else:
        print_colored(f"  [X] Not connected", Colors.RED)

    # Overall status
    print_colored("\n" + "="*60, Colors.BLUE)
    if not required_invalid and db_connected:
        print_colored("STATUS: READY FOR PRODUCTION", Colors.BOLD + Colors.GREEN)
        print_colored("="*60, Colors.BLUE)
        return True
    elif not required_invalid:
        print_colored("STATUS: CONFIGURATION OK (Database not connected)", Colors.YELLOW)
        print_colored("="*60, Colors.BLUE)
        return True
    else:
        print_colored("STATUS: CONFIGURATION INCOMPLETE", Colors.BOLD + Colors.RED)
        print_colored("="*60, Colors.BLUE)
        print_colored("\nPlease fix the issues above before running the application.", Colors.YELLOW)
        return False


def main():
    """Main validation function."""
    print_colored("\n" + "="*60, Colors.BOLD + Colors.BLUE)
    print_colored("CareerCoach.ai Environment Validator", Colors.BOLD + Colors.BLUE)
    print_colored("="*60, Colors.BOLD + Colors.BLUE)

    # Check if .env exists
    if not check_env_file():
        sys.exit(1)

    # Load environment variables
    env_vars = load_env_file()
    if not env_vars:
        sys.exit(1)

    # Validate required variables
    required_valid, required_invalid = validate_required_vars(env_vars)

    # Validate optional variables
    optional_valid, optional_missing = validate_optional_vars(env_vars)

    # Test database connection
    db_connected = test_database_connection()

    # Print summary
    success = print_summary(
        required_valid, required_invalid,
        optional_valid, optional_missing,
        db_connected
    )

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
