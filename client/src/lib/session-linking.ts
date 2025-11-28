/**
 * Session linking utilities for connecting anonymous chat sessions to authenticated users
 */

const SESSION_KEY = "kinto_session_id";

/**
 * Get the current chat session ID from localStorage
 */
export function getCurrentSessionId(): string | null {
  return localStorage.getItem(SESSION_KEY);
}

/**
 * Link an anonymous chat session to an authenticated user
 * Call this after successful login/signup
 */
export async function linkSessionToUser(accessToken: string): Promise<boolean> {
  const sessionId = getCurrentSessionId();
  if (!sessionId) {
    console.warn("No session ID found to link");
    return false;
  }

  const apiUrl = import.meta.env.VITE_API_URL || "https://api.kintsu.io";

  try {
    const response = await fetch(`${apiUrl}/api/v1/ai/sessions/link`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`
      },
      body: JSON.stringify({ session_id: sessionId })
    });

    if (!response.ok) {
      console.error("Failed to link session:", response.status, response.statusText);
      return false;
    }

    const result = await response.json();
    console.log("Session linked successfully:", result);
    return true;
  } catch (error) {
    console.error("Error linking session:", error);
    return false;
  }
}

/**
 * Clear the current session (useful for logout or session reset)
 */
export function clearSession(): void {
  localStorage.removeItem(SESSION_KEY);
}

/**
 * Check if a session is currently linked to a user
 * This would require a backend endpoint to check session status
 */
export async function isSessionLinked(accessToken?: string): Promise<boolean> {
  const sessionId = getCurrentSessionId();
  if (!sessionId) return false;

  const apiUrl = import.meta.env.VITE_API_URL || "https://api.kintsu.io";

  try {
    const headers: Record<string, string> = {
      "Content-Type": "application/json"
    };

    if (accessToken) {
      headers["Authorization"] = `Bearer ${accessToken}`;
    }

    const response = await fetch(`${apiUrl}/api/v1/ai/sessions/status`, {
      method: "POST",
      headers,
      body: JSON.stringify({ session_id: sessionId })
    });

    if (!response.ok) return false;

    const result = await response.json();
    return result.linked === true;
  } catch (error) {
    console.error("Error checking session status:", error);
    return false;
  }
}