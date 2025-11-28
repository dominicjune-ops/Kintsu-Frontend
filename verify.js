#!/usr/bin/env node

/**
 * Kintsu Chatbot Platform - Verification Script
 *
 * This script verifies the 6 key scenarios for the chatbot platform:
 * 1. Anonymous chat works
 * 2. User registration works
 * 3. User login works
 * 4. Session linking works
 * 5. Authenticated chat works
 * 6. Database verification
 */

const https = require('https');
const { createClient } = require('@supabase/supabase-js');

// Configuration - Update these with your actual values
const SUPABASE_URL = process.env.VITE_SUPABASE_URL || 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = process.env.VITE_SUPABASE_ANON_KEY || 'your-anon-key';
const BACKEND_URL = process.env.BACKEND_URL || 'https://your-backend.vercel.app';

// Test user credentials
const TEST_EMAIL = 'test@example.com';
const TEST_PASSWORD = 'testpassword123';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function makeRequest(endpoint, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const url = `${BACKEND_URL}${endpoint}`;
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const req = https.request(url, options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(body);
          resolve({ status: res.statusCode, data: response });
        } catch (e) {
          resolve({ status: res.statusCode, data: body });
        }
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(JSON.stringify(data));
    }

    req.end();
  });
}

async function testAnonymousChat() {
  console.log('\n1. Testing Anonymous Chat...');
  try {
    const response = await makeRequest('/api/chat', 'POST', {
      message: 'Hello, I need career advice',
      sessionId: 'test-session-' + Date.now()
    });

    if (response.status === 200 && response.data.response) {
      console.log('✅ Anonymous chat works');
      return true;
    } else {
      console.log('❌ Anonymous chat failed:', response);
      return false;
    }
  } catch (error) {
    console.log('❌ Anonymous chat error:', error.message);
    return false;
  }
}

async function testUserRegistration() {
  console.log('\n2. Testing User Registration...');
  try {
    const { data, error } = await supabase.auth.signUp({
      email: TEST_EMAIL,
      password: TEST_PASSWORD
    });

    if (error) {
      console.log('❌ Registration failed:', error.message);
      return false;
    }

    console.log('✅ User registration works');
    return true;
  } catch (error) {
    console.log('❌ Registration error:', error.message);
    return false;
  }
}

async function testUserLogin() {
  console.log('\n3. Testing User Login...');
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email: TEST_EMAIL,
      password: TEST_PASSWORD
    });

    if (error) {
      console.log('❌ Login failed:', error.message);
      return false;
    }

    console.log('✅ User login works');
    return data.session;
  } catch (error) {
    console.log('❌ Login error:', error.message);
    return false;
  }
}

async function testSessionLinking(session) {
  console.log('\n4. Testing Session Linking...');
  try {
    // First create an anonymous session
    const anonResponse = await makeRequest('/api/chat', 'POST', {
      message: 'Test message for linking',
      sessionId: 'link-test-' + Date.now()
    });

    if (anonResponse.status !== 200) {
      console.log('❌ Could not create anonymous session');
      return false;
    }

    // Link the session to the user
    const linkResponse = await makeRequest('/api/link-session', 'POST', {
      sessionId: anonResponse.data.sessionId,
      accessToken: session.access_token
    });

    if (linkResponse.status === 200 && linkResponse.data.success) {
      console.log('✅ Session linking works');
      return true;
    } else {
      console.log('❌ Session linking failed:', linkResponse);
      return false;
    }
  } catch (error) {
    console.log('❌ Session linking error:', error.message);
    return false;
  }
}

async function testAuthenticatedChat(session) {
  console.log('\n5. Testing Authenticated Chat...');
  try {
    const response = await makeRequest('/api/chat', 'POST', {
      message: 'Authenticated career advice request',
      sessionId: 'auth-test-' + Date.now(),
      accessToken: session.access_token
    });

    if (response.status === 200 && response.data.response) {
      console.log('✅ Authenticated chat works');
      return true;
    } else {
      console.log('❌ Authenticated chat failed:', response);
      return false;
    }
  } catch (error) {
    console.log('❌ Authenticated chat error:', error.message);
    return false;
  }
}

async function testDatabaseVerification() {
  console.log('\n6. Testing Database Verification...');
  try {
    // Test database connection by checking if we can query users
    const { data, error } = await supabase
      .from('users')
      .select('count')
      .limit(1);

    if (error) {
      console.log('❌ Database verification failed:', error.message);
      return false;
    }

    console.log('✅ Database verification works');
    return true;
  } catch (error) {
    console.log('❌ Database verification error:', error.message);
    return false;
  }
}

async function cleanup() {
  console.log('\n🧹 Cleaning up test data...');
  try {
    // Sign out
    await supabase.auth.signOut();
    console.log('✅ Cleanup completed');
  } catch (error) {
    console.log('❌ Cleanup error:', error.message);
  }
}

async function runVerification() {
  console.log('🚀 Starting Kintsu Chatbot Platform Verification');
  console.log('='.repeat(50));

  const results = [];

  // Test 1: Anonymous chat
  results.push(await testAnonymousChat());

  // Test 2: User registration
  results.push(await testUserRegistration());

  // Test 3: User login
  const session = await testUserLogin();
  results.push(!!session);

  if (session) {
    // Test 4: Session linking
    results.push(await testSessionLinking(session));

    // Test 5: Authenticated chat
    results.push(await testAuthenticatedChat(session));
  } else {
    results.push(false, false);
  }

  // Test 6: Database verification
  results.push(await testDatabaseVerification());

  // Cleanup
  await cleanup();

  // Summary
  console.log('\n' + '='.repeat(50));
  console.log('📊 VERIFICATION SUMMARY');
  console.log('='.repeat(50));

  const tests = [
    'Anonymous chat works',
    'User registration works',
    'User login works',
    'Session linking works',
    'Authenticated chat works',
    'Database verification works'
  ];

  let passed = 0;
  tests.forEach((test, index) => {
    const status = results[index] ? '✅ PASS' : '❌ FAIL';
    console.log(`${status}: ${test}`);
    if (results[index]) passed++;
  });

  console.log(`\n🎯 Overall: ${passed}/${tests.length} tests passed`);

  if (passed === tests.length) {
    console.log('🎉 All verification tests passed! The platform is ready.');
  } else {
    console.log('⚠️  Some tests failed. Please check the configuration and try again.');
  }

  process.exit(passed === tests.length ? 0 : 1);
}

// Run the verification
runVerification().catch(console.error);