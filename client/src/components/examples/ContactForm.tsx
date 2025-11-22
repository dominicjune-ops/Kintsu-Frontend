import { ContactForm } from '../ContactForm';
import { ThemeProvider } from '../ThemeProvider';

export default function ContactFormExample() {
  return (
    <ThemeProvider>
      <div className="p-8 bg-background max-w-2xl">
        <ContactForm />
      </div>
    </ThemeProvider>
  );
}
