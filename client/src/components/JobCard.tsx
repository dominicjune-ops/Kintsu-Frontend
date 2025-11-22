import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { MapPin, DollarSign, Briefcase } from "lucide-react";

interface JobCardProps {
  title: string;
  company: string;
  location: string;
  salary: string;
  type: string;
  tags: string[];
  description: string;
  onApply?: () => void;
}

export function JobCard({
  title,
  company,
  location,
  salary,
  type,
  tags,
  description,
  onApply
}: JobCardProps) {
  return (
    <Card className="p-6 hover-elevate transition-all duration-200" data-testid="card-job">
      <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-semibold mb-2" data-testid="text-job-title">{title}</h3>
          <p className="text-muted-foreground font-medium mb-3" data-testid="text-job-company">{company}</p>
          
          <div className="flex flex-wrap gap-4 text-sm text-muted-foreground mb-3">
            <div className="flex items-center gap-1">
              <MapPin className="h-4 w-4" />
              <span data-testid="text-job-location">{location}</span>
            </div>
            <div className="flex items-center gap-1">
              <DollarSign className="h-4 w-4" />
              <span data-testid="text-job-salary">{salary}</span>
            </div>
            <div className="flex items-center gap-1">
              <Briefcase className="h-4 w-4" />
              <span data-testid="text-job-type">{type}</span>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 mb-3">
            {tags.map((tag, index) => (
              <Badge key={index} variant="secondary" data-testid={`badge-tag-${index}`}>
                {tag}
              </Badge>
            ))}
          </div>
        </div>

        <Button onClick={onApply} data-testid="button-apply">
          Apply Now
        </Button>
      </div>

      <p className="text-sm text-muted-foreground line-clamp-2" data-testid="text-job-description">
        {description}
      </p>
    </Card>
  );
}
