import { useState } from "react";
import { Link, useLocation } from "wouter";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "./ThemeToggle";
import { Menu, X } from "lucide-react";

export function Header() {
  const [location] = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { href: "/", label: "Home" },
    { href: "/pricing", label: "Pricing" },
    { href: "/employers", label: "For Employers" },
    { href: "/jobs", label: "Jobs" },
    { href: "/about", label: "About" },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 md:px-6">
        <Link href="/">
          <div className="flex items-center gap-2 hover-elevate active-elevate-2 rounded-md px-2 py-1 cursor-pointer" data-testid="link-home">
            <div className="text-2xl font-bold font-serif bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Kintsu.io
            </div>
          </div>
        </Link>

        <nav className="hidden md:flex items-center gap-1">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href}>
              <div
                data-testid={`link-${item.label.toLowerCase().replace(/\s+/g, '-')}`}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors hover-elevate active-elevate-2 cursor-pointer ${
                  location === item.href
                    ? "bg-accent/10 text-accent-foreground"
                    : "text-muted-foreground"
                }`}
              >
                {item.label}
              </div>
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Button
            asChild
            variant="default"
            className="hidden md:inline-flex"
            data-testid="button-start-trial"
          >
            <a href="https://app.kintsu.io">Start Free Trial</a>
          </Button>
          
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            data-testid="button-mobile-menu"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className="md:hidden border-t bg-background">
          <nav className="container mx-auto flex flex-col p-4 gap-2">
            {navItems.map((item) => (
              <Link key={item.href} href={item.href}>
                <div
                  onClick={() => setMobileMenuOpen(false)}
                  data-testid={`link-mobile-${item.label.toLowerCase().replace(/\s+/g, '-')}`}
                  className={`block px-4 py-3 rounded-md text-sm font-medium hover-elevate active-elevate-2 cursor-pointer ${
                    location === item.href
                      ? "bg-accent/10 text-accent-foreground"
                      : "text-muted-foreground"
                  }`}
                >
                  {item.label}
                </div>
              </Link>
            ))}
            <Button
              asChild
              variant="default"
              className="mt-2"
              data-testid="button-mobile-start-trial"
            >
              <a href="https://app.kintsu.io">Start Free Trial</a>
            </Button>
          </nav>
        </div>
      )}
    </header>
  );
}
