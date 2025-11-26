/**
 * Chat API Endpoint
 *
 * POST /api/chat
 * Main orchestrator for Kinto AI assistant
 */

import type { ChatRequest, KintoResponse } from "../types";
import { RAGEngine } from "../services/rag-engine";
import { PIIRedactionService } from "../services/pii-redaction";

// Initialize services
const ragEngine = new RAGEngine();

/**
 * Chat endpoint handler
 */
export async function handleChatRequest(req: any, res: any) {
  try {
    // Validate request
    const validation = validateRequest(req.body);
    if (!validation.valid) {
      return res.status(400).json({
        error: "Invalid request",
        details: validation.errors
      });
    }

    const chatRequest: ChatRequest = req.body;

    // Safety checks
    if (PIIRedactionService.containsPII(chatRequest.message)) {
      console.warn("PII detected in message (will be redacted)");
    }

    // Generate response
    const response: KintoResponse = await ragEngine.generateResponse(chatRequest);

    // Log interaction (for metrics)
    logInteraction(chatRequest, response);

    // Return response
    res.status(200).json(response);

  } catch (error) {
    console.error("Chat API error:", error);
    res.status(500).json({
      error: "Internal server error",
      message: "Something went wrong. Please try again or contact support."
    });
  }
}

/**
 * Validate chat request
 */
function validateRequest(body: any): { valid: boolean; errors?: string[] } {
  const errors: string[] = [];

  if (!body) {
    errors.push("Request body is required");
    return { valid: false, errors };
  }

  if (!body.message || typeof body.message !== 'string') {
    errors.push("message field is required and must be a string");
  }

  if (body.message && body.message.length > 1000) {
    errors.push("message must be less than 1000 characters");
  }

  if (body.message && body.message.trim().length < 3) {
    errors.push("message must be at least 3 characters");
  }

  if (!body.context || typeof body.context !== 'object') {
    errors.push("context field is required and must be an object");
  }

  if (!body.session_id || typeof body.session_id !== 'string') {
    errors.push("session_id field is required and must be a string");
  }

  return {
    valid: errors.length === 0,
    errors: errors.length > 0 ? errors : undefined
  };
}

/**
 * Log interaction for analytics
 */
function logInteraction(request: ChatRequest, response: KintoResponse) {
  // TODO: Implement actual logging to database/analytics service
  const logEntry = {
    timestamp: new Date().toISOString(),
    session_id: request.session_id,
    user_id: request.context.user_id,
    message_length: request.message.length,
    confidence_score: response.confidence_score,
    confidence_label: response.confidence_label,
    retrieved_passages: response.metadata?.retrieved_passages || 0,
    response_time_ms: response.metadata?.response_time_ms || 0,
    escalated: response.ui_actions.talk_to_human,
    page: request.context.page
  };

  console.log("Chat interaction:", JSON.stringify(logEntry));
}

/**
 * Health check endpoint
 */
export function handleHealthCheck(req: any, res: any) {
  res.status(200).json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    service: "Kinto Chat API",
    version: "1.0.0"
  });
}
