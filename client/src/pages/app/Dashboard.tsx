import { DashboardLayout } from "@/layouts/DashboardLayout";
import { JourneyMap } from "@/components/dashboard/JourneyMap";
import { SignalContainer } from "@/components/dashboard/SignalCard";

// Mock data - in production this would come from API/state
const MOCK_MILESTONES = [
  {
    id: "resume-upload",
    status: "completed" as const,
    module: "resume" as const,
    title: "Resume Uploaded",
    description: "Your professional story is ready to shine",
    href: "/app/dashboard",
  },
  {
    id: "coach-intro",
    status: "active" as const,
    module: "coach" as const,
    title: "AI Career Coach",
    description: "Get personalized guidance on interview prep and career strategy",
    href: "/app/coach",
    progressPercentage: 35,
  },
  {
    id: "insights-analysis",
    status: "upcoming" as const,
    module: "insights" as const,
    title: "Career Insights",
    description: "Analyze your skills and discover market opportunities",
    href: "/app/insights",
  },
  {
    id: "pathways-explore",
    status: "upcoming" as const,
    module: "pathways" as const,
    title: "Career Pathways",
    description: "Explore personalized career paths based on your goals",
    href: "/app/pathways",
  },
  {
    id: "signals-advanced",
    status: "locked" as const,
    module: "signals" as const,
    title: "Job Signals",
    description: "Real-time alerts for opportunities matching your profile",
    unlockRequirement: "Complete Career Pathways to unlock",
  },
];

// Mock signals - in production these would come from real-time events
const MOCK_SIGNALS = [
  {
    id: "signal-1",
    type: "job_match" as const,
    title: "New Job Matches",
    description: "3 positions match your updated profile",
    action: {
      label: "View Matches",
      onClick: () => console.log("View job matches"),
    },
  },
];

export default function Dashboard() {
  return (
    <DashboardLayout>
      {/* Floating Signals */}
      <SignalContainer signals={MOCK_SIGNALS} />

      <div className="container px-4 md:px-6 py-8 space-y-12">
        {/* Journey Map */}
        <JourneyMap milestones={MOCK_MILESTONES} />

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="rounded-lg border bg-card p-6 space-y-2">
            <p className="text-sm text-muted-foreground">Applications</p>
            <p className="text-3xl font-bold">12</p>
            <p className="text-xs text-muted-foreground">+3 this week</p>
          </div>
          <div className="rounded-lg border bg-card p-6 space-y-2">
            <p className="text-sm text-muted-foreground">Interviews</p>
            <p className="text-3xl font-bold">4</p>
            <p className="text-xs text-muted-foreground">2 upcoming</p>
          </div>
          <div className="rounded-lg border bg-card p-6 space-y-2">
            <p className="text-sm text-muted-foreground">Success Rate</p>
            <p className="text-3xl font-bold">67%</p>
            <p className="text-xs text-muted-foreground">Above average</p>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="space-y-4">
          <h3 className="text-xl font-bold font-serif">Recent Activity</h3>
          <div className="space-y-3">
            {[
              { action: "Resume tailored for Senior Developer role", time: "2 hours ago" },
              { action: "Completed interview prep session", time: "1 day ago" },
              { action: "Applied to 3 new positions", time: "2 days ago" },
            ].map((activity, index) => (
              <div
                key={index}
                className="flex items-center justify-between rounded-lg border bg-card p-4"
              >
                <p className="text-sm">{activity.action}</p>
                <p className="text-xs text-muted-foreground">{activity.time}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
