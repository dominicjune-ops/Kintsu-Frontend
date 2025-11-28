#!/usr/bin/env python3
"""
Kintsu Final Product Implementation
Create the finalized product lineup with add-ons in Stripe
"""

import os
import stripe
import json
from datetime import datetime

def implement_final_product_strategy():
    """Implement the finalized Kintsu product strategy"""
    
    print(" Implementing Kintsu Final Product Strategy")
    print("=" * 60)
    
    # Set up Stripe
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    if not stripe.api_key:
        print(" Set STRIPE_SECRET_KEY environment variable first")
        print("Run: $env:STRIPE_SECRET_KEY = 'your_stripe_secret_key'")
        return False
    
    try:
        # Archive existing products first
        print("🗂️  Archiving old products...")
        existing_products = stripe.Product.list(active=True, limit=100)
        for product in existing_products.data:
            stripe.Product.modify(product.id, active=False)
            print(f"📦 Archived: {product.name}")
        
        created_products = {}
        
        # 1. Kintsu Basic - $9.99/month
        basic_product = stripe.Product.create(
            name="Kintsu Basic",
            description="For job seekers who want speed and structure. 26x faster job search with AI-powered matching, resume builder with ATS optimization, and personalized job alerts.",
            metadata={
                "tier": "basic",
                "target_audience": "early-career professionals, career switchers",
                "key_benefit": "26x faster job search",
                "platform": "kintsu.io"
            }
        )
        
        basic_price = stripe.Price.create(
            product=basic_product.id,
            unit_amount=999,  # $9.99
            currency='usd',
            recurring={'interval': 'month'}
        )
        
        created_products['basic'] = {
            'product_id': basic_product.id,
            'price_id': basic_price.id,
            'name': 'Kintsu Basic',
            'price': 9.99
        }
        print(" Created: Kintsu Basic - $9.99/month")
        
        # 2. Kintsu Professional - $29.99/month
        professional_product = stripe.Product.create(
            name="Kintsu Professional", 
            description="For professionals ready to level up. 31x faster AI coaching with real-time feedback, interview prep with dynamic Q&A simulations, and salary benchmarking insights.",
            metadata={
                "tier": "professional",
                "target_audience": "mid-career professionals, high-performers", 
                "key_benefit": "31x faster AI coaching",
                "platform": "kintsu.io"
            }
        )
        
        professional_price = stripe.Price.create(
            product=professional_product.id,
            unit_amount=2999,  # $29.99
            currency='usd',
            recurring={'interval': 'month'}
        )
        
        created_products['professional'] = {
            'product_id': professional_product.id,
            'price_id': professional_price.id,
            'name': 'Kintsu Professional',
            'price': 29.99
        }
        print(" Created: Kintsu Professional - $29.99/month")
        
        # 3. Kintsu Executive - $99.99/month
        executive_product = stripe.Product.create(
            name="Kintsu Executive",
            description="For leaders aiming for C-suite roles. 1-on-1 executive coaching and strategy sessions, C-suite interview prep, private KPI dashboard, and white-glove support.",
            metadata={
                "tier": "executive", 
                "target_audience": "senior leaders, founders, C-suite candidates",
                "key_benefit": "1-on-1 executive coaching",
                "platform": "kintsu.io"
            }
        )
        
        executive_price = stripe.Price.create(
            product=executive_product.id,
            unit_amount=9999,  # $99.99
            currency='usd',
            recurring={'interval': 'month'}
        )
        
        created_products['executive'] = {
            'product_id': executive_product.id,
            'price_id': executive_price.id,
            'name': 'Kintsu Executive',
            'price': 99.99
        }
        print(" Created: Kintsu Executive - $99.99/month")
        
        # 4. Add-On: Resume Tailor Pro - $4.99 one-time
        resume_addon = stripe.Product.create(
            name="Resume Tailor Pro",
            description="One-time resume enhancement with AI-driven tailoring for specific job applications. Perfect for Basic plan users.",
            metadata={
                "type": "addon",
                "category": "resume_enhancement",
                "target_tier": "basic",
                "platform": "kintsu.io"
            }
        )
        
        resume_price = stripe.Price.create(
            product=resume_addon.id,
            unit_amount=499,  # $4.99
            currency='usd'
            # No recurring for one-time purchase
        )
        
        created_products['resume_addon'] = {
            'product_id': resume_addon.id,
            'price_id': resume_price.id,
            'name': 'Resume Tailor Pro',
            'price': 4.99,
            'type': 'one_time'
        }
        print(" Created: Resume Tailor Pro - $4.99 one-time")
        
        # 5. Add-On: LinkedIn Optimization - $9.99 one-time
        linkedin_addon = stripe.Product.create(
            name="LinkedIn Optimization",
            description="Profile rewrite with keyword tuning for maximum recruiter visibility. Ideal cross-sell for Professional users.",
            metadata={
                "type": "addon",
                "category": "profile_optimization", 
                "target_tier": "professional",
                "platform": "kintsu.io"
            }
        )
        
        linkedin_price = stripe.Price.create(
            product=linkedin_addon.id,
            unit_amount=999,  # $9.99
            currency='usd'
        )
        
        created_products['linkedin_addon'] = {
            'product_id': linkedin_addon.id,
            'price_id': linkedin_price.id,
            'name': 'LinkedIn Optimization',
            'price': 9.99,
            'type': 'one_time'
        }
        print(" Created: LinkedIn Optimization - $9.99 one-time")
        
        # 6. Add-On: Job Connector API Access - $19.99/month
        api_addon = stripe.Product.create(
            name="Job Connector API Access",
            description="Developer access to job-matching endpoints and webhook triggers. Enterprise-grade integration capabilities.",
            metadata={
                "type": "addon",
                "category": "api_access",
                "target_tier": "executive", 
                "platform": "kintsu.io"
            }
        )
        
        api_price = stripe.Price.create(
            product=api_addon.id,
            unit_amount=1999,  # $19.99
            currency='usd',
            recurring={'interval': 'month'}
        )
        
        created_products['api_addon'] = {
            'product_id': api_addon.id,
            'price_id': api_price.id,
            'name': 'Job Connector API Access',
            'price': 19.99,
            'type': 'recurring'
        }
        print(" Created: Job Connector API Access - $19.99/month")
        
        # Save the complete product configuration
        final_config = {
            'strategy_version': '2.0_final',
            'created_at': datetime.utcnow().isoformat(),
            'platform': 'kintsu.io',
            'products': created_products,
            'revenue_projections': {
                'conservative_monthly': {
                    'basic': {'users': 100, 'revenue': 999.00},
                    'professional': {'users': 50, 'revenue': 1499.50},
                    'executive': {'users': 20, 'revenue': 1999.80},
                    'addons': {'sales': 30, 'revenue': 250.00},
                    'total': 4748.30
                },
                'optimistic_monthly': {
                    'basic': {'users': 300, 'revenue': 2997.00},
                    'professional': {'users': 150, 'revenue': 4498.50},
                    'executive': {'users': 50, 'revenue': 4999.50},
                    'addons': {'sales': 100, 'revenue': 832.00},
                    'total': 13327.00
                }
            },
            'upgrade_paths': {
                'basic_to_professional': 'Target 25% conversion with AI coaching benefits',
                'professional_to_executive': 'Target 10% conversion with 1-on-1 coaching',
                'addon_attach_rate': 'Target 30% across all tiers'
            },
            'competitive_advantages': {
                'performance': '26x-31x faster than competitors',
                'pricing': 'Premium value at accessible price points',
                'features': 'Comprehensive career coaching vs job search only',
                'technology': 'AI-powered vs traditional methods'
            }
        }
        
        with open('careercoach_final_products.json', 'w') as f:
            json.dump(final_config, f, indent=2)
        
        print(f"\n Complete product configuration saved!")
        
        # Display revenue summary
        print(f"\n Revenue Potential:")
        print(f"   Conservative: ${final_config['revenue_projections']['conservative_monthly']['total']:,.2f}/month")
        print(f"   Optimistic:   ${final_config['revenue_projections']['optimistic_monthly']['total']:,.2f}/month")
        
        return created_products
        
    except Exception as e:
        print(f" Error implementing products: {str(e)}")
        return None

