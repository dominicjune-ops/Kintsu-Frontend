import { useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { MilestoneCard, type MilestoneStatus, type ModuleType } from "./MilestoneCard";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Milestone {
  id: string;
  status: MilestoneStatus;
  module: ModuleType;
  title: string;
  description: string;
  href?: string;
  unlockRequirement?: string;
  progressPercentage?: number;
}

interface JourneyMapProps {
  milestones: Milestone[];
}

export function JourneyMap({ milestones }: JourneyMapProps) {
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to active milestone on mount
  useEffect(() => {
    const activeIndex = milestones.findIndex((m) => m.status === "active");
    if (activeIndex !== -1 && scrollContainerRef.current) {
      const container = scrollContainerRef.current;
      const activeCard = container.children[activeIndex] as HTMLElement;
      if (activeCard) {
        const scrollPosition =
          activeCard.offsetLeft -
          container.offsetWidth / 2 +
          activeCard.offsetWidth / 2;
        container.scrollTo({
          left: scrollPosition,
          behavior: "smooth",
        });
      }
    }
  }, [milestones]);

  const scroll = (direction: "left" | "right") => {
    if (scrollContainerRef.current) {
      const scrollAmount = 400;
      scrollContainerRef.current.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  return (
    <div className="relative space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h2 className="text-2xl md:text-3xl font-bold font-serif bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            Your Journey
          </h2>
          <p className="text-muted-foreground">
            Transform setbacks into golden opportunities
          </p>
        </div>

        {/* Desktop Navigation Buttons */}
        <div className="hidden md:flex gap-2">
          <Button
            variant="outline"
            size="icon"
            onClick={() => scroll("left")}
            className="rounded-full"
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            onClick={() => scroll("right")}
            className="rounded-full"
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Timeline Container */}
      <div className="relative">
        {/* Timeline Line */}
        <div className="absolute top-[4.5rem] left-0 right-0 h-1 bg-gradient-to-r from-muted via-accent/20 to-muted -z-10 hidden md:block" />

        {/* Scrollable Cards Container */}
        <div className="relative">
          {/* Left Fade Overlay */}
          <div className="absolute left-0 top-0 bottom-0 w-20 bg-gradient-to-r from-background to-transparent z-10 pointer-events-none hidden md:block" />

          {/* Right Fade Overlay */}
          <div className="absolute right-0 top-0 bottom-0 w-20 bg-gradient-to-l from-background to-transparent z-10 pointer-events-none hidden md:block" />

          {/* Scrollable Container */}
          <div
            ref={scrollContainerRef}
            className="flex gap-6 overflow-x-auto pb-4 snap-x snap-mandatory scrollbar-hide md:px-10"
            style={{
              scrollbarWidth: "none",
              msOverflowStyle: "none",
            }}
          >
            {milestones.map((milestone, index) => (
              <motion.div
                key={milestone.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex-shrink-0 w-80 snap-center"
              >
                <MilestoneCard
                  layoutId={milestone.id}
                  status={milestone.status}
                  module={milestone.module}
                  title={milestone.title}
                  description={milestone.description}
                  href={milestone.href}
                  unlockRequirement={milestone.unlockRequirement}
                  progressPercentage={milestone.progressPercentage}
                />
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Mobile Scroll Hint */}
      <div className="md:hidden text-center">
        <p className="text-xs text-muted-foreground">
          Swipe to explore your journey →
        </p>
      </div>
    </div>
  );
}

// Hide scrollbar utility
const styles = `
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
`;

// Inject styles
if (typeof document !== "undefined") {
  const styleSheet = document.createElement("style");
  styleSheet.textContent = styles;
  document.head.appendChild(styleSheet);
}
