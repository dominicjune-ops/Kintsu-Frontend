import { Hero } from "@/components/Hero";
import { TrustPillars } from "@/components/TrustPillars";
import { Features } from "@/components/Features";
import { PricingTable } from "@/components/PricingTable";
import { Testimonials } from "@/components/Testimonials";
import { GoldSeamDivider } from "@/components/GoldSeamDivider";

export default function Home() {
  return (
    <div>
      <Hero />
      <GoldSeamDivider />
      <TrustPillars />
      <Features />
      <Testimonials />
      <PricingTable />
    </div>
  );
}
