import { Card } from "@/components/ui/card";
import { FileText, MessageSquare, Briefcase } from "lucide-react";
import { GoldSeamDivider } from "./GoldSeamDivider";

const features = [
  {
    icon: FileText,
    title: "Repair with Precision",
    description: "AI-powered resume tailoring that produces ATS-friendly, role-specific content in seconds. Each application is optimized for the job you want."
  },
  {
    icon: MessageSquare,
    title: "Learn & Level Up",
    description: "Interview coaching, salary negotiation guidance, and structured progress tracking to help you improve with every application."
  },
  {
    icon: Briefcase,
    title: "Trusted, Honest Results",
    description: "Transparent claims, clear benchmarks, and privacy-first data handling. We're committed to helping you succeed authentically."
  }
];

export function Features() {
  return (
    <section className="py-20 md:py-32 bg-card">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold font-serif mb-4">
            Everything you need to transform your career
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            From resume repair to interview prep, we've got you covered
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {features.map((feature, index) => (
            <div key={index} className="space-y-4" data-testid={`feature-${index}`}>
              <div className="inline-flex items-center justify-center w-14 h-14 rounded-md bg-primary text-primary-foreground">
                <feature.icon className="h-7 w-7" />
              </div>
              <h3 className="text-2xl font-semibold font-serif">{feature.title}</h3>
              <p className="text-muted-foreground leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        <GoldSeamDivider />
      </div>
    </section>
  );
}
