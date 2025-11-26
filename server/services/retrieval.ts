/**
 * Retrieval Service
 *
 * Implements hybrid search: BM25 keyword search + semantic similarity
 * For MVP: Simple keyword matching. Future: Vector embeddings
 */

import type { KBArticle, RetrievalResult } from "../types";
import knowledgeBase from "../data/kb/knowledge-base.json";

export class RetrievalService {
  private kb: KBArticle[] = knowledgeBase as KBArticle[];

  /**
   * Search knowledge base using hybrid approach
   */
  async search(query: string, limit: number = 5): Promise<RetrievalResult[]> {
    // Normalize query
    const normalizedQuery = query.toLowerCase().trim();

    // Score each article
    const scored = this.kb.map(article => ({
      article,
      score: this.calculateRelevanceScore(normalizedQuery, article)
    }));

    // Sort by score descending
    scored.sort((a, b) => b.score - a.score);

    // Take top results
    const topResults = scored.slice(0, limit);

    // Convert to RetrievalResult format
    return topResults
      .filter(result => result.score > 0) // Only return matches
      .map(({ article, score }) => ({
        passage: this.extractBestPassage(normalizedQuery, article),
        article_id: article.id,
        title: article.title,
        score,
        metadata: {
          category: article.category,
          last_updated: article.last_updated,
          tags: article.tags
        }
      }));
  }

  /**
   * Calculate relevance score using multiple signals
   */
  private calculateRelevanceScore(query: string, article: KBArticle): number {
    let score = 0;

    // 1. Canonical question matching (highest weight: 40 points)
    const canonicalMatch = this.matchCanonicalQuestions(query, article.canonical_questions);
    score += canonicalMatch * 40;

    // 2. Title matching (30 points)
    const titleMatch = this.fuzzyMatch(query, article.title.toLowerCase());
    score += titleMatch * 30;

    // 3. Summary matching (20 points)
    const summaryMatch = this.fuzzyMatch(query, article.summary.toLowerCase());
    score += summaryMatch * 20;

    // 4. Tag matching (10 points)
    const tagMatch = this.matchTags(query, article.tags);
    score += tagMatch * 10;

    // 5. Popularity boost (max 10 points)
    if (article.popularity_score) {
      score += (article.popularity_score / 100) * 10;
    }

    return Math.min(100, score);
  }

  /**
   * Match query against canonical questions
   */
  private matchCanonicalQuestions(query: string, questions: string[]): number {
    let maxMatch = 0;

    for (const question of questions) {
      const match = this.fuzzyMatch(query, question.toLowerCase());
      maxMatch = Math.max(maxMatch, match);
    }

    return maxMatch;
  }

  /**
   * Fuzzy string matching (returns 0-1 score)
   */
  private fuzzyMatch(query: string, target: string): number {
    // Extract keywords from query (remove common words)
    const stopWords = new Set(['how', 'do', 'i', 'the', 'a', 'an', 'is', 'are', 'can', 'what', 'where', 'when', 'why', 'to', 'my', 'me', 'you', 'your']);
    const queryWords = query.split(/\s+/).filter(w => !stopWords.has(w) && w.length > 2);

    if (queryWords.length === 0) return 0;

    // Count matching words
    let matches = 0;
    for (const word of queryWords) {
      if (target.includes(word)) {
        matches++;
      }
    }

    // Exact phrase match bonus
    if (target.includes(query)) {
      return 1.0;
    }

    // Partial match score
    return matches / queryWords.length;
  }

  /**
   * Match query words against article tags
   */
  private matchTags(query: string, tags: string[]): number {
    const queryWords = query.toLowerCase().split(/\s+/);
    let matches = 0;

    for (const tag of tags) {
      for (const word of queryWords) {
        if (tag.toLowerCase().includes(word) || word.includes(tag.toLowerCase())) {
          matches++;
          break;
        }
      }
    }

    return matches > 0 ? matches / tags.length : 0;
  }

  /**
   * Extract most relevant passage from article
   */
  private extractBestPassage(query: string, article: KBArticle): string {
    // Check canonical questions first
    for (const question of article.canonical_questions) {
      if (this.fuzzyMatch(query, question.toLowerCase()) > 0.7) {
        // Return answer as most relevant passage
        return article.answer;
      }
    }

    // Check if query mentions "step" or "how to" - return step_by_step
    if ((query.includes('step') || query.includes('how')) && article.step_by_step) {
      return article.step_by_step.join('\n');
    }

    // Check if query mentions "example" - return examples
    if (query.includes('example') && article.examples) {
      return article.examples.join('\n');
    }

    // Check if query mentions "not work" or "problem" - return troubleshooting
    if ((query.includes('not work') || query.includes('problem') || query.includes('error')) && article.if_not_work) {
      return article.if_not_work.join('\n');
    }

    // Default: return answer
    return article.answer;
  }

  /**
   * Get article by ID
   */
  getArticleById(id: string): KBArticle | undefined {
    return this.kb.find(article => article.id === id);
  }

  /**
   * Get articles by category
   */
  getArticlesByCategory(category: string): KBArticle[] {
    return this.kb.filter(article => article.category === category);
  }

  /**
   * Get related articles
   */
  getRelatedArticles(articleId: string): KBArticle[] {
    const article = this.getArticleById(articleId);
    if (!article || !article.related_articles) return [];

    return article.related_articles
      .map(id => this.getArticleById(id))
      .filter(a => a !== undefined) as KBArticle[];
  }
}
