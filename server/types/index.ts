/**
 * Backend Type Definitions
 * Shared types for API, services, and data models
 */

// Kinto Response Schema (matches requirement #8)
export interface KintoResponse {
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

export interface KBProvenance {
  article_id: string;
  title: string;
  link: string;
  excerpt: string;
}

// Chat Request
export interface ChatRequest {
  message: string;
  context: UserContext;
  session_id: string;
}

export interface UserContext {
  user_id?: string;
  page?: string;
  user_agent?: string;
  last_messages?: ChatMessage[];
  user_profile?: UserProfile;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export interface UserProfile {
  plan: "free" | "pro";
  expertise_level?: "beginner" | "intermediate" | "expert";
  career_goal?: "promotion" | "pivot" | "growth";
  tech_stack?: string[];
}

// Knowledge Base Article
export interface KBArticle {
  id: string;
  title: string;
  summary: string;
  canonical_questions: string[];
  answer: string;
  step_by_step?: string[];
  examples?: string[];
  if_not_work?: string[];
  related_articles?: string[];
  tags: string[];
  category: KBCategory;
  last_updated: string;
  author?: string;
  security_class: "public" | "internal";
  locale: string;
  version: number;
  popularity_score?: number;
}

export type KBCategory =
  | "onboarding"
  | "resume"
  | "coach"
  | "insights"
  | "pathways"
  | "billing"
  | "account"
  | "troubleshooting"
  | "integrations";

// RAG Retrieval Result
export interface RetrievalResult {
  passage: string;
  article_id: string;
  title: string;
  score: number;
  metadata: {
    category: KBCategory;
    last_updated: string;
    tags: string[];
  };
}

// Confidence Scoring
export interface ConfidenceFactors {
  retrieval_score: number; // 0-1
  passage_coverage: number; // 0-1
  model_certainty: number; // 0-1
  recency_factor: number; // 0-1
  source_trust: number; // 0-1
}

// Escalation
export interface EscalationTicket {
  ticket_id: string;
  transcript: ChatMessage[];
  user_consent: boolean;
  context: UserContext;
  provenance: KBProvenance[];
  confidence_score: number;
  escalation_reason: string;
  created_at: Date;
}

// Logging
export interface ChatLog {
  session_id: string;
  user_id?: string;
  messages: ChatMessage[];
  kinto_responses: KintoResponse[];
  escalated: boolean;
  satisfaction_rating?: number;
  created_at: Date;
  metadata: {
    user_agent: string;
    page: string;
  };
}

// PII Redaction
export interface RedactionResult {
  redacted_text: string;
  masks: Record<string, string>; // original -> token mapping
  patterns_found: string[]; // types of PII found
}
