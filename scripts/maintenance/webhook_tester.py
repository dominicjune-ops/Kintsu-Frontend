#!/usr/bin/env python3
"""
Stripe Webhook Testing Utilities
Simulate webhook events for testing webhook endpoints
"""

import requests
import json
import os
from datetime import datetime
import hmac
import hashlib
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WebhookTester:
    """Test utility for Stripe webhook endpoints"""

    def __init__(self, webhook_url="http://localhost:4242/webhook", webhook_secret=None):
        self.webhook_url = webhook_url
        self.webhook_secret = webhook_secret or os.getenv('STRIPE_WEBHOOK_SECRET')

    def create_signature(self, payload):
        """Create Stripe-style webhook signature"""
        if not self.webhook_secret:
            return None

        timestamp = str(int(datetime.now().timestamp()))
        signed_payload = f"{timestamp}.{payload}"

        signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            signed_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return f"t={timestamp},v1={signature}"

    def send_test_event(self, event_type, event_data):
        """Send a test webhook event"""
        # Create event payload
        event = {
            "id": f"evt_test_{event_type.replace('.', '_')}",
            "object": "event",
            "api_version": "2020-08-27",
            "created": int(datetime.now().timestamp()),
            "data": {
                "object": event_data
            },
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": f"req_test_{int(datetime.now().timestamp())}",
                "idempotency_key": None
            },
            "type": event_type
        }

        payload = json.dumps(event, separators=(',', ':'))

        headers = {
            'Content-Type': 'application/json',
        }

        # Add signature if webhook secret is available
        if self.webhook_secret:
            signature = self.create_signature(payload)
            if signature:
                headers['Stripe-Signature'] = signature

        try:
            response = requests.post(
                self.webhook_url,
                data=payload,
                headers=headers,
                timeout=10
            )

            print(f"Event: {event_type}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            print("-" * 50)

            return response

        except requests.exceptions.RequestException as e:
            print(f"Error sending webhook: {e}")
            return None

def test_subscription_events():
    """Test subscription-related webhook events"""

    tester = WebhookTester()

    # Test subscription created
    subscription_created_data = {
        "id": "sub_test_123",
        "object": "subscription",
        "customer": "cus_test_123",
        "status": "active",
        "current_period_end": int(datetime.now().timestamp()) + 30*24*60*60,  # 30 days
        "current_period_start": int(datetime.now().timestamp()),
        "items": {
            "data": [{
                "price": {
                    "id": "price_premium_monthly",
                    "unit_amount": 999
                }
            }]
        }
    }

    tester.send_test_event("customer.subscription.created", subscription_created_data)

    # Test payment succeeded
    payment_succeeded_data = {
        "id": "in_test_123",
        "object": "invoice",
        "customer": "cus_test_123",
        "amount_paid": 999,
        "currency": "usd",
        "status": "paid",
        "subscription": "sub_test_123"
    }

    tester.send_test_event("invoice.payment_succeeded", payment_succeeded_data)

    # Test subscription cancelled
    subscription_cancelled_data = {
        "id": "sub_test_123",
        "object": "subscription",
        "customer": "cus_test_123",
        "status": "canceled",
        "canceled_at": int(datetime.now().timestamp())
    }

    tester.send_test_event("customer.subscription.deleted", subscription_cancelled_data)

def test_checkout_events():
    """Test checkout-related webhook events"""

    tester = WebhookTester()

    # Test checkout completed
    checkout_completed_data = {
        "id": "cs_test_123",
        "object": "checkout.session",
        "customer": "cus_test_123",
        "payment_status": "paid",
        "amount_total": 999,
        "currency": "usd",
        "mode": "subscription"
    }

    tester.send_test_event("checkout.session.completed", checkout_completed_data)

def test_payment_failure():
    """Test payment failure event"""

    tester = WebhookTester()

    payment_failed_data = {
        "id": "in_test_456",
        "object": "invoice",
        "customer": "cus_test_123",
        "amount_due": 999,
        "currency": "usd",
        "status": "open",
        "attempt_count": 3,
        "subscription": "sub_test_123"
    }

    tester.send_test_event("invoice.payment_failed", payment_failed_data)

def run_all_tests():
    """Run all webhook tests"""
    print(" Starting Stripe Webhook Tests")
    print("=" * 50)

    test_subscription_events()
    test_checkout_events()
    test_payment_failure()

    print(" All webhook tests completed")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "subscription":
            test_subscription_events()
        elif sys.argv[1] == "checkout":
            test_checkout_events()
        elif sys.argv[1] == "failure":
            test_payment_failure()
        else:
            print("Usage: python webhook_tester.py [subscription|checkout|failure|all]")
    else:
        run_all_tests()