def display_implementation_summary(products):
    """Display the final implementation summary"""
    
    print(f"\n🎊 Kintsu Product Strategy Implemented!")
    print(f"=" * 60)
    
    print(f"\n📦 Products Created:")
    tier_products = [p for p in products.values() if p.get('type') != 'one_time' and p.get('type') != 'recurring']
    addon_products = [p for p in products.values() if p.get('type') in ['one_time', 'recurring']]
    
    print(f"\n🏆 Subscription Tiers:")
    for product in tier_products:
        print(f"   • {product['name']}: ${product['price']}/month")
    
    print(f"\n Add-On Products:")
    for product in addon_products:
        billing = "/month" if product.get('type') == 'recurring' else " one-time"
        print(f"   • {product['name']}: ${product['price']}{billing}")
    
    print(f"\n Strategic Benefits:")
    print(f"    Clear value ladder with 3x price progression")
    print(f"    Performance differentiation (26x-31x faster)")
    print(f"    Cross-sell opportunities with targeted add-ons")
    print(f"    Competitive positioning vs LinkedIn/ZipRecruiter")
    print(f"    Revenue potential: $4,748 - $13,327/month")
    
    print(f"\n Next Steps:")
    print(f"   1. Set up payment forms with new product IDs")
    print(f"   2. Configure upgrade/cross-sell automation")
    print(f"   3. Launch marketing campaigns with performance messaging")
    print(f"   4. Track conversion metrics and optimize")
    
    print(f"\n Your Kintsu monetization strategy is LIVE!")

def main():
    """Main implementation flow"""
    
    products = implement_final_product_strategy()
    
    if products:
        display_implementation_summary(products)
        print(f"\n Implementation successful!")
        return True
    else:
        print(f"\n Implementation failed - check errors above")
        return False

if __name__ == "__main__":
    success = main()