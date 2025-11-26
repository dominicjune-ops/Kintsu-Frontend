/**
 * RAG Engine Service
 *
 * Orchestrates Retrieval Augmented Generation:
 * 1. Retrieve relevant KB passages
 * 2. Construct prompt with context
 * 3. Call LLM (OpenAI/Anthropic)
 * 4. Parse and validate response
 */

import type { KintoResponse, ChatRequest, RetrievalResult, UserContext } from "../types";
import { RetrievalService } from "./retrieval";
import { ConfidenceScorer } from "./confidence-scorer";
import { PIIRedactionService } from "./pii-redaction";

// LLM Configuration
const LLM_CONFIG = {
  provider: process.env.LLM_PROVIDER || "openai", // "openai" or "anthropic"
  model: process.env.LLM_MODEL || "gpt-4o-mini",
  apiKey: process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY,
  maxTokens: 800,
  temperature: 0.3 // Low for factual, consistent responses
};

export class RAGEngine {
  private retrieval: RetrievalService;

  constructor() {
    this.retrieval = new RetrievalService();
  }

  /**
   * Generate Kinto response using RAG
   */
  async generateResponse(request: ChatRequest): Promise<KintoResponse> {
    const startTime = Date.now();

    try {
      // 1. Redact PII from user message
      const redactionResult = PIIRedactionService.redact(request.message);
      const safeMessage = redactionResult.redacted_text;

      // 2. Retrieve relevant passages
      const retrievalResults = await this.retrieval.search(safeMessage, 3);

      // 3. If no results found, escalate
      if (retrievalResults.length === 0) {
        return this.buildLowConfidenceResponse(
          request.message,
          "I don't have specific information about that in my knowledge base. Would you like to speak with our support team?",
          []
        );
      }

      // 4. Construct RAG prompt
      const prompt = this.buildPrompt(safeMessage, retrievalResults, request.context);

      // 5. Call LLM
      const llmResponse = await this.callLLM(prompt);

      // 6. Build structured response
      const response = this.buildResponse(
        llmResponse,
        retrievalResults,
        request.message,
        Date.now() - startTime
      );

      return response;

    } catch (error) {
      console.error("RAG Engine error:", error);
      return this.buildErrorResponse();
    }
  }

  /**
   * Build RAG prompt with retrieved context
   */
  private buildPrompt(query: string, results: RetrievalResult[], context: UserContext): string {
    const passages = results.map((r, i) =>
      `[Source ${i + 1}: ${r.title}]\n${r.passage}`
    ).join('\n\n');

    // Kinto personality primer
    const personality = `You are Kinto, Kintsu's AI Career Companion. Your role is to be:
- Calm and confident (never rushed or uncertain)
- Warm and human (not robotic)
- Intelligent but humble (admit when you don't know)
- Professional yet approachable

Your responses should:
- Be concise (2-4 sentences maximum)
- Use "I" and "you" (conversational, not formal)
- Reference the golden joinery metaphor when relevant
- Focus on actionable next steps
- Never make up information not in the provided sources`;

    // User context
    const userInfo = context.user_profile ? `
User Context:
- Plan: ${context.user_profile.plan}
- Career Goal: ${context.user_profile.career_goal || 'not specified'}
- Expertise: ${context.user_profile.expertise_level || 'not specified'}
` : '';

    // Final prompt
    return `${personality}

${userInfo}

Knowledge Base Context:
${passages}

User Question: "${query}"

Instructions:
1. Answer the user's question using ONLY the information from the Knowledge Base Context above
2. If the context doesn't fully answer the question, acknowledge what you do know and suggest talking to support
3. Keep your response concise and actionable (2-4 sentences)
4. Use a warm, conversational tone
5. If suggesting next steps, make them specific (e.g., "Navigate to Settings → Profile")

Your response:`;
  }

  /**
   * Call LLM API (OpenAI or Anthropic)
   */
  private async callLLM(prompt: string): Promise<string> {
    // For MVP: Return mock response
    // TODO: Implement actual OpenAI/Anthropic API calls

    // Mock response structure
    if (LLM_CONFIG.provider === "openai") {
      return this.mockOpenAICall(prompt);
    } else if (LLM_CONFIG.provider === "anthropic") {
      return this.mockAnthropicCall(prompt);
    }

    throw new Error(`Unsupported LLM provider: ${LLM_CONFIG.provider}`);
  }

  /**
   * Mock OpenAI API call (for development)
   */
  private async mockOpenAICall(prompt: string): Promise<string> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Extract query from prompt
    const queryMatch = prompt.match(/User Question: "(.+)"/);
    const query = queryMatch ? queryMatch[1].toLowerCase() : '';

    // Simple mock responses based on query patterns
    if (query.includes('resume') && query.includes('upload')) {
      return "You can upload your resume in two ways: during onboarding after selecting your goal, or from Settings → Profile → Resume. Simply drag your PDF or DOCX file, and I'll scan it in about 5-10 seconds. Need help with a specific issue?";
    }

    if (query.includes('coach') || query.includes('message')) {
      return "The AI Coach is available at /app/coach or in your Journey Map. Free plan users get 10 messages per month, while Pro users have unlimited access. You can ask me about interview prep, resume optimization, salary negotiation, or career strategy.";
    }

    if (query.includes('career') && (query.includes('goal') || query.includes('path'))) {
      return "During onboarding, you choose between Promotion (advancing in your field), Career Pivot (transitioning to a new role), or Professional Growth (expanding skills). This personalizes your recommendations, job matches, and insights. You can change this anytime in Settings → Career Goals.";
    }

