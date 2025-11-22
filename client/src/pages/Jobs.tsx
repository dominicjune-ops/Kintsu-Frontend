import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { JobCard } from "@/components/JobCard";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search } from "lucide-react";
import type { Job } from "@shared/schema";

export default function Jobs() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedTag, setSelectedTag] = useState<string | null>(null);

  const { data: jobs = [], isLoading } = useQuery<Job[]>({
    queryKey: ["/api/jobs"],
  });

  const allTags = useMemo(() => {
    return Array.from(
      new Set(jobs.flatMap(job => job.tags || []))
    );
  }, [jobs]);

  const filteredJobs = useMemo(() => {
    return jobs.filter(job => {
      const matchesSearch = searchQuery === "" || 
        job.roleTitle.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.companyName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.location.toLowerCase().includes(searchQuery.toLowerCase());
      
      const matchesTag = !selectedTag || (job.tags && job.tags.includes(selectedTag));
      
      return matchesSearch && matchesTag;
    });
  }, [jobs, searchQuery, selectedTag]);

  const handleApply = (jobId: string) => {
    console.log(`Applying to job ${jobId}`);
    window.open("https://app.kintsu.io", "_blank");
  };

  return (
    <div className="py-20 md:py-32 bg-background">
      <div className="container mx-auto px-4 md:px-6">
        <div className="mb-12">
          <h1 className="text-4xl md:text-5xl font-bold font-serif mb-4">
            Find Your Next Opportunity
          </h1>
          <p className="text-lg text-muted-foreground mb-8">
            Discover roles from companies looking for talented professionals
          </p>

          <div className="flex flex-col gap-4 mb-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search jobs, companies, or locations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
                data-testid="input-job-search"
              />
            </div>

            <div className="flex flex-wrap gap-2">
              <Badge
                variant={selectedTag === null ? "default" : "outline"}
                className="cursor-pointer hover-elevate active-elevate-2"
                onClick={() => setSelectedTag(null)}
                data-testid="badge-filter-all"
              >
                All Jobs
              </Badge>
              {allTags.map((tag) => (
                <Badge
                  key={tag}
                  variant={selectedTag === tag ? "default" : "outline"}
                  className="cursor-pointer hover-elevate active-elevate-2"
                  onClick={() => setSelectedTag(tag)}
                  data-testid={`badge-filter-${tag.toLowerCase().replace(/\s+/g, '-')}`}
                >
                  {tag}
                </Badge>
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-4">
          {isLoading ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">Loading jobs...</p>
            </div>
          ) : filteredJobs.length > 0 ? (
            filteredJobs.map((job) => (
              <JobCard
                key={job.id}
                title={job.roleTitle}
                company={job.companyName}
                location={job.location}
                salary={job.salaryRange}
                type={job.type}
                tags={job.tags || []}
                description={job.jobDescription}
                onApply={() => handleApply(job.id)}
              />
            ))
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground">No jobs found matching your criteria</p>
            </div>
          )}
        </div>

        <p className="text-sm text-muted-foreground text-center mt-12">
          New jobs are posted daily. <a href="#" className="text-accent hover:underline">Set up job alerts</a> to never miss an opportunity.
        </p>
      </div>
    </div>
  );
}
