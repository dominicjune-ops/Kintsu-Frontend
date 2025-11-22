import { Card } from "@/components/ui/card";
import { Route, useRoute } from "wouter";

function PrivacyPolicy() {
  return (
    <div className="py-20 md:py-32 bg-background">
      <div className="container mx-auto px-4 md:px-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold font-serif mb-6">Privacy Policy</h1>
          <Card className="p-8 prose max-w-none">
            <p className="text-muted-foreground mb-4">Last updated: November 22, 2025</p>
            
            <h2>Introduction</h2>
            <p>
              At Kintsu.io, we take your privacy seriously. This Privacy Policy explains how we collect, use, and protect your personal information.
            </p>

            <h2>Information We Collect</h2>
            <p>We collect information that you provide directly to us, including:</p>
            <ul>
              <li>Account information (name, email, password)</li>
              <li>Resume and career-related information</li>
              <li>Payment information (processed securely through our payment provider)</li>
              <li>Usage data and analytics</li>
            </ul>

            <h2>How We Use Your Information</h2>
            <p>We use your information to:</p>
            <ul>
              <li>Provide and improve our AI-powered career services</li>
              <li>Tailor resumes and provide job recommendations</li>
              <li>Process payments and manage your account</li>
              <li>Send service updates and marketing communications (with your consent)</li>
            </ul>

            <h2>Data Security</h2>
            <p>
              We implement industry-standard security measures including encryption at rest and in transit. Your data is stored securely and we never share it with third parties without your explicit permission.
            </p>

            <h2>Your Rights</h2>
            <p>You have the right to:</p>
            <ul>
              <li>Access and download your personal data</li>
              <li>Request deletion of your account and data</li>
              <li>Opt out of marketing communications</li>
              <li>Request corrections to your information</li>
            </ul>

            <h2>Contact Us</h2>
            <p>
              If you have questions about this Privacy Policy, please contact us at privacy@kintsu.io
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
}

function TermsOfService() {
  return (
    <div className="py-20 md:py-32 bg-background">
      <div className="container mx-auto px-4 md:px-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold font-serif mb-6">Terms of Service</h1>
          <Card className="p-8 prose max-w-none">
            <p className="text-muted-foreground mb-4">Last updated: November 22, 2025</p>
            
            <h2>Acceptance of Terms</h2>
            <p>
              By accessing and using Kintsu.io, you agree to be bound by these Terms of Service and all applicable laws and regulations.
            </p>

            <h2>Service Description</h2>
            <p>
              Kintsu provides AI-powered career tools including resume tailoring, job matching, and interview coaching. Our services are designed to assist but not guarantee employment outcomes.
            </p>

            <h2>User Responsibilities</h2>
            <p>You agree to:</p>
            <ul>
              <li>Provide accurate information</li>
              <li>Maintain the security of your account</li>
              <li>Not misuse or abuse the service</li>
              <li>Comply with all applicable laws</li>
            </ul>

            <h2>Payment Terms</h2>
            <p>
              Paid subscriptions are billed monthly or annually. You may cancel at any time, with access continuing until the end of your billing period.
            </p>

            <h2>Limitation of Liability</h2>
            <p>
              Kintsu.io is provided "as is" without warranties. We are not liable for employment outcomes, decisions made based on our recommendations, or indirect damages.
            </p>

            <h2>Changes to Terms</h2>
            <p>
              We may update these terms from time to time. Continued use of the service constitutes acceptance of modified terms.
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
}

function AccessibilityStatement() {
  return (
    <div className="py-20 md:py-32 bg-background">
      <div className="container mx-auto px-4 md:px-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold font-serif mb-6">Accessibility Statement</h1>
          <Card className="p-8 prose max-w-none">
            <p className="text-muted-foreground mb-4">Last updated: November 22, 2025</p>
            
            <h2>Our Commitment</h2>
            <p>
              Kintsu.io is committed to ensuring digital accessibility for people with disabilities. We continually improve the user experience for everyone and apply relevant accessibility standards.
            </p>

            <h2>Conformance Status</h2>
            <p>
              We aim to conform with WCAG 2.1 Level AA standards. Our website includes:
            </p>
            <ul>
              <li>Keyboard navigation support</li>
              <li>Screen reader compatibility</li>
              <li>High contrast text and UI elements</li>
              <li>Resizable text without loss of functionality</li>
              <li>Clear focus indicators</li>
              <li>Respect for prefers-reduced-motion preferences</li>
            </ul>

            <h2>Feedback</h2>
            <p>
              We welcome feedback on the accessibility of Kintsu.io. If you encounter accessibility barriers, please contact us at accessibility@kintsu.io
            </p>

            <h2>Ongoing Efforts</h2>
            <p>
              We regularly review our website with automated and manual testing to identify and fix accessibility issues. Our team receives ongoing accessibility training.
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default function Legal() {
  const [matchPrivacy] = useRoute("/legal/privacy");
  const [matchTerms] = useRoute("/legal/terms");
  const [matchAccessibility] = useRoute("/legal/accessibility");

  if (matchPrivacy) return <PrivacyPolicy />;
  if (matchTerms) return <TermsOfService />;
  if (matchAccessibility) return <AccessibilityStatement />;

  return null;
}