    if (query.includes('salary') || query.includes('pay') || query.includes('compensation')) {
      return "Navigate to Insights → Salary Analysis to see your estimated market value based on 500,000+ job postings. You'll see salary ranges for your current role and target roles, plus geographic variations. The data updates weekly and includes negotiation tips.";
    }

    // Generic fallback
    return "I found some relevant information in our knowledge base, but I'd like to make sure I understand your specific question. Could you provide a bit more detail, or would you prefer to talk with our support team for personalized help?";
  }

  /**
   * Mock Anthropic API call (for development)
   */
  private async mockAnthropicCall(prompt: string): Promise<string> {
    // Same logic as OpenAI for MVP
    return this.mockOpenAICall(prompt);
  }

  /**
   * Build structured KintoResponse
   */
  private buildResponse(
    answerText: string,
    retrievalResults: RetrievalResult[],
    originalMessage: string,
    responseTimeMs: number
  ): KintoResponse {
    // Calculate confidence
    const avgRetrievalScore = retrievalResults.length > 0
      ? retrievalResults.reduce((sum, r) => sum + r.score, 0) / retrievalResults.length / 100
      : 0;

    const confidence = ConfidenceScorer.calculate({
      retrieval_score: avgRetrievalScore,
      passage_coverage: retrievalResults.length > 0 ? 0.8 : 0,
      model_certainty: 0.75, // Mock for now
      recency_factor: 1.0,
      source_trust: 1.0
    });

    const confidenceLabel = ConfidenceScorer.getLabel(confidence);

    // Build provenance
    const provenance = retrievalResults.map(r => ({
      article_id: r.article_id,
      title: r.title,
      link: `/help/${r.article_id}`,
      excerpt: r.passage.substring(0, 150) + (r.passage.length > 150 ? '...' : '')
    }));

    // Determine suggested next steps
    const suggestedNextSteps = this.generateNextSteps(originalMessage, retrievalResults);

    // Determine UI actions
    const showFullArticle = retrievalResults.length > 0 && confidence >= 70;
    const talkToHuman = confidence < 50 || ConfidenceScorer.shouldEscalate(confidence, avgRetrievalScore);

    return {
      answer_text: answerText,
      confidence_score: confidence,
      confidence_label: confidenceLabel,
      provenance,
      suggested_next_steps: suggestedNextSteps,
      ui_actions: {
        show_full_article: showFullArticle,
        talk_to_human: talkToHuman
      },
      metadata: {
        retrieved_passages: retrievalResults.length,
        llm_model: LLM_CONFIG.model,
        response_time_ms: responseTimeMs
      }
    };
  }

  /**
   * Generate suggested next steps
   */
  private generateNextSteps(query: string, results: RetrievalResult[]): string[] {
    const steps: string[] = [];
    const lowerQuery = query.toLowerCase();

    // Pattern-based suggestions
    if (lowerQuery.includes('upload') && lowerQuery.includes('resume')) {
      steps.push("Navigate to /app/onboarding to upload your resume");
      steps.push("Ensure file is PDF, DOC, or DOCX under 10MB");
    } else if (lowerQuery.includes('coach')) {
      steps.push("Go to /app/coach to start a conversation");
      steps.push("Check your message limit at Settings → Usage");
    } else if (lowerQuery.includes('salary') || lowerQuery.includes('pay')) {
      steps.push("View salary insights at Insights → Salary Analysis");
      steps.push("Compare by location and experience level");
    } else if (lowerQuery.includes('upgrade') || lowerQuery.includes('pro')) {
      steps.push("Start your 14-day Pro trial at Settings → Billing");
      steps.push("Get unlimited AI Coach messages and advanced insights");
    } else {
      // Generic next steps based on top result
      if (results.length > 0) {
        steps.push(`Read the full article: ${results[0].title}`);
        if (results.length > 1) {
          steps.push("Explore related topics in the knowledge base");
        }
      }
    }

    return steps.slice(0, 3); // Max 3 suggestions
  }

  /**
   * Build low-confidence response for unknown queries
   */
  private buildLowConfidenceResponse(
    query: string,
    message: string,
    retrievalResults: RetrievalResult[]
  ): KintoResponse {
    return {
      answer_text: message,
      confidence_score: 20,
      confidence_label: "Low",
      provenance: [],
      suggested_next_steps: [
        "Try rephrasing your question with more specific details",
        "Search our help center at help.kintsu.io",
        "Contact support at support@kintsu.io"
      ],
      ui_actions: {
        show_full_article: false,
        talk_to_human: true
      },
      metadata: {
        retrieved_passages: 0,
        llm_model: LLM_CONFIG.model,
        response_time_ms: 0
      }
    };
  }

  /**
   * Build error response
   */
  private buildErrorResponse(): KintoResponse {
    return {
      answer_text: "I'm having trouble processing that right now. This is unusual — let me connect you with our support team who can help immediately.",
      confidence_score: 0,
      confidence_label: "Low",
      provenance: [],
      suggested_next_steps: [
        "Try refreshing the page",
        "Contact support@kintsu.io",
        "Check status.kintsu.io for system status"
      ],
      ui_actions: {
        show_full_article: false,
        talk_to_human: true
      },
      metadata: {
        retrieved_passages: 0,
        llm_model: LLM_CONFIG.model,
        response_time_ms: 0
      }
    };
  }
}
