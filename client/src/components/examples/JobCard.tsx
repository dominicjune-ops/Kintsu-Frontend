import { JobCard } from '../JobCard';
import { ThemeProvider } from '../ThemeProvider';

export default function JobCardExample() {
  return (
    <ThemeProvider>
      <div className="p-8 bg-background">
        <JobCard
          title="Senior Software Engineer"
          company="TechCorp Inc"
          location="San Francisco, CA"
          salary="$140k - $180k"
          type="Full-time"
          tags={["React", "TypeScript", "Node.js"]}
          description="We're looking for an experienced Senior Software Engineer to join our growing team. You'll work on cutting-edge web applications and help shape our technical direction."
          onApply={() => console.log('Apply clicked')}
        />
      </div>
    </ThemeProvider>
  );
}
