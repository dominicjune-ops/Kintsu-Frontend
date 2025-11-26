import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, Target, TrendingUp, Zap } from "lucide-react";
import type { CareerGoal } from "./GoalSelection";

interface PathGenerationProps {
  goal: CareerGoal;
  fileName: string;
  onComplete: () => void;
}

const GENERATION_STEPS = [
  { icon: Sparkles, text: "Analyzing your experience" },
  { icon: Target, text: "Identifying your strengths" },
  { icon: TrendingUp, text: "Mapping career opportunities" },
  { icon: Zap, text: "Crafting your golden path" }
];

export function PathGeneration({ goal, fileName, onComplete }: PathGenerationProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Progress animation
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 2;
      });
    }, 50);

    // Step progression
    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev >= GENERATION_STEPS.length - 1) {
          clearInterval(stepInterval);
          return prev;
        }
        return prev + 1;
      });
    }, 1200);

    // Auto-complete after animation
    const completeTimeout = setTimeout(() => {
      onComplete();
    }, 5500);

    return () => {
      clearInterval(progressInterval);
      clearInterval(stepInterval);
      clearTimeout(completeTimeout);
    };
  }, [onComplete]);

  const goalText = {
    promotion: "advancing your career",
    pivot: "your career transition",
    growth: "expanding your expertise"
  }[goal];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.4 }}
      className="space-y-12"
    >
      {/* Header */}
      <div className="text-center space-y-3">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 200, damping: 20 }}
          className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-br from-accent to-accent/60 mb-4"
        >
          <motion.div
            animate={{
              rotate: [0, 360],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: "linear"
            }}
          >
            <Sparkles className="h-12 w-12 text-white" />
          </motion.div>
        </motion.div>

        <h2 className="text-3xl md:text-4xl font-bold font-serif bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
          Constructing your golden path
        </h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          We're personalizing your journey for {goalText}
        </p>
      </div>

      {/* Progress Circle */}
      <div className="max-w-2xl mx-auto">
        <div className="relative">
          {/* Background Card */}
          <div className="relative overflow-hidden rounded-2xl border bg-card p-8 md:p-12">
            {/* Animated Background */}
            <div className="absolute inset-0 opacity-5">
              <motion.div
                className="absolute inset-0 bg-gradient-to-br from-accent via-primary to-accent"
                animate={{
                  rotate: [0, 360],
                }}
                transition={{
                  duration: 20,
                  repeat: Infinity,
                  ease: "linear"
                }}
              />
            </div>

            {/* Content */}
            <div className="relative space-y-8">
              {/* Circular Progress */}
              <div className="flex justify-center">
                <div className="relative">
                  <svg className="w-40 h-40 transform -rotate-90">
                    {/* Background circle */}
                    <circle
                      cx="80"
                      cy="80"
                      r="70"
                      stroke="currentColor"
                      strokeWidth="8"
                      fill="none"
                      className="text-muted"
                    />
                    {/* Progress circle */}
                    <motion.circle
                      cx="80"
                      cy="80"
                      r="70"
                      stroke="url(#gradient)"
                      strokeWidth="8"
                      fill="none"
                      strokeLinecap="round"
                      strokeDasharray={`${2 * Math.PI * 70}`}
                      initial={{ strokeDashoffset: 2 * Math.PI * 70 }}
                      animate={{
                        strokeDashoffset: 2 * Math.PI * 70 * (1 - progress / 100)
                      }}
                      transition={{ duration: 0.3 }}
                    />
                    <defs>
                      <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="hsl(var(--accent))" />
                        <stop offset="100%" stopColor="hsl(var(--primary))" />
                      </linearGradient>
                    </defs>
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                      {Math.round(progress)}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Generation Steps */}
              <div className="space-y-4">
                {GENERATION_STEPS.map((step, index) => {
                  const Icon = step.icon;
                  const isActive = index === currentStep;
                  const isCompleted = index < currentStep;

                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{
                        opacity: isCompleted || isActive ? 1 : 0.4,
                        x: 0
                      }}
                      transition={{ delay: index * 0.1 }}
                      className="flex items-center gap-4"
                    >
                      <div
                        className={`flex h-10 w-10 items-center justify-center rounded-full transition-all ${
                          isCompleted
                            ? "bg-accent text-accent-foreground"
                            : isActive
                            ? "bg-accent/20 text-accent ring-2 ring-accent"
                            : "bg-muted text-muted-foreground"
                        }`}
                      >
                        {isCompleted ? (
                          <svg
                            className="h-5 w-5"
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
                          <Icon className="h-5 w-5" />
                        )}
                      </div>

                      <div className="flex-1">
                        <p
                          className={`font-medium ${
                            isActive ? "text-foreground" : "text-muted-foreground"
                          }`}
                        >
                          {step.text}
                        </p>
                      </div>

                      {isActive && (
                        <motion.div
                          className="flex gap-1"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                        >
                          {[0, 1, 2].map((i) => (
                            <motion.div
                              key={i}
                              className="h-2 w-2 rounded-full bg-accent"
                              animate={{
                                scale: [1, 1.5, 1],
                                opacity: [0.3, 1, 0.3]
                              }}
                              transition={{
                                duration: 1,
                                repeat: Infinity,
                                delay: i * 0.2
                              }}
                            />
                          ))}
                        </motion.div>
                      )}
                    </motion.div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Info */}
      <div className="text-center">
        <p className="text-sm text-muted-foreground">
          Analyzing <span className="font-medium text-foreground">{fileName}</span>
        </p>
      </div>
    </motion.div>
  );
}
