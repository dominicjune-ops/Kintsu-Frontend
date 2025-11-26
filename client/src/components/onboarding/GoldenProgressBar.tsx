import { motion } from "framer-motion";

interface GoldenProgressBarProps {
  currentStep: number;
  totalSteps: number;
  label?: string;
}

const STEP_LABELS = [
  "Setting foundations...",
  "Building momentum...",
  "Igniting your path..."
];

export function GoldenProgressBar({
  currentStep,
  totalSteps,
  label
}: GoldenProgressBarProps) {
  const progress = (currentStep / totalSteps) * 100;
  const stepLabel = label || STEP_LABELS[currentStep - 1] || "Loading...";

  return (
    <div className="w-full space-y-3">
      {/* Progress Text */}
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-foreground">{stepLabel}</span>
        <span className="text-muted-foreground">
          {currentStep} of {totalSteps}
        </span>
      </div>

      {/* Progress Bar Container */}
      <div className="relative h-2 w-full overflow-hidden rounded-full bg-secondary">
        {/* Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-r from-primary via-accent/50 to-accent opacity-20" />

        {/* Progress Fill */}
        <motion.div
          className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-accent to-accent/80"
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{
            type: "spring",
            stiffness: 100,
            damping: 20,
            duration: 0.6
          }}
          style={{
            boxShadow: "0 0 20px rgba(212, 165, 116, 0.5)"
          }}
        >
          {/* Shimmer Effect */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent"
            animate={{
              x: ["-100%", "200%"]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "linear"
            }}
          />
        </motion.div>
      </div>

      {/* Step Indicators */}
      <div className="flex justify-between">
        {Array.from({ length: totalSteps }).map((_, index) => {
          const stepNumber = index + 1;
          const isCompleted = stepNumber < currentStep;
          const isCurrent = stepNumber === currentStep;

          return (
            <motion.div
              key={stepNumber}
              className={`flex h-8 w-8 items-center justify-center rounded-full text-xs font-semibold transition-colors ${
                isCompleted
                  ? "bg-accent text-accent-foreground"
                  : isCurrent
                  ? "bg-accent/20 text-accent ring-2 ring-accent"
                  : "bg-muted text-muted-foreground"
              }`}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{
                scale: isCurrent ? 1.1 : 1,
                opacity: 1
              }}
              transition={{
                type: "spring",
                stiffness: 300,
                damping: 20
              }}
            >
              {isCompleted ? (
                <svg
                  className="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={3}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              ) : (
                stepNumber
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
