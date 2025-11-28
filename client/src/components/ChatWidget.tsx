import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageCircle, X, Send, Minimize2, ThumbsUp, ThumbsDown, ExternalLink, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { TypingIndicator } from "@/components/ui/typing-indicator";
import { Badge } from "@/components/ui/badge";
import { KintoAvatar, type KintoState } from "@/components/kinto/KintoAvatar";

// Backend API types
interface KintoResponse {
  answer_text: string;
  confidence_score: number;
  confidence_label: "High" | "Medium" | "Low";
  provenance: KBProvenance[];
  suggested_next_steps: string[];
  ui_actions: {
    show_full_article: boolean;
    talk_to_human: boolean;
  };
  metadata?: {
    retrieved_passages: number;
    llm_model: string;
    response_time_ms: number;
  };
}

interface KBProvenance {
  article_id: string;
  title: string;
  link: string;
  excerpt: string;
}

interface ChatMessage {
  id: string;
  content: string;
  sender: "user" | "ai";
  timestamp: Date;
  kintoResponse?: KintoResponse;
  feedback?: "positive" | "negative";
}

export function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      content: "Hi! I'm Kinto, your AI career companion. How can I help you today?",
      sender: "ai",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [kintoState, setKintoState] = useState<KintoState>("idle");
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  // Persistent session ID management
  const getOrCreateSessionId = () => {
    const key = "kinto_session_id";
    let sessionId = localStorage.getItem(key);
    if (!sessionId) {
      sessionId = generateSessionId();
      localStorage.setItem(key, sessionId);
    }
    return sessionId;
  };

  const handleSend = async () => {
    if (!inputValue.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsTyping(true);
    setKintoState("thinking");

    try {
      const apiUrl = import.meta.env.VITE_API_URL || "https://api.kintsu.io";
      // Gather previous messages for context (exclude welcome message)
      const conversationContext = messages
        .filter((msg) => msg.id !== "welcome")
        .map((msg) => ({
          sender: msg.sender,
          content: msg.content,
          timestamp: msg.timestamp,
        }));

      const response = await fetch(`${apiUrl}/api/v1/ai/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: inputValue,
          coaching_type: "general",
          session_id: getOrCreateSessionId(),
          context: {
            user_id: "user_demo",
            page: window.location.pathname,
            user_profile: {
              plan: "free",
              expertise_level: "intermediate",
              career_goal: "promotion",
            },
            conversation: conversationContext,
          },
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response from Kinto");
      }

      const kintoResponse: KintoResponse = await response.json();

      setKintoState("responding");

      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: kintoResponse.answer_text,
        sender: "ai",
        timestamp: new Date(),
        kintoResponse,
      };

      setMessages((prev) => [...prev, aiMessage]);
      setKintoState("success");

      setTimeout(() => setKintoState("idle"), 1000);
    } catch (error) {
      console.error("Chat API error:", error);

      setKintoState("error");

      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: "I'm having trouble connecting right now. Please try again in a moment, or click 'Talk to Human' for immediate assistance.",
        sender: "ai",
        timestamp: new Date(),
        kintoResponse: {
          answer_text: "I'm having trouble connecting right now.",
          confidence_score: 0,
          confidence_label: "Low",
          provenance: [],
          suggested_next_steps: ["Retry your question", "Contact support"],
          ui_actions: {
            show_full_article: false,
            talk_to_human: true,
          },
        },
      };

      setMessages((prev) => [...prev, errorMessage]);

      setTimeout(() => setKintoState("idle"), 2000);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFeedback = (messageId: string, feedback: "positive" | "negative") => {
    setMessages((prev) =>
      prev.map((msg) =>
        msg.id === messageId ? { ...msg, feedback } : msg
      )
    );
    // TODO: Send feedback to backend analytics
    console.log(`Feedback for message ${messageId}:`, feedback);
  };

  const generateSessionId = () => {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  const getConfidenceBadgeColor = (label: "High" | "Medium" | "Low") => {
    switch (label) {
      case "High":
        return "bg-green-100 text-green-800 border-green-300";
      case "Medium":
        return "bg-yellow-100 text-yellow-800 border-yellow-300";
      case "Low":
        return "bg-orange-100 text-orange-800 border-orange-300";
      default:
        return "bg-gray-100 text-gray-800 border-gray-300";
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      <AnimatePresence>
        {!isOpen && (
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            transition={{ type: "spring", stiffness: 260, damping: 20 }}
            style={{ position: "fixed", bottom: "80px", right: "20px", zIndex: 50 }}
          >
            <Button
              size="icon"
              className="h-14 w-14 rounded-full shadow-2xl bg-accent hover:bg-accent/90 text-accent-foreground transition-transform hover:scale-105"
              onClick={() => setIsOpen(true)}
              data-testid="button-chat-widget"
              aria-label="Open chat"
            >
              <MessageCircle className="h-6 w-6" />
            </Button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 100, scale: 0.9 }}
            animate={{
              opacity: 1,
              y: 0,
              scale: 1,
              height: isMinimized ? "60px" : "600px",
            }}
            exit={{ opacity: 0, y: 100, scale: 0.9 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            style={{
              position: "fixed",
              bottom: "80px", // Raised to ensure input is visible
              right: "20px",
              width: "420px",
              maxWidth: "calc(100vw - 40px)",
              zIndex: 50,
            }}
          >
            <Card className="flex flex-col overflow-hidden shadow-2xl">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-accent to-accent/80 text-accent-foreground">
                <div className="flex items-center gap-3">
                  <KintoAvatar state={kintoState} size="sm" />
                  <div>
                    <h3 className="font-semibold text-sm">Kinto</h3>
                    <p className="text-xs opacity-90">Your AI Career Companion</p>
                  </div>
                </div>
                <div className="flex gap-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 hover:bg-white/20 text-accent-foreground"
                    onClick={() => setIsMinimized(!isMinimized)}
                  >
                    <Minimize2 className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 hover:bg-white/20 text-accent-foreground"
                    onClick={() => setIsOpen(false)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              {/* Messages */}
              {!isMinimized && (
                <>
                  <ScrollArea className="flex-1 p-4 h-[460px]" ref={scrollAreaRef}>
                    <div className="space-y-4">
                      {messages.map((message) => (
                        <motion.div
                          key={message.id}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className={`flex ${
                            message.sender === "user" ? "justify-end" : "justify-start"
                          }`}
                        >
                          {message.sender === "user" ? (
                            // User message
                            <div className="flex gap-2 items-start max-w-[85%]">
                              <div className="flex-1">
                                <div className="bg-accent text-accent-foreground rounded-2xl px-4 py-2">
                                  <p className="text-sm">{message.content}</p>
                                  <p className="text-xs opacity-70 mt-1">
                                    {message.timestamp.toLocaleTimeString([], {
                                      hour: "2-digit",
                                      minute: "2-digit",
                                    })}
                                  </p>
                                </div>
                              </div>
                              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center mt-1">
                                <User className="h-3 w-3 text-accent" />
                              </div>
                            </div>
                          ) : (
                            // AI message with full KintoResponse
                            <div className="max-w-[95%] space-y-2">
                              <div className="bg-muted rounded-2xl px-4 py-3">
                                <p className="text-sm leading-relaxed">{message.content}</p>
                                <p className="text-xs opacity-70 mt-2">
                                  {message.timestamp.toLocaleTimeString([], {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                  })}
                                </p>

                                {/* Confidence Badge */}
                                {message.kintoResponse && (
                                  <div className="flex items-center gap-2 mt-3">
                                    <Badge
                                      variant="outline"
                                      className={`text-xs ${getConfidenceBadgeColor(
                                        message.kintoResponse.confidence_label
                                      )}`}
                                    >
                                      {message.kintoResponse.confidence_label} Confidence (
                                      {message.kintoResponse.confidence_score})
                                    </Badge>
                                    {message.kintoResponse.metadata && (
                                      <span className="text-xs text-muted-foreground">
                                        {message.kintoResponse.metadata.response_time_ms}ms
                                      </span>
                                    )}
                                  </div>
                                )}
                              </div>

                              {/* Suggested Next Steps */}
                              {message.kintoResponse &&
                                message.kintoResponse.suggested_next_steps.length > 0 && (
                                  <div className="bg-accent/5 border border-accent/20 rounded-xl px-3 py-2">
                                    <p className="text-xs font-semibold text-accent mb-1.5">
                                      Next Steps:
                                    </p>
                                    <ul className="space-y-1">
                                      {message.kintoResponse.suggested_next_steps.map(
                                        (step, idx) => (
                                          <li key={idx} className="text-xs text-foreground/80 flex items-start gap-1.5">
                                            <span className="text-accent mt-0.5">•</span>
                                            <span>{step}</span>
                                          </li>
                                        )
                                      )}
                                    </ul>
                                  </div>
                                )}

                              {/* Provenance Cards */}
                              {message.kintoResponse &&
                                message.kintoResponse.provenance.length > 0 && (
                                  <div className="space-y-1.5">
                                    <p className="text-xs font-semibold text-muted-foreground px-1">
                                      Sources:
                                    </p>
                                    {message.kintoResponse.provenance.map((prov) => (
                                      <Card
                                        key={prov.article_id}
                                        className="p-2.5 hover:bg-accent/5 transition-colors cursor-pointer border-accent/20"
                                      >
                                        <div className="flex items-start justify-between gap-2">
                                          <div className="flex-1 min-w-0">
                                            <p className="text-xs font-medium text-accent truncate">
                                              {prov.title}
                                            </p>
                                            <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">
                                              {prov.excerpt}
                                            </p>
                                          </div>
                                          <ExternalLink className="h-3 w-3 text-accent flex-shrink-0 mt-0.5" />
                                        </div>
                                      </Card>
                                    ))}
                                  </div>
                                )}

                              {/* UI Actions */}
                              {message.kintoResponse && (
                                <div className="flex gap-2 flex-wrap">
                                  {message.kintoResponse.ui_actions.show_full_article && (
                                    <Button
                                      size="sm"
                                      variant="outline"
                                      className="text-xs h-7 border-accent text-accent hover:bg-accent hover:text-accent-foreground"
                                    >
                                      <ExternalLink className="h-3 w-3 mr-1.5" />
                                      View Full Article
                                    </Button>
                                  )}
                                  {message.kintoResponse.ui_actions.talk_to_human && (
                                    <Button
                                      size="sm"
                                      variant="outline"
                                      className="text-xs h-7 border-orange-400 text-orange-600 hover:bg-orange-50"
                                    >
                                      <User className="h-3 w-3 mr-1.5" />
                                      Talk to Human
                                    </Button>
                                  )}
                                </div>
                              )}

                              {/* Feedback Buttons */}
                              {message.kintoResponse && (
                                <div className="flex items-center gap-2 pt-1">
                                  <span className="text-xs text-muted-foreground">Helpful?</span>
                                  <Button
                                    variant="ghost"
                                    size="icon"
                                    className={`h-6 w-6 ${
                                      message.feedback === "positive"
                                        ? "text-green-600 bg-green-50"
                                        : "text-muted-foreground hover:text-green-600"
                                    }`}
                                    onClick={() => handleFeedback(message.id, "positive")}
                                  >
                                    <ThumbsUp className="h-3 w-3" />
                                  </Button>
                                  <Button
                                    variant="ghost"
                                    size="icon"
                                    className={`h-6 w-6 ${
                                      message.feedback === "negative"
                                        ? "text-red-600 bg-red-50"
                                        : "text-muted-foreground hover:text-red-600"
                                    }`}
                                    onClick={() => handleFeedback(message.id, "negative")}
                                  >
                                    <ThumbsDown className="h-3 w-3" />
                                  </Button>
                                </div>
                              )}
                            </div>
                          )}
                        </motion.div>
                      ))}
                      {isTyping && (
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className="flex justify-start"
                        >
                          <TypingIndicator />
                        </motion.div>
                      )}
                    </div>
                  </ScrollArea>

                  {/* Input */}
                  <div className="p-4 border-t bg-background">
                    <div className="flex gap-2">
                      <Input
                        placeholder="Ask me anything about your career..."
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={handleKeyPress}
                        className="flex-1"
                        disabled={isTyping}
                      />
                      <Button
                        size="icon"
                        onClick={handleSend}
                        disabled={!inputValue.trim() || isTyping}
                        className="bg-accent hover:bg-accent/90 text-accent-foreground"
                      >
                        <Send className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </>
              )}
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
