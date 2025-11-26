# Kintsu Backend - Kinto AI Assistant API

Complete backend implementation for the Kinto AI Career Companion.

## Architecture

```
server/
├── api/
│   └── chat.ts              # Main chat endpoint orchestrator
├── services/
│   ├── rag-engine.ts        # RAG orchestration + LLM integration
│   ├── retrieval.ts         # Hybrid search (BM25 + semantic)
│   ├── confidence-scorer.ts # Confidence scoring algorithm
│   └── pii-redaction.ts     # PII detection and redaction
├── data/
│   └── kb/
│       └── knowledge-base.json  # 40 KB articles
├── types/
│   └── index.ts             # TypeScript interfaces
└── index.ts                 # Express server
```

## Features Implemented

✅ **RAG Engine**
- Retrieval Augmented Generation
- Context-aware prompt construction
- Kinto personality integration
- Mock LLM responses (OpenAI/Anthropic ready)

✅ **Hybrid Search**
- Canonical question matching (40% weight)
- Title fuzzy matching (30% weight)
- Summary matching (20% weight)
- Tag matching (10% weight)
- Popularity boost

✅ **Confidence Scoring**
- 5-factor weighted algorithm:
  - Retrieval score (40%)
  - Passage coverage (20%)
  - Model certainty (20%)
  - Recency (10%)
  - Source trust (10%)
- Auto-escalation at <50% confidence

✅ **PII Protection**
- Email, phone, SSN, credit card detection
- Regex-based pattern matching
- Restore capability for authorized access
- User consent handling

✅ **Knowledge Base**
- 40 comprehensive articles
- 9 categories (onboarding, resume, coach, etc.)
- Canonical questions for semantic matching
- Related articles linking

## API Endpoints

### POST /api/chat

Main chat endpoint for Kinto interactions.

**Request:**
```json
{
  "message": "How do I upload my resume?",
  "context": {
    "user_id": "user_123",
    "session_id": "session_456",
    "page": "/app/dashboard",
    "user_profile": {
      "plan": "free",
      "expertise_level": "intermediate",
      "career_goal": "promotion"
    }
  }
}
```

**Response:**
```json
{
  "answer_text": "You can upload your resume in two ways...",
  "confidence_score": 85,
  "confidence_label": "High",
  "provenance": [
    {
      "article_id": "kb-001",
      "title": "How to Upload Your Resume",
      "link": "/help/kb-001",
      "excerpt": "Upload your resume via drag & drop..."
    }
  ],
  "suggested_next_steps": [
    "Navigate to /app/onboarding to upload your resume",
    "Ensure file is PDF, DOC, or DOCX under 10MB"
  ],
  "ui_actions": {
    "show_full_article": true,
    "talk_to_human": false
  },
  "metadata": {
    "retrieved_passages": 3,
    "llm_model": "gpt-4o-mini",
    "response_time_ms": 524
  }
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-25T10:30:00.000Z",
  "service": "Kinto Chat API",
  "version": "1.0.0"
}
```

## Installation

```bash
cd server
npm install
```

## Development

```bash
# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test
```

## Environment Variables

Create a `.env` file:

```bash
# Server
PORT=3001
NODE_ENV=development
FRONTEND_URL=http://localhost:5173

# LLM Configuration
LLM_PROVIDER=openai  # or "anthropic"
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## RAG Prompt Engineering

The RAG engine constructs prompts with:

1. **Kinto Personality Primer**
   - Calm, warm, intelligent, professional
   - Conversational tone (not robotic)
   - Humble intelligence (admits unknowns)

2. **User Context**
   - Plan type (free/pro)
   - Career goal (promotion/pivot/growth)
   - Expertise level

3. **Retrieved Knowledge**
   - Top 3 relevant passages
   - Source attribution

4. **Instructions**
   - Answer only from provided context
   - Concise responses (2-4 sentences)
   - Specific next steps
   - Warm, actionable tone

**Example Prompt:**
```
You are Kinto, Kintsu's AI Career Companion. Your role is to be:
- Calm and confident (never rushed or uncertain)
- Warm and human (not robotic)
- Intelligent but humble (admit when you don't know)
- Professional yet approachable

User Context:
- Plan: free
- Career Goal: promotion
- Expertise: intermediate

Knowledge Base Context:
[Source 1: How to Upload Your Resume]
You can upload your resume in two ways: 1) During the onboarding flow...

User Question: "How do I upload my resume?"

Instructions:
1. Answer using ONLY the Knowledge Base Context
2. Keep response concise (2-4 sentences)
3. Use warm, conversational tone
4. Provide specific next steps

