import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  X,
  Target,
  TrendingUp,
  Trophy,
  AlertCircle,
  Briefcase,
  Star
} from "lucide-react";
import { signalVariants } from "@/lib/interactions";

export type SignalType =
  | "job_match"
  | "skill_gap"
  | "milestone_achieved"
  | "interview_tip"
  | "market_trend"
  | "achievement";

interface SignalCardProps {
  id: string;
  type: SignalType;
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  onDismiss: (id: string) => void;
  autoDismissSeconds?: number;
}

const SIGNAL_CONFIG = {
  job_match: {
    icon: Briefcase,
    gradient: "from-blue-500 to-indigo-600",
    bgColor: "bg-blue-500/10",
    borderColor: "border-blue-500/20"
  },
  skill_gap: {
    icon: TrendingUp,
    gradient: "from-amber-500 to-orange-600",
    bgColor: "bg-amber-500/10",
    borderColor: "border-amber-500/20"
  },
  milestone_achieved: {
    icon: Trophy,
    gradient: "from-accent to-accent/60",
    bgColor: "bg-accent/10",
    borderColor: "border-accent/20"
  },
  interview_tip: {
    icon: Target,
    gradient: "from-purple-500 to-pink-600",
    bgColor: "bg-purple-500/10",
    borderColor: "border-purple-500/20"
  },
  market_trend: {
    icon: TrendingUp,
    gradient: "from-green-500 to-emerald-600",
    bgColor: "bg-green-500/10",
    borderColor: "border-green-500/20"
  },
  achievement: {
    icon: Star,
    gradient: "from-accent to-accent/60",
    bgColor: "bg-accent/10",
    borderColor: "border-accent/20"
  }
};

export function SignalCard({
  id,
  type,
  title,
  description,
  action,
  onDismiss,
  autoDismissSeconds = 8
}: SignalCardProps) {
  const [progress, setProgress] = useState(100);
  const config = SIGNAL_CONFIG[type];
  const Icon = config.icon;

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        const newProgress = prev - (100 / (autoDismissSeconds * 10));
        if (newProgress <= 0) {
          clearInterval(interval);
          onDismiss(id);
          return 0;
        }
        return newProgress;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [id, autoDismissSeconds, onDismiss]);

  const handleActionClick = () => {
    if (action?.onClick) {
      action.onClick();
      onDismiss(id);
    }
  };

  return (
    <motion.div
      variants={signalVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      layout
    >
      <Card className={`relative overflow-hidden border ${config.borderColor} ${config.bgColor} backdrop-blur-sm`}>
        {/* Background Gradient */}
        <div className={`absolute inset-0 bg-gradient-to-br ${config.gradient} opacity-5`} />

        {/* Content */}
        <div className="relative p-4 space-y-3">
          {/* Header */}
          <div className="flex items-start gap-3">
            {/* Icon */}
            <div className={`flex-shrink-0 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-gradient-to-br ${config.gradient} text-white`}>
              <Icon className="h-5 w-5" />
            </div>

            {/* Text */}
            <div className="flex-1 min-w-0 space-y-1">
              <h3 className="font-semibold text-sm leading-tight">{title}</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                {description}
              </p>
            </div>

            {/* Dismiss Button */}
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onDismiss(id)}
              className="flex-shrink-0 h-6 w-6 rounded-full hover:bg-background/50"
            >
              <X className="h-3 w-3" />
            </Button>
          </div>

          {/* Action Button */}
          {action && (
            <Button
              onClick={handleActionClick}
              size="sm"
              className={`w-full bg-gradient-to-r ${config.gradient} text-white hover:opacity-90`}
            >
              {action.label}
            </Button>
          )}

          {/* Auto-dismiss Progress */}
          <div className="space-y-1">
            <Progress value={progress} className="h-1" />
          </div>
        </div>
      </Card>
    </motion.div>
  );
}

// Container component for managing multiple signals
interface SignalContainerProps {
  signals: Array<Omit<SignalCardProps, "onDismiss">>;
  onDismissSignal?: (id: string) => void;
}

export function SignalContainer({ signals: initialSignals, onDismissSignal }: SignalContainerProps) {
  const [signals, setSignals] = useState(initialSignals);

  const handleDismiss = (id: string) => {
    setSignals((prev) => prev.filter((signal) => signal.id !== id));
    onDismissSignal?.(id);
  };

  return (
    <div className="fixed top-20 right-4 z-50 w-full max-w-sm space-y-3 pointer-events-none">
      <AnimatePresence mode="popLayout">
        {signals.map((signal) => (
          <div key={signal.id} className="pointer-events-auto">
            <SignalCard {...signal} onDismiss={handleDismiss} />
          </div>
        ))}
      </AnimatePresence>
    </div>
  );
}
