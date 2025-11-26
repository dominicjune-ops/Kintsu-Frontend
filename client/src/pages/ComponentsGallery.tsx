import { Hero } from "@/components/Hero";
import { TrustPillars } from "@/components/TrustPillars";
import { Features } from "@/components/Features";
import { PricingTable } from "@/components/PricingTable";
import { Testimonials } from "@/components/Testimonials";
import { GoldSeamDivider } from "@/components/GoldSeamDivider";
import { ContactForm } from "@/components/ContactForm";
import { EmployerJobForm } from "@/components/EmployerJobForm";
import { JobCard } from "@/components/JobCard";
import { ThemeToggle } from "@/components/ThemeToggle";

const ComponentsGallery = () => {
  return (
    <div className="container mx-auto p-4 space-y-8">
      <h1 className="text-3xl font-bold text-center">Components Gallery</h1>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Hero</h2>
        <Hero />
      </section>

      <GoldSeamDivider />

      <section>
        <h2 className="text-2xl font-semibold mb-4">Trust Pillars</h2>
        <TrustPillars />
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Features</h2>
        <Features />
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Testimonials</h2>
        <Testimonials />
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Pricing Table</h2>
        <PricingTable />
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Contact Form</h2>
        <ContactForm />
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Employer Job Form</h2>
        <EmployerJobForm />
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Job Card</h2>
        <JobCard
          title="Sample Job"
          company="Sample Company"
          location="Remote"
          salary="$50k - $70k"
          type="Full-time"
          tags={["React", "TypeScript"]}
          description="This is a sample job description."
        />
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Theme Toggle</h2>
        <ThemeToggle />
      </section>
    </div>
  );
};

export default ComponentsGallery;