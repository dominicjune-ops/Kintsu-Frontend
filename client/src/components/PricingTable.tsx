import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";

const pricingTiers = [
  {
    name: "Starter",
    tagline: "Begin your golden repair",
    monthlyPrice: 0,
    annualPrice: 0,
    features: [
      "Basic resume tailoring",
      "3 job applications per month",
      "Email support",
      "Basic ATS optimization"
    ]
  },
  {
    name: "Professional",
    tagline: "Perfect for active job seekers",
    monthlyPrice: 29,
    annualPrice: 290,
    popular: true,
    features: [
      "Unlimited resume tailoring",
      "Unlimited job applications",
      "AI-powered interview coaching",
      "Advanced ATS optimization",
      "Salary negotiation guidance",
      "Priority support",
      "Progress tracking dashboard"
    ]
  },
  {
    name: "Executive",
    tagline: "Premium career transformation",
    monthlyPrice: 99,
    annualPrice: 990,
    features: [
      "Everything in Professional",
      "1-on-1 human coaching sessions",
      "Executive resume review",
      "LinkedIn profile optimization",
      "Personal brand consulting",
      "Dedicated account manager",
      "Custom career strategy"
    ]
  }
];

export function PricingTable() {
  const [isAnnual, setIsAnnual] = useState(false);

  return (
    <section className="py-20 md:py-32 bg-card">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold font-serif mb-4">
            Choose your plan
          </h2>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
            Start free or unlock premium features with our Pro plans
          </p>

          <div className="flex items-center justify-center gap-3">
            <Label htmlFor="billing-toggle" className={!isAnnual ? "font-semibold" : ""}>
              Monthly
            </Label>
            <Switch
              id="billing-toggle"
              checked={isAnnual}
              onCheckedChange={setIsAnnual}
              data-testid="switch-billing-toggle"
            />
            <Label htmlFor="billing-toggle" className={isAnnual ? "font-semibold" : ""}>
              Annual <span className="text-accent text-sm">(Save 17%)</span>
            </Label>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {pricingTiers.map((tier, index) => (
            <Card
              key={index}
              className={`p-8 relative hover-elevate transition-all duration-200 ${
                tier.popular ? "border-accent border-2" : ""
              }`}
              data-testid={`pricing-card-${tier.name.toLowerCase()}`}
            >
              {tier.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                  <span className="bg-accent text-accent-foreground text-xs font-semibold px-3 py-1 rounded-full">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-2xl font-bold font-serif mb-2">{tier.name}</h3>
                <p className="text-sm text-muted-foreground">{tier.tagline}</p>
              </div>

              <div className="mb-6">
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-bold">
                    ${isAnnual ? tier.annualPrice : tier.monthlyPrice}
                  </span>
                  <span className="text-muted-foreground">
                    /{isAnnual ? "year" : "month"}
                  </span>
                </div>
              </div>

              <Button
                className="w-full mb-6"
                variant={tier.popular ? "default" : "outline"}
                data-testid={`button-select-${tier.name.toLowerCase()}`}
              >
                {tier.monthlyPrice === 0 ? "Get Started Free" : "Start 14-Day Trial"}
              </Button>

              <ul className="space-y-3">
                {tier.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start gap-3">
                    <Check className="h-5 w-5 text-accent flex-shrink-0 mt-0.5" />
                    <span className="text-sm">{feature}</span>
                  </li>
                ))}
              </ul>
            </Card>
          ))}
        </div>

        <p className="text-sm text-muted-foreground text-center mt-8">
          All plans include 14-day free trial · Credit card required · Cancel anytime
        </p>
      </div>
    </section>
  );
}
