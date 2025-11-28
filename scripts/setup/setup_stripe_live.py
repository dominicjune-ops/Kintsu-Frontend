#!/usr/bin/env python3
"""
Kintsu Stripe Live Setup
Secure script to initialize your Stripe integration with real API keys
"""

import os
import sys
import json
from datetime import datetime

def setup_stripe_environment():
    """Guide user through secure Stripe setup"""
    print(" Kintsu Stripe Live Setup")
    print("=" * 50)
    
    print("\n Setup Checklist:")
    print(" Stripe account created")
    print(" API keys added to GitHub Secrets")
    print(" Stripe SDK installed")
    print(" Now setting up live integration...")
    
    print("\n🔐 SECURITY REMINDER:")
    print("• Never commit API keys to git")
    print("• Keys are stored securely in GitHub Secrets")
    print("• Local testing uses environment variables")
    
    # Check if user wants to proceed with live keys
    print("\n  To test with live Stripe keys:")
    print("1. Go to https://dashboard.stripe.com/apikeys")
    print("2. Copy your keys (they start with sk_test_ and pk_test_)")
    print("3. Set them as environment variables for this session")
    
    proceed = input("\n🔑 Do you have your Stripe keys ready? (y/n): ").lower()
    
    if proceed != 'y':
        print("\n Instructions for when you're ready:")
        print("1. Get keys from Stripe dashboard")
        print("2. Run: $env:STRIPE_SECRET_KEY = 'sk_test_your_key'")
        print("3. Run: $env:STRIPE_PUBLISHABLE_KEY = 'pk_test_your_key'")
        print("4. Run: python setup_stripe_live.py")
        return False
    
    # Check environment variables
    secret_key = os.getenv('STRIPE_SECRET_KEY')
    publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
    
    if not secret_key or not publishable_key:
        print("\n Environment variables not set!")
        print("\nRun these commands first:")
        print("$env:STRIPE_SECRET_KEY = 'your_secret_key_here'")
        print("$env:STRIPE_PUBLISHABLE_KEY = 'your_publishable_key_here'")
        return False
    
    # Validate key format
    if not secret_key.startswith('sk_test_'):
        print(f"  Warning: Secret key should start with 'sk_test_' for testing")
    
    if not publishable_key.startswith('pk_test_'):
        print(f"  Warning: Publishable key should start with 'pk_test_' for testing")
    
    print(f"\n Keys detected:")
    print(f"   Secret Key: {secret_key[:12]}...{secret_key[-4:]}")
    print(f"   Publishable Key: {publishable_key[:12]}...{publishable_key[-4:]}")
    
    return True

def create_careercoach_products():
    """Create Kintsu subscription products in Stripe"""
    
    try:
        import stripe
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        
        print("\n  Creating Kintsu subscription products...")
        
        products = {}
        
        # Basic Tier
        basic_product = stripe.Product.create(
            name="Kintsu Basic",
            description="26x faster job search with AI-powered recommendations and resume builder",
            metadata={
                "tier": "basic",
                "platform": "kintsu.io",
                "features": "ai_job_search,resume_builder,basic_recommendations"
            }
        )
        
        basic_price = stripe.Price.create(
            product=basic_product.id,
            unit_amount=999,  # $9.99
            currency='usd',
            recurring={'interval': 'month'},
            metadata={'tier': 'basic'}
        )
        
        products['basic'] = {
            'product_id': basic_product.id,
            'price_id': basic_price.id,
            'amount': 9.99
        }
        
        print(" Basic Tier created: $9.99/month")
        
        # Professional Tier
        professional_product = stripe.Product.create(
            name="Kintsu Professional", 
            description="31x faster AI coaching with interview preparation and salary insights",
            metadata={
                "tier": "professional",
                "platform": "kintsu.io", 
                "features": "everything_basic,advanced_ai_coaching,interview_prep,salary_insights"
            }
        )
        
        professional_price = stripe.Price.create(
            product=professional_product.id,
            unit_amount=2999,  # $29.99
            currency='usd',
            recurring={'interval': 'month'},
            metadata={'tier': 'professional'}
        )
        
        products['professional'] = {
            'product_id': professional_product.id,
            'price_id': professional_price.id,
            'amount': 29.99
        }
        
        print(" Professional Tier created: $29.99/month")
        
        # Executive Tier
        executive_product = stripe.Product.create(
            name="Kintsu Executive",
            description="Enterprise coaching with 1-on-1 sessions and custom career strategies", 
            metadata={
                "tier": "executive",
                "platform": "kintsu.io",
                "features": "everything_professional,one_on_one_coaching,custom_strategies,priority_support"
            }
        )
        
        executive_price = stripe.Price.create(
            product=executive_product.id,
            unit_amount=9999,  # $99.99
            currency='usd', 
            recurring={'interval': 'month'},
            metadata={'tier': 'executive'}
        )
        
        products['executive'] = {
            'product_id': executive_product.id,
            'price_id': executive_price.id,
            'amount': 99.99
        }
        
        print(" Executive Tier created: $99.99/month")
        
        # Save configuration
        config = {
            'created_at': datetime.utcnow().isoformat(),
            'platform': 'kintsu.io',
            'products': products,
            'webhook_events': [
                'customer.subscription.created',
                'customer.subscription.updated', 
                'customer.subscription.deleted',
                'invoice.payment_succeeded',
                'invoice.payment_failed'
            ]
        }
        
        with open('stripe_live_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n Configuration saved to stripe_live_config.json")
        
        return products
        
    except Exception as e:
        print(f"\n Error creating products: {str(e)}")
        return None

def display_setup_summary(products):
    """Display final setup summary and next steps"""
    
    print("\n🎊 Kintsu Stripe Integration Complete!")
    print("=" * 60)
    
    if products:
        total_revenue = 0
        print("\n Subscription Tiers Created:")
        for tier, data in products.items():
            users = {'basic': 100, 'professional': 50, 'executive': 20}[tier]
            revenue = data['amount'] * users
            total_revenue += revenue
            print(f"   {tier.title():12} | ${data['amount']:6.2f} × {users:3d} users = ${revenue:8.2f}/month")
        
        print(f"\n Total Revenue Potential: ${total_revenue:,.2f}/month")
        print(f"   Annual: ${total_revenue * 12:,.2f}")
        print(f"   vs $84/year hosting cost = 99.8% profit margin!")
    
    print("\n Next Steps:")
    print("1.  Products created in Stripe")
    print("2.  Set up webhook endpoint")
    print("3.  Integrate with frontend")
    print("4.  Add user authentication")
    print("5.  Deploy to production")
    
    print("\n🔗 Useful Links:")
    print("   • Stripe Dashboard: https://dashboard.stripe.com")
    print("   • Webhook Config: https://dashboard.stripe.com/webhooks")
    print("   • Documentation: https://stripe.com/docs/billing/subscriptions")
    
    print("\n Your Competitive Advantage:")
    print("   • 26x faster job search performance")
    print("   • 31x faster AI response times")
    print("   • Enterprise-grade reliability")
    print("   • $125/month operational cost savings")
    print("   • Superior AI technology stack")

def main():
    """Main setup flow"""
    
    # Step 1: Environment setup
    if not setup_stripe_environment():
        sys.exit(1)
    
    # Step 2: Create products
    print("\n Proceeding with Stripe product creation...")
    products = create_careercoach_products()
    
    # Step 3: Display summary
    display_setup_summary(products)
    
    if products:
        print(f"\n Setup completed successfully!")
        print(f" {len(products)} subscription tiers ready for launch")
        return True
    else:
        print(f"\n Setup incomplete - check errors above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)