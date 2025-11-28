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
    // Extract user ID from JWT token (simple decode - in production you might want proper JWT parsing)
    const tokenPayload = JSON.parse(atob(accessToken.split('.')[1]));
    const userId = tokenPayload.sub || tokenPayload.user_id;

    if (!userId) {
      console.error("Could not extract user ID from token");
      return false;
    }

    const response = await fetch(`${apiUrl}/api/sessions/link`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`
      },
      body: JSON.stringify({
        sessionId: sessionId,
        userId: userId
      })
    });

    if (!response.ok) {
      console.error("Failed to link session:", response.status, response.statusText);
      return false;
    }

    const result = await response.json();
    console.log("Session linked successfully:", result);

    // Update local session ID to canonical session if it changed
    if (result.canonicalSessionId && result.canonicalSessionId !== sessionId) {
      localStorage.setItem(SESSION_KEY, result.canonicalSessionId);
      console.log("Updated to canonical session:", result.canonicalSessionId);
    }

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

    const response = await fetch(`${apiUrl}/api/sessions/${sessionId}`, {
      method: "GET",
      headers
    });

    if (!response.ok) return false;

    const result = await response.json();
    return result.isLinked === true;
  } catch (error) {
    console.error("Error checking session status:", error);
    return false;
  }
}