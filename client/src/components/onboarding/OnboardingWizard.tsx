import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { useLocation } from "wouter";
import { Button } from "@/components/ui/button";
import { X, ArrowLeft, ArrowRight } from "lucide-react";
import { GoldenProgressBar } from "./GoldenProgressBar";
import { GoalSelection, type CareerGoal } from "./steps/GoalSelection";
import { ResumeUpload } from "./steps/ResumeUpload";
import { PathGeneration } from "./steps/PathGeneration";
import { celebrateMilestone } from "@/lib/interactions";

export interface OnboardingData {
  goal: CareerGoal | null;
  resume: File | null;
}

interface OnboardingWizardProps {
  onComplete?: (data: OnboardingData) => void;
}

const TOTAL_STEPS = 3;

export function OnboardingWizard({ onComplete }: OnboardingWizardProps) {
  const [, setLocation] = useLocation();
  const [currentStep, setCurrentStep] = useState(1);
  const [data, setData] = useState<OnboardingData>({
    goal: null,
    resume: null,
  });

  const handleGoalSelect = (goal: CareerGoal) => {
    setData((prev) => ({ ...prev, goal }));
  };

  const handleFileSelect = (file: File) => {
    setData((prev) => ({ ...prev, resume: file }));
  };

  const handleNext = () => {
    if (currentStep < TOTAL_STEPS) {
      setCurrentStep((prev) => prev + 1);
      celebrateMilestone();
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep((prev) => prev - 1);
    }
  };

  const handleComplete = () => {
    celebrateMilestone();
    if (onComplete) {
      onComplete(data);
    }
    // Redirect to dashboard after completion
    setTimeout(() => {
      setLocation("/app/dashboard");
    }, 1000);
  };

  const handleClose = () => {
    setLocation("/");
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return data.goal !== null;
      case 2:
        return data.resume !== null;
      case 3:
        return false; // Step 3 auto-completes
      default:
        return false;
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between px-4 md:px-6">
          <div className="flex items-center space-x-2">
            <span className="text-2xl font-bold font-serif bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Kintsu
            </span>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={handleClose}
            className="rounded-full"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>
      </header>

      {/* Progress Bar */}
      <div className="border-b bg-card">
        <div className="container px-4 md:px-6 py-6">
          <GoldenProgressBar currentStep={currentStep} totalSteps={TOTAL_STEPS} />
        </div>
      </div>

      {/* Main Content */}
      <main className="flex-1 container px-4 md:px-6 py-12">
        <AnimatePresence mode="wait">
          {currentStep === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 300 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -300 }}
              transition={{ duration: 0.4, ease: "easeInOut" }}
            >
              <GoalSelection
                selectedGoal={data.goal}
                onSelectGoal={handleGoalSelect}
              />
            </motion.div>
          )}

          {currentStep === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 300 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -300 }}
              transition={{ duration: 0.4, ease: "easeInOut" }}
            >
              <ResumeUpload file={data.resume} onFileSelect={handleFileSelect} />
            </motion.div>
          )}

          {currentStep === 3 && data.goal && data.resume && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 300 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -300 }}
              transition={{ duration: 0.4, ease: "easeInOut" }}
            >
              <PathGeneration
                goal={data.goal}
                fileName={data.resume.name}
                onComplete={handleComplete}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Navigation Footer */}
      {currentStep < 3 && (
        <footer className="sticky bottom-0 w-full border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container flex items-center justify-between px-4 md:px-6 py-4">
            <Button
              variant="ghost"
              onClick={handleBack}
              disabled={currentStep === 1}
              className="gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back
            </Button>

            <div className="flex items-center gap-2">
              <Button
                onClick={handleNext}
                disabled={!canProceed()}
                className="gap-2 bg-accent hover:bg-accent/90 text-accent-foreground"
              >
                {currentStep === TOTAL_STEPS - 1 ? "Generate Path" : "Continue"}
                <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </footer>
      )}
    </div>
  );
}
