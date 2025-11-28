#!/usr/bin/env python3
"""
Stripe Webhook Development Server
Quick start script for webhook development and testing
"""

import os
import subprocess
import sys
import time
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import stripe
        print(" Requirements satisfied")
        return True
    except ImportError as e:
        print(f" Missing requirement: {e}")
        print("Run: pip install -r archive/deprecated/requirements-webhook.txt")
        return False

def check_environment():
    """Check environment variables"""
    required_vars = ['STRIPE_SECRET_KEY', 'STRIPE_WEBHOOK_SECRET']
    missing = []

    for var in required_vars:
        value = os.getenv(var)
        is_placeholder = (
            not value or
            'your' in value or  # Generic check for placeholder text
            len(value) < 20     # Real keys are longer
        )
        if is_placeholder:
            missing.append(var)

    if missing:
        print("  Missing or placeholder environment variables:")
        for var in missing:
            print(f"   - {var}")
        print("\nUpdate your .env file with real Stripe credentials")
        return False

    print(" Environment variables configured")
    return True

def start_webhook_server():
    """Start the webhook server"""
    print(" Starting webhook server...")
    print("Webhook endpoint: http://localhost:4242/webhook")
    print("Health check: http://localhost:4242/health")
    print("Press Ctrl+C to stop\n")

    try:
        # Run the webhook server
        subprocess.run([
            sys.executable, "stripe_webhook_builder.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f" Server error: {e}")

def run_tests():
    """Run webhook tests"""
    print(" Running webhook tests...")

    try:
        subprocess.run([
            sys.executable, "webhook_tester.py"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f" Test error: {e}")

def show_menu():
    """Show interactive menu"""
    print("\n" + "="*50)
    print(" Stripe Webhook Development Server")
    print("="*50)
    print("1. Start webhook server")
    print("2. Run webhook tests")
    print("3. Check configuration")
    print("4. View setup guide")
    print("5. Exit")
    print("="*50)

    while True:
        try:
            choice = input("Choose an option (1-5): ").strip()

            if choice == "1":
                if check_requirements() and check_environment():
                    start_webhook_server()
                else:
                    print(" Fix configuration issues first")
            elif choice == "2":
                if check_requirements():
                    run_tests()
                else:
                    print(" Install requirements first")
            elif choice == "3":
                check_requirements()
                check_environment()
                input("\nPress Enter to continue...")
            elif choice == "4":
                print("\n📖 Opening setup guide...")
                guide_path = Path(__file__).parent / "STRIPE_WEBHOOK_SETUP_GUIDE.md"
                if guide_path.exists():
                    if sys.platform == "win32":
                        os.startfile(guide_path)
                    else:
                        subprocess.run(["open", str(guide_path)])
                else:
                    print("Guide not found. Check STRIPE_WEBHOOK_SETUP_GUIDE.md")
                input("\nPress Enter to continue...")
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print(" Invalid choice. Please select 1-5.")

            show_menu()

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f" Error: {e}")

def main():
    """Main function"""
    print(" Stripe Webhook Endpoint Builder")
    print("Following Stripe documentation for secure webhook implementation")

    if len(sys.argv) > 1:
        # Command line mode
        command = sys.argv[1]

        if command == "server":
            if check_requirements() and check_environment():
                start_webhook_server()
            else:
                sys.exit(1)
        elif command == "test":
            if check_requirements():
                run_tests()
            else:
                sys.exit(1)
        elif command == "check":
            req_ok = check_requirements()
            env_ok = check_environment()
            sys.exit(0 if req_ok and env_ok else 1)
        else:
            print("Usage: python run_webhook.py [server|test|check]")
            print("Or run without arguments for interactive menu")
            sys.exit(1)
    else:
        # Interactive mode
        show_menu()

if __name__ == "__main__":
    main()