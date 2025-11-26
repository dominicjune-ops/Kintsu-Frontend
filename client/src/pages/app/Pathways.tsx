import { DashboardLayout } from "@/layouts/DashboardLayout";

export default function Pathways() {
  return (
    <DashboardLayout>
      <div className="container px-4 md:px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-serif mb-2">
            Career Pathways
          </h1>
          <p className="text-muted-foreground">
            Explore paths and opportunities tailored to your goals
          </p>
        </div>

        {/* Placeholder for Pathways Module */}
        <div className="min-h-[500px] rounded-lg border-2 border-dashed border-muted-foreground/25 flex items-center justify-center">
          <p className="text-muted-foreground">Pathways interface will be rendered here</p>
        </div>
      </div>
    </DashboardLayout>
  );
}
