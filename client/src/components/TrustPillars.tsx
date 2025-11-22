import { Shield, Target, TrendingUp } from "lucide-react";
import { Card } from "@/components/ui/card";

const pillars = [
  {
    icon: Target,
    title: "Proven AI Tailoring",
    description: "ATS-optimized resumes and role-fit recommendations that improve interview rates.*"
  },
  {
    icon: Shield,
    title: "Privacy-First",
    description: "Your data is encrypted and secure. We never share your information without permission."
  },
  {
    icon: TrendingUp,
    title: "Real Outcomes",
    description: "Transparent benchmarks and honest claims. See our methodology for details."
  }
];

export function TrustPillars() {
  return (
    <section className="py-20 md:py-32 bg-background">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold font-serif mb-4">Why Kintsu</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Built on trust, powered by precision, designed for your success
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {pillars.map((pillar, index) => (
            <Card
              key={index}
              className="p-8 hover-elevate transition-all duration-200"
              data-testid={`card-pillar-${index}`}
            >
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-md bg-accent/10 mb-4">
                <pillar.icon className="h-6 w-6 text-accent" />
              </div>
              <h3 className="text-xl font-semibold mb-3">{pillar.title}</h3>
              <p className="text-muted-foreground leading-relaxed">{pillar.description}</p>
            </Card>
          ))}
        </div>

        <p className="text-sm text-muted-foreground text-center mt-8">
          * Based on internal benchmarks. <a href="/methodology" className="text-accent hover:underline">See our methodology</a>
        </p>
      </div>
    </section>
  );
}
