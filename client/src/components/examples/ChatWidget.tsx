import { ChatWidget } from '../ChatWidget';
import { ThemeProvider } from '../ThemeProvider';

export default function ChatWidgetExample() {
  return (
    <ThemeProvider>
      <div className="h-96 bg-background relative">
        <ChatWidget />
      </div>
    </ThemeProvider>
  );
}
