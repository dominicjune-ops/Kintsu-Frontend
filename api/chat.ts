/**
 * Vercel Serverless Function: Chat Endpoint
 *
 * Handles POST /api/chat requests
 * Integrates with RAG engine for intelligent responses
 */

import type { VercelRequest, VercelResponse } from '@vercel/node';
import { RAGEngine } from '../server/services/rag-engine';
import { PIIRedactionService } from '../server/services/pii-redaction';
import type { ChatRequest, KintoResponse } from '../server/types';

// Initialize RAG engine (singleton pattern for serverless)
let ragEngine: RAGEngine | null = null;

function getRAGEngine(): RAGEngine {
  if (!ragEngine) {
    ragEngine = new RAGEngine();
  }
  return ragEngine;
}

export default async function handler(
  req: VercelRequest,
  res: VercelResponse
) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  // Handle preflight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({
      error: 'Method not allowed',
      message: 'Only POST requests are accepted'
    });
  }

  try {
    // Validate request body
    const { message, context, session_id } = req.body as ChatRequest;

    if (!message || typeof message !== 'string') {
      return res.status(400).json({
        error: 'Invalid request',
        message: 'Message field is required and must be a string'
      });
    }

    // Build chat request
    const chatRequest: ChatRequest = {
      message,
      context: context || {
        session_id: session_id || `session_${Date.now()}`,
        page: '/',
        user_profile: {
          plan: 'free',
          expertise_level: 'intermediate',
          career_goal: 'promotion'
        }
      },
      session_id: session_id || `session_${Date.now()}`
    };

    // Get RAG engine and generate response
    const engine = getRAGEngine();
    const kintoResponse: KintoResponse = await engine.generateResponse(chatRequest);

    // Log interaction (in production, send to analytics)
    console.log(`Chat request processed: ${message.substring(0, 50)}... | Confidence: ${kintoResponse.confidence_label}`);

    // Return successful response
    return res.status(200).json(kintoResponse);

  } catch (error: any) {
    console.error('Chat API error:', error);

    return res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to process chat request. Please try again.',
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}
