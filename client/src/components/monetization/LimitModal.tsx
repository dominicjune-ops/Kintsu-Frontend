import { motion, AnimatePresence } from "framer-motion";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  CheckCircle2,
  Sparkles,
  Crown,
  X,
  ArrowRight,
  MessageSquare,
  FileText,
  TrendingUp,
  Zap
} from "lucide-react";
import { celebrateSmallWin } from "@/lib/interactions";

export type LimitType = "resume_repairs" | "coach_messages" | "insight_reports";

interface LimitModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  limitType: LimitType;
  currentUsage: number;
  limit: number;
  onUpgrade: () => void;
}

const LIMIT_CONFIG = {
  resume_repairs: {
    icon: FileText,
    title: "Resume Repairs",
    description: "You've successfully polished {count} resumes",
    ctaText: "Upgrade to polish unlimited resumes",
    color: "from-blue-500 to-indigo-600"
  },
  coach_messages: {
    icon: MessageSquare,
    title: "AI Coach Messages",
    description: "You've used {count} coaching sessions",
    ctaText: "Upgrade for unlimited AI coaching",
    color: "from-purple-500 to-pink-600"
  },
  insight_reports: {
    icon: TrendingUp,
    title: "Insight Reports",
    description: "You've generated {count} career insights",
    ctaText: "Upgrade for unlimited insights",
    color: "from-amber-500 to-orange-600"
  }
};

const PRO_FEATURES = [
  { icon: FileText, text: "Unlimited resume repairs" },
  { icon: MessageSquare, text: "Unlimited AI Coach access" },
  { icon: TrendingUp, text: "Advanced career insights" },
  { icon: Zap, text: "Priority job matching" },
];

export function LimitModal({
  open,
  onOpenChange,
  limitType,
  currentUsage,
  limit,
  onUpgrade
}: LimitModalProps) {
  const config = LIMIT_CONFIG[limitType];
  const Icon = config.icon;
  const description = config.description.replace("{count}", currentUsage.toString());

  const handleUpgrade = () => {
    celebrateSmallWin();
    onUpgrade();
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <AnimatePresence>
        {open && (
          <DialogContent className="sm:max-w-lg overflow-hidden p-0">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.2 }}
            >
              {/* Header with Gradient Background */}
              <div className={`relative overflow-hidden bg-gradient-to-br ${config.color} p-8 text-white`}>
                {/* Animated Background Pattern */}
                <div className="absolute inset-0 opacity-20">
                  <motion.div
                    className="absolute inset-0"
                    animate={{
                      backgroundPosition: ["0% 0%", "100% 100%"],
                    }}
                    transition={{
                      duration: 20,
                      repeat: Infinity,
                      ease: "linear"
                    }}
                    style={{
                      backgroundImage: "radial-gradient(circle, white 1px, transparent 1px)",
                      backgroundSize: "20px 20px"
                    }}
                  />
                </div>

                <div className="relative space-y-4">
                  {/* Icon */}
                  <motion.div
                    initial={{ scale: 0, rotate: -180 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{
                      type: "spring",
                      stiffness: 200,
                      damping: 15,
                      delay: 0.1
                    }}
                    className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-white/20 backdrop-blur-sm"
                  >
                    <Icon className="h-8 w-8" />
                  </motion.div>

                  {/* Title */}
                  <DialogHeader>
                    <DialogTitle className="text-3xl font-bold font-serif text-white flex items-center gap-2">
                      <Sparkles className="h-6 w-6" />
                      Unlock More
                    </DialogTitle>
                    <DialogDescription className="text-white/90 text-base">
                      {description}
                    </DialogDescription>
                  </DialogHeader>
                </div>
              </div>

              {/* Content */}
              <div className="p-8 space-y-6">
                {/* Progress Indicator */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Free Plan Usage</span>
                    <Badge variant="secondary" className="gap-1">
                      {currentUsage} / {limit} used
                    </Badge>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-secondary">
                    <motion.div
                      className={`h-full bg-gradient-to-r ${config.color}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${(currentUsage / limit) * 100}%` }}
                      transition={{ duration: 0.8, ease: "easeOut" }}
                    />
                  </div>
                </div>

                {/* CTA Message */}
                <div className="text-center space-y-2 py-4">
                  <p className="text-lg font-semibold">{config.ctaText}</p>
                  <p className="text-sm text-muted-foreground">
                    Ready to polish your entire career path?
                  </p>
                </div>

                {/* Pro Features */}
                <div className="rounded-xl border bg-card p-6 space-y-4">
                  <div className="flex items-center gap-2 mb-4">
                    <Crown className="h-5 w-5 text-accent" />
                    <h3 className="font-semibold text-lg">Pro Features</h3>
                  </div>

                  <div className="space-y-3">
                    {PRO_FEATURES.map((feature, index) => {
                      const FeatureIcon = feature.icon;
                      return (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.1 + 0.3 }}
                          className="flex items-center gap-3"
                        >
                          <div className="flex-shrink-0 flex h-8 w-8 items-center justify-center rounded-lg bg-accent/10">
                            <FeatureIcon className="h-4 w-4 text-accent" />
                          </div>
                          <span className="text-sm">{feature.text}</span>
                          <CheckCircle2 className="ml-auto h-4 w-4 text-green-500 flex-shrink-0" />
                        </motion.div>
                      );
                    })}
                  </div>
                </div>

                {/* Pricing */}
                <div className="text-center space-y-4">
                  <div className="inline-flex flex-col items-center gap-1 px-4 py-2 rounded-lg bg-accent/10">
                    <span className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                      $29
                    </span>
                    <span className="text-xs text-muted-foreground">per month</span>
                  </div>

                  <p className="text-xs text-muted-foreground">
                    Cancel anytime • No hidden fees
                  </p>
                </div>

                {/* Action Buttons */}
                <div className="space-y-3">
                  <Button
                    onClick={handleUpgrade}
                    className="w-full bg-gradient-to-r from-accent to-accent/80 hover:from-accent/90 hover:to-accent/70 text-accent-foreground gap-2 h-12 text-base font-semibold"
                  >
                    <Crown className="h-5 w-5" />
                    Upgrade to Pro
                    <ArrowRight className="h-5 w-5" />
                  </Button>

                  <Button
                    onClick={() => onOpenChange(false)}
                    variant="ghost"
                    className="w-full"
                  >
                    Maybe Later
                  </Button>
                </div>

                {/* Trust Badge */}
                <div className="text-center">
                  <p className="text-xs text-muted-foreground">
                    Join 10,000+ professionals who upgraded their careers
                  </p>
                </div>
              </div>
            </motion.div>
          </DialogContent>
        )}
      </AnimatePresence>
    </Dialog>
  );
}
