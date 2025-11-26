import { Link } from "wouter";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

export function Footer() {
  const [email, setEmail] = useState("");
  const { toast } = useToast();

  const handleNewsletterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const response = await fetch("/api/newsletter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Failed to subscribe");
      }

      toast({
        title: "Thanks for subscribing!",
        description: "You'll receive updates about Kintsu in your inbox.",
      });
      setEmail("");
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to subscribe. Please try again.",
        variant: "destructive"
      });
    }
  };

  return (
    <footer className="border-t bg-card">
      <div className="container mx-auto px-4 md:px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="space-y-4">
            <div className="text-2xl font-bold font-serif bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Kintsu
            </div>
            <p className="text-sm text-muted-foreground">
              Transform your career setbacks into golden opportunities.
            </p>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Product</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/pricing">
                  <a className="text-muted-foreground hover:text-accent transition-colors" data-testid="link-footer-pricing">
                    Pricing
                  </a>
                </Link>
              </li>
              <li>
                <a href="https://app.kintsu.io" className="text-muted-foreground hover:text-accent transition-colors" data-testid="link-footer-app">
                  Web App
                </a>
              </li>
              <li>
                <a href="#features" className="text-muted-foreground hover:text-accent transition-colors" data-testid="link-footer-features">
                  Features
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Company</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/about">
                  <a className="text-muted-foreground hover:text-accent transition-colors" data-testid="link-footer-about">
                    About
                  </a>
                </Link>
              </li>
              <li>
                <Link href="/jobs">
                  <a className="text-muted-foreground hover:text-accent transition-colors" data-testid="link-footer-jobs">
                    Jobs
                  </a>
                </Link>
              </li>
              <li>
                <Link href="/employers">
                  <a className="text-muted-foreground hover:text-accent transition-colors" data-testid="link-footer-employers">
                    For Employers
                  </a>
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Newsletter</h3>
            <form onSubmit={handleNewsletterSubmit} className="space-y-2">
              <Input
                type="email"
                placeholder="Your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                data-testid="input-newsletter-email"
              />
              <Button type="submit" className="w-full" data-testid="button-newsletter-submit">
                Subscribe
              </Button>
            </form>
          </div>
        </div>

        <div className="border-t pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-muted-foreground">
          <p>&copy; 2025 Kintsu. All rights reserved.</p>
          <div className="flex gap-6">
            <Link href="/legal/privacy">
              <a className="hover:text-accent transition-colors" data-testid="link-footer-privacy">
                Privacy Policy
              </a>
            </Link>
            <Link href="/legal/terms">
              <a className="hover:text-accent transition-colors" data-testid="link-footer-terms">
                Terms of Service
              </a>
            </Link>
            <Link href="/legal/accessibility">
              <a className="hover:text-accent transition-colors" data-testid="link-footer-accessibility">
                Accessibility
              </a>
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
