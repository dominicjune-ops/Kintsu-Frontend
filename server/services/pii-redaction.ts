/**
 * PII Redaction Service
 *
 * Redacts personally identifiable information before sending to external LLMs
 * Patterns: emails, phone numbers, SSNs, credit cards
 */

import type { RedactionResult } from "../types";

const PII_PATTERNS = {
  email: {
    regex: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g,
    replacement: "<REDACTED:EMAIL>"
  },
  phone: {
    regex: /\b(?:\+?\d{1,3})?[-.\s]?(?:\(\d{2,4}\)|\d{2,4})[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b/g,
    replacement: "<REDACTED:PHONE>"
  },
  ssn: {
    regex: /\b\d{3}-\d{2}-\d{4}\b/g,
    replacement: "<REDACTED:SSN>"
  },
  creditCard: {
    regex: /\b(?:\d{4}[-\s]?){3}\d{4}\b/g,
    replacement: "<REDACTED:CARD>"
  },
  zipCode: {
    regex: /\b\d{5}(?:-\d{4})?\b/g,
    replacement: "<REDACTED:ZIP>"
  }
};

export class PIIRedactionService {
  /**
   * Redact PII from text
   */
  static redact(text: string, userConsent: boolean = false): RedactionResult {
    if (userConsent) {
      // If user consented, don't redact (for human escalation)
      return {
        redacted_text: text,
        masks: {},
        patterns_found: []
      };
    }

    let redacted = text;
    const masks: Record<string, string> = {};
    const patternsFound: string[] = [];

    // Apply each pattern
    for (const [patternType, config] of Object.entries(PII_PATTERNS)) {
      const matches = text.match(config.regex);

      if (matches && matches.length > 0) {
        patternsFound.push(patternType);

        matches.forEach((match, index) => {
          const token = `${config.replacement}_${index}`;
          masks[match] = token;
          redacted = redacted.replace(match, token);
        });
      }
    }

    return {
      redacted_text: redacted,
      masks,
      patterns_found: patternsFound
    };
  }

  /**
   * Restore redacted text (for authorized access)
   */
  static restore(redactedText: string, masks: Record<string, string>): string {
    let restored = redactedText;

    for (const [original, token] of Object.entries(masks)) {
      restored = restored.replace(new RegExp(token, 'g'), original);
    }

    return restored;
  }

  /**
   * Check if text contains PII
   */
  static containsPII(text: string): boolean {
    return Object.values(PII_PATTERNS).some(pattern =>
      pattern.regex.test(text)
    );
  }

  /**
   * Get summary of PII types found
   */
  static analyzePII(text: string): string[] {
    const found: string[] = [];

    for (const [patternType, config] of Object.entries(PII_PATTERNS)) {
      if (config.regex.test(text)) {
        found.push(patternType);
      }
    }

    return found;
  }
}
