import { useState } from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LimitModal, type LimitType } from "@/components/monetization/LimitModal";
import { useUsageLimits } from "@/hooks/useUsageLimits";
import { FileText, MessageSquare, TrendingUp, Crown } from "lucide-react";

export default function DemoLimits() {
  const [modalOpen, setModalOpen] = useState(false);
  const [currentLimitType, setCurrentLimitType] = useState<LimitType>("resume_repairs");

  const { usage, isPro, incrementUsage, checkLimit, upgradeToPro, resetUsage } = useUsageLimits();

  const handleAction = (type: LimitType) => {
    const canProceed = incrementUsage(type);

    if (!canProceed) {
      setCurrentLimitType(type);
      setModalOpen(true);
    } else {
      alert(`Action completed! You've now used this feature ${checkLimit(type).current} times.`);
    }
  };

  const handleUpgrade = () => {
    upgradeToPro();
    setModalOpen(false);
    alert("Welcome to Kintsu Pro! You now have unlimited access to all features.");
  };

  const limits = {
    resume_repairs: checkLimit("resume_repairs"),
    coach_messages: checkLimit("coach_messages"),
    insight_reports: checkLimit("insight_reports"),
  };

  return (
    <DashboardLayout>
      <div className="container px-4 md:px-6 py-8 space-y-8">
        {/* Header */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl md:text-4xl font-bold font-serif">
              Usage Limits Demo
            </h1>
            {isPro && (
              <Badge className="gap-1 bg-gradient-to-r from-accent to-accent/80">
                <Crown className="h-3 w-3" />
                Pro Member
              </Badge>
            )}
          </div>
          <p className="text-muted-foreground">
            Test the contextual monetization system
          </p>
        </div>

        {/* Plan Status */}
        <Card className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-lg">Current Plan</h3>
              <p className="text-sm text-muted-foreground">
                {isPro ? "Pro - Unlimited access" : "Free - Limited usage"}
              </p>
            </div>
            {!isPro && (
              <Button
                onClick={() => {
                  setCurrentLimitType("resume_repairs");
                  setModalOpen(true);
                }}
                className="bg-gradient-to-r from-accent to-accent/80"
              >
                <Crown className="mr-2 h-4 w-4" />
                Upgrade to Pro
              </Button>
            )}
          </div>

          {!isPro && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t">
              <UsageCard
                icon={FileText}
                title="Resume Repairs"
                current={limits.resume_repairs.current}
                limit={limits.resume_repairs.limit}
                color="from-blue-500 to-indigo-600"
              />
              <UsageCard
                icon={MessageSquare}
                title="Coach Messages"
                current={limits.coach_messages.current}
                limit={limits.coach_messages.limit}
                color="from-purple-500 to-pink-600"
              />
              <UsageCard
                icon={TrendingUp}
                title="Insight Reports"
                current={limits.insight_reports.current}
                limit={limits.insight_reports.limit}
                color="from-amber-500 to-orange-600"
              />
            </div>
          )}
        </Card>

        {/* Test Actions */}
        <Card className="p-6 space-y-4">
          <h3 className="font-semibold text-lg">Test Limit Triggers</h3>
          <p className="text-sm text-muted-foreground">
            Click these buttons to simulate actions and trigger the limit modal
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button
              onClick={() => handleAction("resume_repairs")}
              variant="outline"
              className="h-auto py-4 flex-col gap-2"
            >
              <FileText className="h-6 w-6" />
              <span>Repair Resume</span>
              <span className="text-xs text-muted-foreground">
                ({limits.resume_repairs.current}/{limits.resume_repairs.limit})
              </span>
            </Button>

            <Button
              onClick={() => handleAction("coach_messages")}
              variant="outline"
              className="h-auto py-4 flex-col gap-2"
            >
              <MessageSquare className="h-6 w-6" />
              <span>Send Coach Message</span>
              <span className="text-xs text-muted-foreground">
                ({limits.coach_messages.current}/{limits.coach_messages.limit})
              </span>
            </Button>

            <Button
              onClick={() => handleAction("insight_reports")}
              variant="outline"
              className="h-auto py-4 flex-col gap-2"
            >
              <TrendingUp className="h-6 w-6" />
              <span>Generate Insight</span>
              <span className="text-xs text-muted-foreground">
                ({limits.insight_reports.current}/{limits.insight_reports.limit})
              </span>
            </Button>
          </div>
        </Card>

        {/* Debug Actions */}
        <Card className="p-6 space-y-4 border-dashed">
          <h3 className="font-semibold text-sm text-muted-foreground">Debug Controls</h3>
          <div className="flex gap-2">
            <Button
              onClick={resetUsage}
              variant="outline"
              size="sm"
            >
              Reset Usage
            </Button>
            <Button
              onClick={() => setModalOpen(true)}
              variant="outline"
              size="sm"
            >
              Preview Modal
            </Button>
          </div>
        </Card>
      </div>

      {/* Limit Modal */}
      <LimitModal
        open={modalOpen}
        onOpenChange={setModalOpen}
        limitType={currentLimitType}
        currentUsage={limits[currentLimitType].current}
        limit={limits[currentLimitType].limit}
        onUpgrade={handleUpgrade}
      />
    </DashboardLayout>
  );
}

function UsageCard({
  icon: Icon,
  title,
  current,
  limit,
  color,
}: {
  icon: React.ElementType;
  title: string;
  current: number;
  limit: number;
  color: string;
}) {
  const percentage = (current / limit) * 100;

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <div className={`flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br ${color} text-white`}>
          <Icon className="h-4 w-4" />
        </div>
        <span className="text-sm font-medium">{title}</span>
      </div>
      <div className="space-y-1">
        <div className="flex items-center justify-between text-xs">
          <span className="text-muted-foreground">
            {current} / {limit}
          </span>
          <span className="font-medium">{Math.round(percentage)}%</span>
        </div>
        <div className="h-2 w-full overflow-hidden rounded-full bg-secondary">
          <div
            className={`h-full bg-gradient-to-r ${color}`}
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>
    </div>
  );
}
