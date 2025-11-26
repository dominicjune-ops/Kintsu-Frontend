import { MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ChatWidget() {
  const handleChatClick = () => {
    // TODO: remove mock functionality
    console.log("Opening chat...");
    window.open("https://app.kintsu/chatbot", "_blank");
  };

  return (
    <Button
      size="icon"
      className="fixed bottom-5 right-5 h-14 w-14 rounded-full shadow-2xl bg-accent hover:bg-accent/90 text-accent-foreground z-50 transition-transform hover:scale-105"
      onClick={handleChatClick}
      data-testid="button-chat-widget"
      aria-label="Open chat"
    >
      <MessageCircle className="h-6 w-6" />
    </Button>
  );
}
