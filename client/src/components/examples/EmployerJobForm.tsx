import { EmployerJobForm } from '../EmployerJobForm';
import { ThemeProvider } from '../ThemeProvider';

export default function EmployerJobFormExample() {
  return (
    <ThemeProvider>
      <div className="p-8 bg-background max-w-3xl">
        <EmployerJobForm />
      </div>
    </ThemeProvider>
  );
}
