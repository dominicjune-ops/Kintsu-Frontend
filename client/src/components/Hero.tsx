import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import { Link } from "wouter";
import heroImage from "@assets/generated_images/kintsugi_pottery_with_gold_seams.png";

export function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 z-0">
        <img
          src={heroImage}
          alt="Kintsugi pottery with golden seams"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-primary/90 via-primary/80 to-primary/70" />
      </div>

      <div className="container relative z-10 mx-auto px-4 md:px-6 py-20 md:py-32">
        <div className="max-w-3xl">
          <h1 className="text-4xl md:text-6xl font-bold font-serif mb-6 text-primary-foreground leading-tight">
            Transform your career setbacks into golden opportunities
          </h1>
          <p className="text-lg md:text-xl text-primary-foreground/90 mb-8 leading-relaxed">
            Instant resume tailoring, AI-powered coaching, and job-match recommendations — built to help you get interviews faster.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <Button
              asChild
              size="lg"
              className="bg-accent hover:bg-accent/90 text-accent-foreground text-lg px-8"
              data-testid="button-hero-start-trial"
            >
              <a href="https://app.kintsu.io">
                Start 14-Day Pro Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </a>
            </Button>
            <Button
              asChild
              size="lg"
              variant="outline"
              className="text-lg px-8 bg-primary-foreground/10 backdrop-blur-sm border-primary-foreground/20 text-primary-foreground hover:bg-primary-foreground/20"
              data-testid="button-hero-view-pricing"
            >
              <Link href="/pricing">
                <a>View Pricing & Features</a>
              </Link>
            </Button>
          </div>

          <p className="text-sm text-primary-foreground/70">
            Credit card required · Cancel anytime
          </p>
        </div>
      </div>
    </section>
  );
}
