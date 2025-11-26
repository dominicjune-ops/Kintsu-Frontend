/**
 * Example Test File
 *
 * Demonstrates how to test the Kinto backend services
 * Run with: tsx test-example.ts
 */

import { RAGEngine } from "./services/rag-engine";
import { RetrievalService } from "./services/retrieval";
import { ConfidenceScorer } from "./services/confidence-scorer";
import { PIIRedactionService } from "./services/pii-redaction";
import type { ChatRequest } from "./types";

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m'
};

function log(label: string, value: any, color: string = colors.blue) {
  console.log(`${color}${colors.bright}${label}:${colors.reset}`, value);
}

function section(title: string) {
  console.log(`\n${colors.cyan}${'='.repeat(60)}${colors.reset}`);
  console.log(`${colors.cyan}${colors.bright}${title}${colors.reset}`);
  console.log(`${colors.cyan}${'='.repeat(60)}${colors.reset}\n`);
}

async function testRetrievalService() {
  section("TEST 1: Retrieval Service");

  const retrieval = new RetrievalService();

  const testQueries = [
    "How do I upload my resume?",
    "What are the AI Coach message limits?",
    "Help with salary negotiation",
    "My dashboard won't load"
  ];

  for (const query of testQueries) {
    log("Query", query, colors.yellow);

    const results = await retrieval.search(query, 3);

    log("Results found", results.length, colors.green);

    results.forEach((result, i) => {
      console.log(`\n  ${colors.magenta}[${i + 1}] ${result.title}${colors.reset}`);
      console.log(`      Score: ${result.score.toFixed(2)}`);
      console.log(`      Category: ${result.metadata.category}`);
      console.log(`      Excerpt: ${result.passage.substring(0, 100)}...`);
    });

    console.log();
  }
}

async function testPIIRedaction() {
  section("TEST 2: PII Redaction Service");

  const testMessages = [
    "My email is john.doe@example.com",
    "Call me at 555-123-4567",
    "My SSN is 123-45-6789",
    "No PII in this message!"
  ];

  for (const message of testMessages) {
    log("Original", message, colors.yellow);

    const result = PIIRedactionService.redact(message);

    log("Redacted", result.redacted_text, colors.green);
    log("Patterns found", result.patterns_found, colors.blue);
    console.log();
  }
}

async function testConfidenceScoring() {
  section("TEST 3: Confidence Scoring");

  const scenarios = [
    {
      name: "High confidence",
      factors: {
        retrieval_score: 0.95,
        passage_coverage: 0.90,
        model_certainty: 0.85,
        recency_factor: 1.0,
        source_trust: 1.0
      }
    },
    {
      name: "Medium confidence",
      factors: {
        retrieval_score: 0.65,
        passage_coverage: 0.60,
        model_certainty: 0.70,
        recency_factor: 0.80,
        source_trust: 1.0
      }
    },
    {
      name: "Low confidence",
      factors: {
        retrieval_score: 0.30,
        passage_coverage: 0.40,
        model_certainty: 0.50,
        recency_factor: 0.60,
        source_trust: 1.0
      }
    }
  ];

  for (const scenario of scenarios) {
    log("Scenario", scenario.name, colors.yellow);

    const score = ConfidenceScorer.calculate(scenario.factors);
    const label = ConfidenceScorer.getLabel(score);
    const shouldEscalate = ConfidenceScorer.shouldEscalate(
      score,
      scenario.factors.retrieval_score
    );

    log("Score", `${score}/100`, colors.green);
    log("Label", label, colors.blue);
    log("Escalate?", shouldEscalate ? "Yes" : "No", colors.magenta);
    console.log();
  }
}

async function testRAGEngine() {
  section("TEST 4: Full RAG Engine");

  const ragEngine = new RAGEngine();

  const testRequests: ChatRequest[] = [
    {
      message: "How do I upload my resume?",
      context: {
        session_id: "test_001",
        user_id: "user_123",
        page: "/app/onboarding",
        user_profile: {
          plan: "free",
          expertise_level: "beginner",
          career_goal: "promotion"
        }
      },
      session_id: "test_001"
    },
    {
      message: "What's the difference between Free and Pro?",
      context: {
        session_id: "test_002",
        user_id: "user_456",
        page: "/app/settings",
        user_profile: {
          plan: "free",
          expertise_level: "intermediate",
          career_goal: "pivot"
        }
      },
      session_id: "test_002"
    },
    {
      message: "How do I become a unicorn astronaut CEO?",
      context: {
        session_id: "test_003",
        user_id: "user_789"
      },
      session_id: "test_003"
    }
  ];

  for (const request of testRequests) {
    log("User Query", request.message, colors.yellow);

    const response = await ragEngine.generateResponse(request);

    log("Answer", response.answer_text, colors.green);
    log("Confidence", `${response.confidence_score}/100 (${response.confidence_label})`, colors.blue);
    log("Provenance", `${response.provenance.length} sources`, colors.cyan);

    if (response.provenance.length > 0) {
      console.log(`\n  ${colors.magenta}Sources:${colors.reset}`);
      response.provenance.forEach((prov, i) => {
        console.log(`    [${i + 1}] ${prov.title} (${prov.article_id})`);
      });
    }

    log("Next Steps", response.suggested_next_steps, colors.cyan);
    log("UI Actions", response.ui_actions, colors.magenta);

    if (response.metadata) {
      log("Metadata", {
        passages: response.metadata.retrieved_passages,
        model: response.metadata.llm_model,
        time: `${response.metadata.response_time_ms}ms`
      }, colors.blue);
    }

    console.log();
  }
}

async function runAllTests() {
  console.log(`${colors.bright}${colors.green}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         KINTSU BACKEND - COMPONENT TESTS                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
${colors.reset}`);

  try {
    await testRetrievalService();
    await testPIIRedaction();
    await testConfidenceScoring();
    await testRAGEngine();

    console.log(`${colors.green}${colors.bright}
✅ All tests completed successfully!
${colors.reset}`);

  } catch (error) {
    console.error(`${colors.red}❌ Test failed:${colors.reset}`, error);
    process.exit(1);
  }
}

// Run tests
runAllTests();
