import { useState } from "react";
import { JobCard } from "@/components/JobCard";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search } from "lucide-react";

// TODO: remove mock functionality
const mockJobs = [
  {
    id: "1",
    title: "Senior Product Manager",
    company: "TechVision Inc",
    location: "San Francisco, CA",
    salary: "$140k - $180k",
    type: "Full-time",
    tags: ["Product", "SaaS", "Remote OK"],
    description: "Lead product strategy for our enterprise SaaS platform. Work with engineering and design to ship features that delight customers."
  },
  {
    id: "2",
    title: "Frontend Engineer",
    company: "Startup Labs",
    location: "Remote",
    salary: "$120k - $160k",
    type: "Full-time",
    tags: ["React", "TypeScript", "Remote"],
    description: "Build beautiful, performant user interfaces with React and TypeScript. Join a fast-growing startup building the future of work."
  },
  {
    id: "3",
    title: "Data Scientist",
    company: "Analytics Co",
    location: "New York, NY",
    salary: "$130k - $170k",
    type: "Full-time",
    tags: ["Python", "ML", "Analytics"],
    description: "Apply machine learning to solve complex business problems. Work with large datasets and cutting-edge ML tools."
  },
  {
    id: "4",
    title: "DevOps Engineer",
    company: "CloudScale",
    location: "Austin, TX",
    salary: "$125k - $165k",
    type: "Full-time",
    tags: ["AWS", "Kubernetes", "Remote OK"],
    description: "Build and maintain cloud infrastructure at scale. Automate everything and help teams ship faster."
  },
  {
    id: "5",
    title: "UX Designer",
    company: "DesignFirst",
    location: "Remote",
    salary: "$110k - $145k",
    type: "Full-time",
    tags: ["Figma", "User Research", "Remote"],
    description: "Design delightful experiences for our mobile and web applications. Conduct user research and iterate based on feedback."
  }
];

export default function Jobs() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedTag, setSelectedTag] = useState<string | null>(null);

  const allTags = Array.from(
    new Set(mockJobs.flatMap(job => job.tags))
  );

  const filteredJobs = mockJobs.filter(job => {
    const matchesSearch = searchQuery === "" || 
      job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.location.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesTag = !selectedTag || job.tags.includes(selectedTag);
    
    return matchesSearch && matchesTag;
  });

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
          {filteredJobs.length > 0 ? (
            filteredJobs.map((job) => (
              <JobCard
                key={job.id}
                {...job}
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
