/**
 * Confidence Scoring Service
 *
 * Calculates confidence score for RAG responses
 * Algorithm from requirement #10
 */

import type { ConfidenceFactors, RetrievalResult } from "../types";

export class ConfidenceScorer {
  /**
   * Calculate composite confidence score (0-100)
   *
   * Breakdown:
   * - 40% retrieval match quality
   * - 20% passage coverage
   * - 20% model certainty
   * - 10% recency boost
   * - 10% source trust
   */
  static calculate(factors: ConfidenceFactors): number {
    const score = Math.round(
      0.4 * factors.retrieval_score * 100 +
      0.2 * factors.passage_coverage * 100 +
      0.2 * factors.model_certainty * 100 +
      0.1 * factors.recency_factor * 100 +
      0.1 * factors.source_trust * 100
    );

    return Math.min(100, Math.max(0, score));
  }

  /**
   * Get confidence label from score
   */
  static getLabel(score: number): "High" | "Medium" | "Low" {
    if (score >= 80) return "High";
    if (score >= 50) return "Medium";
    return "Low";
  }

  /**
   * Calculate retrieval score from search results
   */
  static calculateRetrievalScore(results: RetrievalResult[]): number {
    if (results.length === 0) return 0;

    // Average of top 3 results, normalized
    const topScores = results.slice(0, 3).map(r => r.score);
    const average = topScores.reduce((sum, score) => sum + score, 0) / topScores.length;

    return Math.min(1, average);
  }

  /**
   * Calculate passage coverage
   * How many passages support the assertion
   */
  static calculatePassageCoverage(
    retrievedCount: number,
    usedCount: number
  ): number {
    if (retrievedCount === 0) return 0;
    return Math.min(1, usedCount / Math.min(3, retrievedCount));
  }

  /**
   * Calculate recency factor
   * Boost for recently updated articles
   */
  static calculateRecencyFactor(lastUpdated: string): number {
    const articleDate = new Date(lastUpdated);
    const now = new Date();
    const daysSinceUpdate = Math.floor(
      (now.getTime() - articleDate.getTime()) / (1000 * 60 * 60 * 24)
    );

    // Full score if updated in last 30 days, linear decay to 0 at 365 days
    if (daysSinceUpdate <= 30) return 1;
    if (daysSinceUpdate >= 365) return 0;

    return 1 - (daysSinceUpdate - 30) / (365 - 30);
  }

  /**
   * Calculate source trust factor
   * Boost for official/trusted sources
   */
  static calculateSourceTrust(
    articleCategory: string,
    securityClass: "public" | "internal"
  ): number {
    // Official documentation gets highest trust
    const trustedCategories = ["onboarding", "billing", "account"];

    let trust = 0.5; // baseline

    if (trustedCategories.includes(articleCategory)) {
      trust += 0.3;
    }

    if (securityClass === "public") {
      trust += 0.2; // public docs are verified
    }

    return Math.min(1, trust);
  }

  /**
   * Should escalate based on confidence?
   */
  static shouldEscalate(score: number, userExplicitRequest: boolean = false): boolean {
    if (userExplicitRequest) return true;
    return score < 40; // Low confidence threshold
  }

  /**
   * Get escalation reason
   */
  static getEscalationReason(score: number): string {
    if (score < 40) {
      return "Low confidence - unable to find reliable answer in knowledge base";
    }
    return "User explicitly requested human support";
  }
}
