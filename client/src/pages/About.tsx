import { Card } from "@/components/ui/card";
import { ContactForm } from "@/components/ContactForm";
import kintsugiTexture from "@assets/generated_images/abstract_gold_seams_on_indigo.png";

export default function About() {
  return (
    <div>
      <section className="relative py-20 md:py-32 overflow-hidden">
        <div className="absolute inset-0 z-0 opacity-20">
          <img
            src={kintsugiTexture}
            alt=""
            className="w-full h-full object-cover"
          />
        </div>
        <div className="container relative z-10 mx-auto px-4 md:px-6">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl md:text-5xl font-bold font-serif mb-6">
              The Philosophy Behind Kintsu
            </h1>
            <div className="h-1 w-24 bg-gradient-to-r from-accent to-transparent mb-8" />
            <div className="prose prose-lg max-w-none">
              <p className="text-lg text-muted-foreground leading-relaxed mb-6">
                Kintsugi is the Japanese art of repairing broken pottery with gold lacquer — a philosophy that celebrates damage and renewal. At Kintsu, we borrow that spirit: we help professionals transform career setbacks into stronger, more beautiful trajectories.
              </p>
              <p className="text-lg text-muted-foreground leading-relaxed">
                Instead of hiding breaks, we fill them with gold — new skills, sharper resumes, and smarter applications — so the final piece is more valuable than it was before.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-20 md:py-32 bg-card">
        <div className="container mx-auto px-4 md:px-6">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold font-serif mb-8 text-center">
              Our Mission
            </h2>
            <Card className="p-8 md:p-12">
              <p className="text-lg text-muted-foreground leading-relaxed mb-6">
                We built Kintsu because we believe that career setbacks shouldn't define you — they should refine you. Whether you're facing rejections, career gaps, or transitions, our AI-powered tools help you present your best self to employers.
              </p>
              <p className="text-lg text-muted-foreground leading-relaxed">
                We're committed to transparency, privacy, and real results. No false promises, just practical tools that help you get interviews and land the roles you deserve.
              </p>
            </Card>
          </div>
        </div>
      </section>

      <section className="py-20 md:py-32 bg-background">
        <div className="container mx-auto px-4 md:px-6">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold font-serif mb-8 text-center">
              Our Values
            </h2>
            <div className="grid md:grid-cols-3 gap-8 mb-16">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-md bg-accent/10 mb-4">
                  <div className="h-6 w-6 rounded-full bg-accent" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Transparency</h3>
                <p className="text-muted-foreground">
                  Honest claims, clear benchmarks, and open methodology
                </p>
              </div>
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-md bg-accent/10 mb-4">
                  <div className="h-6 w-6 rounded-full bg-accent" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Privacy</h3>
                <p className="text-muted-foreground">
                  Your data is yours, encrypted and never shared
                </p>
              </div>
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-md bg-accent/10 mb-4">
                  <div className="h-6 w-6 rounded-full bg-accent" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Excellence</h3>
                <p className="text-muted-foreground">
                  AI-powered precision meets human-centered design
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-20 md:py-32 bg-card">
        <div className="container mx-auto px-4 md:px-6">
          <div className="max-w-2xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold font-serif mb-4 text-center">
              Get in Touch
            </h2>
            <p className="text-lg text-muted-foreground mb-8 text-center">
              Have questions or feedback? We'd love to hear from you.
            </p>
            <Card className="p-8">
              <ContactForm />
            </Card>
          </div>
        </div>
      </section>
    </div>
  );
}
