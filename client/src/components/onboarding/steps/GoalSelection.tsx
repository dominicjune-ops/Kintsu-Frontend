import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import { TrendingUp, Shuffle, Rocket } from "lucide-react";
import { cardHoverVariants } from "@/lib/interactions";

export type CareerGoal = "promotion" | "pivot" | "growth";

interface GoalSelectionProps {
  selectedGoal: CareerGoal | null;
  onSelectGoal: (goal: CareerGoal) => void;
}

const GOALS = [
  {
    id: "promotion" as CareerGoal,
    icon: TrendingUp,
    title: "Level Up",
    subtitle: "Promotion",
    description: "Climb the ladder in your current field",
    color: "from-blue-500 to-indigo-600"
  },
  {
    id: "pivot" as CareerGoal,
    icon: Shuffle,
    title: "New Direction",
    subtitle: "Career Pivot",
    description: "Transition to a different industry or role",
    color: "from-purple-500 to-pink-600"
  },
  {
    id: "growth" as CareerGoal,
    icon: Rocket,
    title: "Expand Skills",
    subtitle: "Professional Growth",
    description: "Develop expertise and broaden your skillset",
    color: "from-amber-500 to-orange-600"
  }
];

export function GoalSelection({ selectedGoal, onSelectGoal }: GoalSelectionProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.4 }}
      className="space-y-8"
    >
      {/* Header */}
      <div className="text-center space-y-3">
        <h2 className="text-3xl md:text-4xl font-bold font-serif bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
          What's your career goal?
        </h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Choose the path that resonates with your ambitions. We'll tailor your experience accordingly.
        </p>
      </div>

      {/* Goal Cards */}
      <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
        {GOALS.map((goal) => {
          const isSelected = selectedGoal === goal.id;
          const Icon = goal.icon;

          return (
            <motion.div
              key={goal.id}
              variants={cardHoverVariants}
              initial="initial"
              whileHover="hover"
              whileTap={{ scale: 0.98 }}
            >
              <Card
                onClick={() => onSelectGoal(goal.id)}
                className={`relative overflow-hidden cursor-pointer transition-all duration-300 ${
                  isSelected
                    ? "ring-2 ring-accent shadow-xl shadow-accent/20"
                    : "hover:shadow-lg"
                }`}
              >
                {/* Background Gradient */}
                <div
                  className={`absolute inset-0 bg-gradient-to-br ${goal.color} opacity-0 ${
                    isSelected ? "opacity-10" : ""
                  } transition-opacity duration-300`}
                />

                {/* Content */}
                <div className="relative p-6 space-y-4">
                  {/* Icon */}
                  <div
                    className={`inline-flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-br ${goal.color} text-white`}
                  >
                    <Icon className="h-7 w-7" />
                  </div>

                  {/* Text */}
                  <div className="space-y-2">
                    <div className="space-y-1">
                      <p className="text-sm font-medium text-muted-foreground">
                        {goal.title}
                      </p>
                      <h3 className="text-2xl font-bold font-serif">
                        {goal.subtitle}
                      </h3>
                    </div>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {goal.description}
                    </p>
                  </div>

                  {/* Selection Indicator */}
                  {isSelected && (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="absolute top-4 right-4"
                    >
                      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-accent text-accent-foreground">
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
                      </div>
                    </motion.div>
                  )}
                </div>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Helper Text */}
      <p className="text-center text-sm text-muted-foreground">
        Don't worry, you can always adjust this later
      </p>
    </motion.div>
  );
}