Your response:
```

## Retrieval Algorithm

### Scoring Breakdown

1. **Canonical Question Matching (40 points)**
   - Fuzzy match against pre-defined questions
   - Highest weight for direct intent matching

2. **Title Matching (30 points)**
   - Keyword overlap with article title
   - Stop word filtering

3. **Summary Matching (20 points)**
   - Relevance to article summary
   - Context capture

4. **Tag Matching (10 points)**
   - Category and topic alignment

5. **Popularity Boost (max 10 points)**
   - Articles with higher engagement get slight boost
   - Prevents obscure articles from ranking too high

### Passage Extraction

Smart passage selection based on query intent:
- "how to" → step_by_step
- "example" → examples
- "not work"/"error" → if_not_work
- Default → answer

## Confidence Scoring

### Factors

```typescript
{
  retrieval_score: 0.85,      // How well passages match query
  passage_coverage: 0.80,     // How much of query is covered
  model_certainty: 0.75,      // LLM confidence (from logprobs)
  recency_factor: 1.0,        // Article freshness (0-1)
  source_trust: 1.0           // KB article vs external (0-1)
}
```

### Weighted Formula

```
score = (
  0.40 * retrieval_score +
  0.20 * passage_coverage +
  0.20 * model_certainty +
  0.10 * recency_factor +
  0.10 * source_trust
) * 100
```

### Labels

- **High** (≥80): Very confident, show answer
- **Medium** (50-79): Moderately confident, offer alternatives
- **Low** (<50): Escalate to human

### Auto-Escalation

Trigger "Talk to Human" if:
- Confidence < 50
- Retrieval score < 0.3
- No passages found
- PII detected and not consented

## Testing

### Manual Testing

```bash
# Start server
npm run dev

# Test chat endpoint
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I upload my resume?",
    "context": {
      "session_id": "test_123",
      "user_id": "user_456"
    }
  }'
```

### Expected Output

```json
{
  "answer_text": "You can upload your resume in two ways: during onboarding...",
  "confidence_score": 87,
  "confidence_label": "High",
  "provenance": [...],
  "suggested_next_steps": [...],
  "ui_actions": {
    "show_full_article": true,
    "talk_to_human": false
  }
}
```

## LLM Integration (TODO)

Currently uses mock responses. To integrate real LLM:

### OpenAI

```typescript
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

const completion = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [
    { role: "system", content: personality },
    { role: "user", content: prompt }
  ],
  temperature: 0.3,
  max_tokens: 800
});

return completion.choices[0].message.content;
```

### Anthropic

```typescript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const message = await anthropic.messages.create({
  model: "claude-3-5-sonnet-20241022",
  max_tokens: 800,
  temperature: 0.3,
  messages: [
    { role: "user", content: prompt }
  ]
});

return message.content[0].text;
```

## Roadmap

### Phase 1 (MVP) ✅
- [x] RAG engine structure
- [x] Hybrid search
- [x] 40 KB articles
- [x] Confidence scoring
- [x] PII redaction
- [x] Mock LLM responses

### Phase 2 (Production)
- [ ] Real LLM integration (OpenAI/Anthropic)
- [ ] Vector embeddings (Pinecone/Supabase)
- [ ] Conversation history tracking
- [ ] User feedback loop (thumbs up/down)
- [ ] A/B testing framework

### Phase 3 (Scale)
- [ ] Response caching (Redis)
- [ ] Rate limiting per user plan
- [ ] Analytics dashboard
- [ ] Auto-escalation queue (Zendesk/Intercom)
- [ ] Multi-language support

### Phase 4 (Advanced)
- [ ] Fine-tuned model on Kintsu data
- [ ] Proactive suggestions (predictive triggers)
- [ ] Multi-turn conversation optimization
- [ ] Voice interface support

## Performance Targets

- **Response time**: <1s (p95)
- **Accuracy**: 85%+ (measured by user feedback)
- **Deflection rate**: 70%+ (queries resolved without human)
- **Confidence calibration**: ±10% (predicted vs actual)

## Security

- ✅ PII redaction before LLM
- ✅ Input validation (max 1000 chars)
- ✅ Rate limiting ready (TODO: implement)
- ✅ CORS configuration
- ✅ Error handling (no stack traces in prod)
- ✅ User consent for escalation

## Monitoring

Logged metrics:
- Request volume
- Response time
- Confidence distribution
- Escalation rate
- PII detection frequency
- Popular queries
- Low-confidence patterns

## License

Proprietary - Kintsu.io
