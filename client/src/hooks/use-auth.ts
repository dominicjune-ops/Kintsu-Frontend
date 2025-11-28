/**
 * Authentication hook with Supabase integration and session linking
 */

import { useState, useEffect } from 'react';
import { createClient, SupabaseClient, User, Session } from '@supabase/supabase-js';
import { linkSessionToUser, isSessionLinked } from '../lib/session-linking';

// Supabase configuration
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://your-project.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'your-anon-key';

const supabase: SupabaseClient = createClient(supabaseUrl, supabaseAnonKey);

interface AuthState {
  user: User | null;
  session: Session | null;
  loading: boolean;
  sessionLinked: boolean;
}

/**
 * Authentication hook with real Supabase integration
 */
export function useAuth(): AuthState & {
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  linkCurrentSession: () => Promise<boolean>;
} {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [sessionLinked, setSessionLinked] = useState(false);

  // Check for existing session on mount
  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);

      if (session?.access_token) {
        checkSessionLinkStatus(session.access_token);
      }
    });

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setSession(session);
        setUser(session?.user ?? null);
        setLoading(false);

        if (event === 'SIGNED_IN' && session?.access_token) {
          // Link session after successful sign in
          const linked = await linkSessionToUser(session.access_token);
          setSessionLinked(linked);
        } else if (event === 'SIGNED_OUT') {
          setSessionLinked(false);
        }
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const checkSessionLinkStatus = async (accessToken: string) => {
    const linked = await isSessionLinked(accessToken);
    setSessionLinked(linked);
  };

  const signIn = async (email: string, password: string) => {
    setLoading(true);
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      });

      if (error) throw error;

      // Session linking is handled in the auth state change listener
      console.log('User signed in successfully');
    } catch (error) {
      console.error('Sign in failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signUp = async (email: string, password: string) => {
    setLoading(true);
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password
      });

      if (error) throw error;

      // Note: Email confirmation may be required
      console.log('User signed up successfully. Check email for confirmation.');
    } catch (error) {
      console.error('Sign up failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signOut = async () => {
    try {
      const { error } = await supabase.auth.signOut();
      if (error) throw error;

      setSessionLinked(false);
      console.log('User signed out successfully');
    } catch (error) {
      console.error('Sign out failed:', error);
      throw error;
    }
  };

  const linkCurrentSession = async (): Promise<boolean> => {
    if (!session?.access_token) return false;

    const linked = await linkSessionToUser(session.access_token);
    setSessionLinked(linked);
    return linked;
  };

  return {
    user,
    session,
    loading,
    sessionLinked,
    signIn,
    signUp,
    signOut,
    linkCurrentSession
  };
}