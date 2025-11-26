import { Switch, Route, useLocation } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ThemeProvider } from "@/components/ThemeProvider";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { ChatWidget } from "@/components/ChatWidget";
import Home from "@/pages/Home";
import Pricing from "@/pages/Pricing";
import Employers from "@/pages/Employers";
import Jobs from "@/pages/Jobs";
import About from "@/pages/About";
import Legal from "@/pages/Legal";
import NotFound from "@/pages/not-found";
import ComponentsConfig from "@/pages/ComponentsConfig";
import ComponentsGallery from "@/pages/ComponentsGallery";
import Dashboard from "@/pages/app/Dashboard";
import Coach from "@/pages/app/Coach";
import Insights from "@/pages/app/Insights";
import Pathways from "@/pages/app/Pathways";
import Onboarding from "@/pages/app/Onboarding";
import DemoLimits from "@/pages/app/DemoLimits";

function Router() {
  return (
    <Switch>
      <Route path="/" component={Home} />
      <Route path="/pricing" component={Pricing} />
      <Route path="/employers" component={Employers} />
      <Route path="/jobs" component={Jobs} />
      <Route path="/about" component={About} />
      <Route path="/legal/:page" component={Legal} />
      <Route path="/components-config" component={ComponentsConfig} />
      <Route path="/components-gallery" component={ComponentsGallery} />
      <Route path="/app/onboarding" component={Onboarding} />
      <Route path="/app/dashboard" component={Dashboard} />
      <Route path="/app/coach" component={Coach} />
      <Route path="/app/insights" component={Insights} />
      <Route path="/app/pathways" component={Pathways} />
      <Route path="/app/demo-limits" component={DemoLimits} />
      <Route component={NotFound} />
    </Switch>
  );
}

function AppContent() {
  const [location] = useLocation();
  const isAppRoute = location.startsWith('/app');

  return (
    <div className="flex flex-col min-h-screen">
      {!isAppRoute && <Header />}
      <main className="flex-1">
        <Router />
      </main>
      {!isAppRoute && <Footer />}
      {!isAppRoute && <ChatWidget />}
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <TooltipProvider>
          <AppContent />
          <Toaster />
        </TooltipProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
