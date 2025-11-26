import { DashboardLayout } from "@/layouts/DashboardLayout";

export default function Coach() {
  return (
    <DashboardLayout>
      <div className="container px-4 md:px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-serif mb-2">
            AI Career Coach
          </h1>
          <p className="text-muted-foreground">
            Get personalized guidance on your career journey
          </p>
        </div>

        {/* Placeholder for Coach Module */}
        <div className="min-h-[500px] rounded-lg border-2 border-dashed border-muted-foreground/25 flex items-center justify-center">
          <p className="text-muted-foreground">Coach interface will be rendered here</p>
        </div>
      </div>
    </DashboardLayout>
  );
}
