import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  CheckCircle2,
  Lock,
  ArrowRight,
  MessageSquare,
  TrendingUp,
  Map,
  Bell
} from "lucide-react";
import { cardHoverVariants } from "@/lib/interactions";
import { Link } from "wouter";

export type MilestoneStatus = "completed" | "active" | "upcoming" | "locked";
export type ModuleType = "coach" | "insights" | "pathways" | "signals" | "resume";

interface MilestoneCardProps {
  status: MilestoneStatus;
  module: ModuleType;
  layoutId: string;
  title: string;
  description: string;
  href?: string;
  unlockRequirement?: string;
  progressPercentage?: number;
}

const MODULE_CONFIG = {
  coach: {
    icon: MessageSquare,
    gradient: "from-blue-500 to-indigo-600",
    color: "text-blue-600 dark:text-blue-400"
  },
  insights: {
    icon: TrendingUp,
    gradient: "from-purple-500 to-pink-600",
    color: "text-purple-600 dark:text-purple-400"
  },
  pathways: {
    icon: Map,
    gradient: "from-amber-500 to-orange-600",
    color: "text-amber-600 dark:text-amber-400"
  },
  signals: {
    icon: Bell,
    gradient: "from-green-500 to-emerald-600",
    color: "text-green-600 dark:text-green-400"
  },
  resume: {
    icon: CheckCircle2,
    gradient: "from-slate-500 to-gray-600",
    color: "text-slate-600 dark:text-slate-400"
  }
};

export function MilestoneCard({
  status,
  module,
  layoutId,
  title,
  description,
  href,
  unlockRequirement,
  progressPercentage = 0
}: MilestoneCardProps) {
  const config = MODULE_CONFIG[module];
  const Icon = config.icon;

  const isCompleted = status === "completed";
  const isActive = status === "active";
  const isUpcoming = status === "upcoming";
  const isLocked = status === "locked";

  const cardContent = (
    <Card
      className={`relative overflow-hidden transition-all duration-300 h-full ${
        isCompleted
          ? "opacity-70 grayscale"
          : isActive
          ? "ring-2 ring-accent shadow-xl shadow-accent/20 scale-[1.02]"
          : isLocked
          ? "opacity-50 blur-[2px]"
          : ""
      } ${href && !isLocked ? "cursor-pointer hover:shadow-lg" : ""}`}
    >
      {/* Background Gradient */}
      <div
        className={`absolute inset-0 bg-gradient-to-br ${config.gradient} ${
          isActive ? "opacity-10" : "opacity-5"
        } transition-opacity duration-300`}
      />

      {/* Lock Overlay */}
      {isLocked && (
        <div className="absolute inset-0 z-10 flex items-center justify-center bg-background/80 backdrop-blur-sm">
          <div className="text-center space-y-2 p-4">
            <Lock className="h-8 w-8 mx-auto text-muted-foreground" />
            <p className="text-sm font-medium text-muted-foreground">
              {unlockRequirement || "Complete previous milestones to unlock"}
            </p>
          </div>
        </div>
      )}

      {/* Content */}
      <div className="relative p-6 space-y-4 h-full flex flex-col">
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          {/* Icon */}
          <div
            className={`flex-shrink-0 inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br ${config.gradient} text-white`}
          >
            <Icon className="h-6 w-6" />
          </div>

          {/* Status Badge */}
          <div>
            {isCompleted && (
              <Badge variant="secondary" className="gap-1">
                <CheckCircle2 className="h-3 w-3" />
                Completed
              </Badge>
            )}
            {isActive && (
              <Badge className="bg-accent text-accent-foreground gap-1 animate-pulse">
                <div className="h-2 w-2 rounded-full bg-accent-foreground" />
                In Progress
              </Badge>
            )}
            {isUpcoming && (
              <Badge variant="outline">Next</Badge>
            )}
          </div>
        </div>

        {/* Text */}
        <div className="flex-1 space-y-2">
          <h3 className="text-xl font-bold font-serif">{title}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {description}
          </p>
        </div>

        {/* Progress Bar (for active cards) */}
        {isActive && progressPercentage > 0 && (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">Progress</span>
              <span className="font-medium">{progressPercentage}%</span>
            </div>
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-secondary">
              <motion.div
                className={`h-full bg-gradient-to-r ${config.gradient}`}
                initial={{ width: 0 }}
                animate={{ width: `${progressPercentage}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
              />
            </div>
          </div>
        )}

        {/* Action Button */}
        {!isLocked && href && (
          <Button
            className={`w-full gap-2 ${
              isActive
                ? "bg-accent hover:bg-accent/90 text-accent-foreground"
                : ""
            }`}
            variant={isActive ? "default" : "outline"}
          >
            {isCompleted ? "View Again" : isActive ? "Continue" : "Start"}
            <ArrowRight className="h-4 w-4" />
          </Button>
        )}
      </div>

      {/* Completed Checkmark Overlay */}
      {isCompleted && (
        <div className="absolute top-4 right-4">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-accent text-accent-foreground">
            <CheckCircle2 className="h-5 w-5" />
          </div>
        </div>
      )}
    </Card>
  );

  if (href && !isLocked) {
    return (
      <Link href={href}>
        <motion.a
          layoutId={layoutId}
          variants={cardHoverVariants}
          initial="initial"
          whileHover={!isLocked ? "hover" : undefined}
          className="block h-full"
        >
          {cardContent}
        </motion.a>
      </Link>
    );
  }

  return (
    <motion.div
      layoutId={layoutId}
      variants={cardHoverVariants}
      initial="initial"
      whileHover={!isLocked ? "hover" : undefined}
      className="h-full"
    >
      {cardContent}
    </motion.div>
  );
}
