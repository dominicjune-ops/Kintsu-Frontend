import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { useToast } from "@/hooks/use-toast";

const jobPostSchema = z.object({
  companyName: z.string().min(2, "Company name is required"),
  roleTitle: z.string().min(3, "Role title is required"),
  location: z.string().min(2, "Location is required"),
  isRemote: z.boolean(),
  salaryRange: z.string().min(3, "Salary range is required"),
  jobDescription: z.string().min(50, "Job description must be at least 50 characters"),
  contactEmail: z.string().email("Please enter a valid email"),
  companyWebsite: z.string().url("Please enter a valid URL").or(z.literal("")),
  honeypot: z.string().max(0, "Invalid submission")
});

type JobPostFormData = z.infer<typeof jobPostSchema>;

export function EmployerJobForm() {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<JobPostFormData>({
    resolver: zodResolver(jobPostSchema),
    defaultValues: {
      companyName: "",
      roleTitle: "",
      location: "",
      isRemote: false,
      salaryRange: "",
      jobDescription: "",
      contactEmail: "",
      companyWebsite: "",
      honeypot: ""
    }
  });

  const onSubmit = async (data: JobPostFormData) => {
    setIsSubmitting(true);
    
    try {
      // Generate tags from the job description (basic extraction)
      const tags: string[] = [];
      if (data.isRemote) tags.push("Remote");
      tags.push("Full-time"); // Default for now
      
      const response = await fetch("/api/jobs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...data,
          tags,
          type: "Full-time"
        })
      });

      if (!response.ok) {
        throw new Error("Failed to submit job posting");
      }

      toast({
        title: "Job posted successfully!",
        description: "Your job posting is under review. We'll notify you once it's live.",
      });

      form.reset();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to submit job posting. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <div className="hidden">
          <FormField
            control={form.control}
            name="honeypot"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <Input {...field} tabIndex={-1} autoComplete="off" />
                </FormControl>
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="companyName"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Company Name</FormLabel>
              <FormControl>
                <Input placeholder="Acme Corp" {...field} data-testid="input-company-name" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="roleTitle"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Role Title</FormLabel>
              <FormControl>
                <Input placeholder="Senior Software Engineer" {...field} data-testid="input-role-title" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            control={form.control}
            name="location"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Location</FormLabel>
                <FormControl>
                  <Input placeholder="San Francisco, CA" {...field} data-testid="input-location" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="isRemote"
            render={({ field }) => (
              <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
                <div className="space-y-0.5">
                  <FormLabel className="text-base">Remote Position</FormLabel>
                  <FormDescription>Allow remote work</FormDescription>
                </div>
                <FormControl>
                  <Switch
                    checked={field.value}
                    onCheckedChange={field.onChange}
                    data-testid="switch-remote"
                  />
                </FormControl>
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="salaryRange"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Salary Range</FormLabel>
              <FormControl>
                <Input placeholder="$120k - $180k" {...field} data-testid="input-salary" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="jobDescription"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Job Description</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="Describe the role, responsibilities, requirements..."
                  className="min-h-40"
                  {...field}
                  data-testid="input-job-description"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            control={form.control}
            name="contactEmail"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Contact Email</FormLabel>
                <FormControl>
                  <Input type="email" placeholder="hiring@company.com" {...field} data-testid="input-contact-email" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="companyWebsite"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Company Website (Optional)</FormLabel>
                <FormControl>
                  <Input placeholder="https://company.com" {...field} data-testid="input-company-website" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="bg-muted/50 p-4 rounded-md">
          <p className="text-sm text-muted-foreground">
            Note: All job postings are reviewed before going live. You'll receive a notification once approved.
          </p>
        </div>

        <Button type="submit" disabled={isSubmitting} className="w-full" data-testid="button-submit-job">
          {isSubmitting ? "Submitting..." : "Submit Job Posting"}
        </Button>
      </form>
    </Form>
  );
}
