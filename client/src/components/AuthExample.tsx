/**
 * Example authentication component demonstrating session linking
 * Replace with actual login/signup UI when implementing Supabase auth
 */

import { useState } from 'react';
import { useAuth } from '../hooks/use-auth';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';

export function AuthExample() {
  const { user, loading, sessionLinked, signIn, signUp, signOut, linkCurrentSession } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (isSignUp) {
        await signUp(email, password);
      } else {
        await signIn(email, password);
      }
      setEmail('');
      setPassword('');
    } catch (error) {
      console.error('Auth error:', error);
      // Handle error (show toast, etc.)
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (user) {
    return (
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle>Welcome, {user.email}!</CardTitle>
          <CardDescription>
            Session Status: <Badge variant={sessionLinked ? "default" : "secondary"}>
              {sessionLinked ? "Linked" : "Not Linked"}
            </Badge>
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {!sessionLinked && (
            <Button onClick={linkCurrentSession} className="w-full">
              Link Current Chat Session
            </Button>
          )}
          <Button onClick={signOut} variant="outline" className="w-full">
            Sign Out
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>{isSignUp ? 'Sign Up' : 'Sign In'}</CardTitle>
        <CardDescription>
          {isSignUp ? 'Create an account' : 'Sign in to your account'}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit" className="w-full">
            {isSignUp ? 'Sign Up' : 'Sign In'}
          </Button>
        </form>
        <div className="mt-4 text-center">
          <Button
            variant="ghost"
            onClick={() => setIsSignUp(!isSignUp)}
          >
            {isSignUp ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}