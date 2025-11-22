import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { EmployerJobForm } from "@/components/EmployerJobForm";
import { Users, Target, TrendingUp, Clock } from "lucide-react";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export default function Employers() {
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const benefits = [
    {
      icon: Users,
      title: "Quality Candidates",
      description: "Access pre-screened professionals actively seeking opportunities"
    },
    {
      icon: Target,
      title: "Targeted Reach",
      description: "Connect with candidates whose skills match your requirements"
    },
    {
      icon: TrendingUp,
      title: "Better Conversion",
      description: "Higher application-to-interview rates with quality matches"
    },
    {
      icon: Clock,
      title: "Save Time",
      description: "Streamlined posting and candidate management"
    }
  ];

  return (
    <div>
      <section className="py-20 md:py-32 bg-gradient-to-br from-primary via-primary/95 to-primary/90 text-primary-foreground">
        <div className="container mx-auto px-4 md:px-6">
          <div className="max-w-3xl">
            <h1 className="text-4xl md:text-5xl font-bold font-serif mb-6">
              Hire Quality Talent Faster
            </h1>
            <p className="text-lg md:text-xl mb-8 text-primary-foreground/90">
              Post jobs and connect with professionals who are actively improving their skills and career trajectory with Kintsu.
            </p>
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button
                  size="lg"
                  className="bg-accent hover:bg-accent/90 text-accent-foreground"
                  data-testid="button-post-job-hero"
                >
                  Post a Job
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle>Post a Job</DialogTitle>
                  <DialogDescription>
                    Fill out the form below to submit your job posting. All submissions are reviewed before going live.
                  </DialogDescription>
                </DialogHeader>
                <EmployerJobForm />
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </section>

      <section className="py-20 md:py-32 bg-background">
        <div className="container mx-auto px-4 md:px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold font-serif mb-4">
              Why Post on Kintsu
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Reach motivated professionals who are invested in their growth
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => (
              <Card key={index} className="p-6 text-center hover-elevate transition-all duration-200">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-md bg-accent/10 mb-4">
                  <benefit.icon className="h-6 w-6 text-accent" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{benefit.title}</h3>
                <p className="text-sm text-muted-foreground">{benefit.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 md:py-32 bg-card">
        <div className="container mx-auto px-4 md:px-6">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold font-serif mb-4">
                Simple, Transparent Pricing
              </h2>
              <p className="text-lg text-muted-foreground">
                Pay only for what you need
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              <Card className="p-8">
                <h3 className="text-2xl font-bold mb-2">Single Job Post</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold">$199</span>
                  <span className="text-muted-foreground"> / 30 days</span>
                </div>
                <ul className="space-y-3 mb-6">
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>Active for 30 days</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>Unlimited applicants</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>Featured listing</span>
                  </li>
                </ul>
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                  <DialogTrigger asChild>
                    <Button className="w-full" variant="outline" data-testid="button-post-single">
                      Post a Job
                    </Button>
                  </DialogTrigger>
                </Dialog>
              </Card>

              <Card className="p-8 border-accent border-2 relative">
                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                  <span className="bg-accent text-accent-foreground text-xs font-semibold px-3 py-1 rounded-full">
                    Best Value
                  </span>
                </div>
                <h3 className="text-2xl font-bold mb-2">Monthly Plan</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold">$499</span>
                  <span className="text-muted-foreground"> / month</span>
                </div>
                <ul className="space-y-3 mb-6">
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>3 active job posts</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>Priority placement</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>Dedicated support</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>Analytics dashboard</span>
                  </li>
                </ul>
                <Button className="w-full" data-testid="button-contact-sales">
                  Contact Sales
                </Button>
              </Card>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
