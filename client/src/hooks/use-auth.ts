/**
 * Authentication hook with session linking integration
 * Replace with actual Supabase auth implementation when ready
 */

import { useState, useEffect } from 'react';
import { linkSessionToUser, isSessionLinked } from '../lib/session-linking';

interface User {
  id: string;
  email: string;
  // Add other user properties as needed
}

interface AuthState {
  user: User | null;
  loading: boolean;
  sessionLinked: boolean;
}

/**
 * Example authentication hook
 * Replace this with actual Supabase auth when implemented
 */
export function useAuth(): AuthState & {
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  linkCurrentSession: () => Promise<boolean>;
} {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [sessionLinked, setSessionLinked] = useState(false);

  // Check for existing session on mount
  useEffect(() => {
    checkAuthState();
  }, []);

  const checkAuthState = async () => {
    try {
      // TODO: Replace with actual Supabase auth check
      // const { data: { session } } = await supabase.auth.getSession();

      // For now, check localStorage (replace with real auth)
      const savedUser = localStorage.getItem('kintsu_user');
      if (savedUser) {
        const userData = JSON.parse(savedUser);
        setUser(userData);

        // Check if session is linked
        const linked = await isSessionLinked(userData.accessToken);
        setSessionLinked(linked);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const signIn = async (email: string, password: string) => {
    setLoading(true);
    try {
      // TODO: Replace with actual Supabase sign in
      // const { data, error } = await supabase.auth.signInWithPassword({
      //   email,
      //   password
      // });

      // Mock successful login for now
      const mockUser: User = {
        id: 'user_' + Date.now(),
        email
      };

      const mockToken = 'mock_jwt_token_' + Date.now();

      // Store user data
      localStorage.setItem('kintsu_user', JSON.stringify({
        ...mockUser,
        accessToken: mockToken
      }));

      setUser(mockUser);

      // Link the current chat session to the user
      const linked = await linkSessionToUser(mockToken);
      setSessionLinked(linked);

      console.log('User signed in and session linked:', linked);
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
      // TODO: Replace with actual Supabase sign up
      // const { data, error } = await supabase.auth.signUp({
      //   email,
      //   password
      // });

      // Mock successful signup
      const mockUser: User = {
        id: 'user_' + Date.now(),
        email
      };

      const mockToken = 'mock_jwt_token_' + Date.now();

      localStorage.setItem('kintsu_user', JSON.stringify({
        ...mockUser,
        accessToken: mockToken
      }));

      setUser(mockUser);

      // Link the current chat session to the user
      const linked = await linkSessionToUser(mockToken);
      setSessionLinked(linked);

      console.log('User signed up and session linked:', linked);
    } catch (error) {
      console.error('Sign up failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signOut = async () => {
    try {
      // TODO: Replace with actual Supabase sign out
      // await supabase.auth.signOut();

      localStorage.removeItem('kintsu_user');
      setUser(null);
      setSessionLinked(false);
    } catch (error) {
      console.error('Sign out failed:', error);
      throw error;
    }
  };

  const linkCurrentSession = async (): Promise<boolean> => {
    if (!user) return false;

    const userData = JSON.parse(localStorage.getItem('kintsu_user') || '{}');
    const accessToken = userData.accessToken;

    if (!accessToken) return false;

    const linked = await linkSessionToUser(accessToken);
    setSessionLinked(linked);
    return linked;
  };

  return {
    user,
    loading,
    sessionLinked,
    signIn,
    signUp,
    signOut,
    linkCurrentSession
  };
}