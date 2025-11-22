import { PricingTable } from "@/components/PricingTable";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";

export default function Pricing() {
  return (
    <div>
      <section className="py-20 md:py-32 bg-background">
        <div className="container mx-auto px-4 md:px-6">
          <div className="text-center mb-16 max-w-3xl mx-auto">
            <h1 className="text-4xl md:text-5xl font-bold font-serif mb-6">
              Transparent Pricing for Every Career Stage
            </h1>
            <p className="text-lg text-muted-foreground">
              Start free and upgrade as you grow. All plans include our core AI-powered features with no hidden fees.
            </p>
          </div>
        </div>
      </section>

      <PricingTable />

      <section className="py-20 bg-background">
        <div className="container mx-auto px-4 md:px-6">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold font-serif mb-8 text-center">
              Frequently Asked Questions
            </h2>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-2">How does the 14-day trial work?</h3>
                <p className="text-muted-foreground">
                  Start with full access to Professional or Executive features. Your card won't be charged until the trial ends. Cancel anytime during the trial period.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">Can I change plans later?</h3>
                <p className="text-muted-foreground">
                  Absolutely. Upgrade or downgrade your plan at any time. Changes take effect on your next billing cycle.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">What's included in AI-powered tailoring?</h3>
                <p className="text-muted-foreground">
                  Our AI analyzes job descriptions and tailors your resume to match specific roles, optimizes for ATS systems, and suggests improvements based on industry best practices.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">Is my data secure?</h3>
                <p className="text-muted-foreground">
                  Yes. We use bank-level encryption and never share your data without permission. See our privacy policy for details.
                </p>
              </div>
            </div>

            <div className="mt-12 text-center">
              <Button size="lg" asChild data-testid="button-pricing-cta">
                <a href="https://app.kintsu.io">Start Your 14-Day Trial</a>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
