import { MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ChatWidget() {
  const handleChatClick = () => {
    // TODO: remove mock functionality
    console.log("Opening chat...");
    window.open("https://app.kintsu.io/chatbot", "_blank");
  };

  return (
    <Button
      size="icon"
      className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg bg-accent hover:bg-accent/90 text-accent-foreground z-40"
      onClick={handleChatClick}
      data-testid="button-chat-widget"
      aria-label="Open chat"
    >
      <MessageCircle className="h-6 w-6" />
    </Button>
  );
}
