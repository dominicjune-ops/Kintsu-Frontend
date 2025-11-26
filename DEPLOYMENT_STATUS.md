# Kintsu Deployment Status

## Current Progress: Step 1 → Step 2 In Progress

### ✅ Step 1: Frontend Deployed (COMPLETE)

**Vercel Deployment:**
- Project: `kintsu-frontend`
- Repository: `dominicjune-ops/Kintsu-Frontend`
- Auto-deploy: Enabled (deploys on git push to main)

**Domains Configured:**
- ✅ `kintsu-frontend.vercel.app` - Valid Configuration
- ✅ `app.kintsu.io` - Valid Configuration
- ⚠️ `kintsu.io` - Invalid Configuration (DNS issue - see below)
- 🔄 `www.kintsu.io` - Generating SSL Certificate

**Routes Working:**
- `https://app.kintsu.io/` - Marketing homepage ✅
- `https://app.kintsu.io/app` - Dashboard ✅
- `https://app.kintsu.io/app/onboarding` - Onboarding flow ✅
- `https://app.kintsu.io/app/coach` - Kinto chat UI ✅

---

### 🔄 Step 2: Backend Connection (IN PROGRESS)

**Goal:** Connect frontend to CareerCoach.ai backend via `api.kintsu.io`

**Backend:**
- Service: CareerCoach.ai
- Hosting: Render
- URL: `https://careercoach-ai.onrender.com`
- Status: ✅ Operational

**Architecture:**
```
Frontend (kintsu.io)
    ↓ calls
api.kintsu.io (CNAME)
    ↓ points to
careercoach-ai.onrender.com (Render)
```

**Configuration Status:**

1. **✅ Render Custom Domain**
   - `api.kintsu.io` already configured in Render backend

2. **🔄 Hostinger DNS (PENDING)**
   - Need to add:
     ```
     Type: CNAME
     Name: api
     Target: careercoach-ai.onrender.com
     TTL: 14400
     ```

3. **✅ Frontend Code Updated**
   - ChatWidget.tsx uses `import.meta.env.VITE_API_URL`
   - Fallback: `http://localhost:3001`
   - Committed: 5f3fd23

4. **🔄 Vercel Environment Variable (PENDING)**
   - Need to add in Vercel:
     ```
     Name: VITE_API_URL
     Value: https://api.kintsu.io
     Environment: Production
     ```

5. **❓ Endpoint Path (TO BE DETERMINED)**
   - Frontend calls: `/api/chat`
   - Backend has: `/api/v1/ai/health` (confirmed)
   - Need to confirm: Chat endpoint path
   - Likely: `/api/v1/chat` or `/api/v1/ai/chat`

---

## DNS Issues to Fix

### Issue 1: kintsu.io (Root Domain)

**Problem:** Vercel shows "Invalid Configuration" (307 error)

**Solution Required in Hostinger:**

1. **Remove conflicting AAAA record:**
   ```
   Type: AAAA
   Name: @
   Value: 2600:1901:0:84ef::
   ```
   ☝️ DELETE THIS

2. **Update A record to Vercel's new IP:**
   ```
   Type: A
   Name: @
   Value: 216.198.79.1  (UPDATE from 76.76.21.21)
   TTL: 14400
   ```

### Issue 2: www.kintsu.io (WWW Subdomain)

**Current Status:** Generating SSL Certificate (in progress)

**If CNAME Error Occurs:**
- Check for existing `www` records in Hostinger
- Delete any conflicting A or CNAME records for `www`
- Then add:
  ```
  Type: CNAME
  Name: www
  Target: cname.vercel-dns.com
  TTL: 14400
  ```

---

## Pending Tasks

### Immediate (Step 2 Completion):

1. **Add CNAME in Hostinger**
   - Add `api` CNAME pointing to `careercoach-ai.onrender.com`

2. **Determine Chat Endpoint**
   - Test: `https://careercoach-ai.onrender.com/api/chat`
   - Test: `https://careercoach-ai.onrender.com/api/v1/chat`
   - Test: `https://careercoach-ai.onrender.com/api/v1/ai/chat`
   - Confirm which one works

3. **Update ChatWidget if Needed**
   - If endpoint is not `/api/chat`, update code to correct path

4. **Set Vercel Environment Variable**
   - Add `VITE_API_URL=https://api.kintsu.io` in Vercel

5. **Test End-to-End**
   - Open `https://app.kintsu.io`
   - Click chat widget
   - Send a test message
   - Verify it reaches backend and returns response

### DNS Fixes (Parallel):

1. **Fix kintsu.io root domain**
   - Remove AAAA record
   - Update A record to 216.198.79.1

2. **Verify www.kintsu.io**
   - Wait for SSL certificate generation
   - If errors, check for conflicting records

---

## Testing Checklist

Once all configuration is complete:

- [ ] `https://kintsu.io` loads marketing site
- [ ] `https://www.kintsu.io` redirects to kintsu.io
- [ ] `https://app.kintsu.io` loads dashboard
- [ ] `https://api.kintsu.io` returns backend API response
- [ ] Chat widget opens on all pages
- [ ] Chat widget can send messages
- [ ] Chat widget receives responses from backend
- [ ] All routes work (/, /app, /app/onboarding, /app/coach)
- [ ] SSL certificates valid on all domains

---

## Backend Endpoint Discovery

**Known Endpoints from Backend:**
```
GET  /                          → API info
GET  /docs                      → API documentation
GET  /api/v1/health             → Health check
GET  /api/v1/ai/health          → AI service health
POST /api/v1/resumes            → Resume operations
POST /api/v1/jobs               → Job operations
POST /api/v1/applications       → Application operations
POST /api/v1/??? → Chat endpoint (TO BE DETERMINED)
```

**Need to Find:**
- Chat/conversation endpoint that accepts user messages
- Expected request format
- Response format (should match KintoResponse schema if possible)

---

## Environment Variables

### Development (localhost)
```bash
VITE_API_URL=http://localhost:3001
```

### Production (Vercel)
```bash
VITE_API_URL=https://api.kintsu.io
```

---

## Next Session Resume Point

**If you need to pick up where you left off:**

1. Check if `api` CNAME was added in Hostinger
2. Verify chat endpoint path in backend code
3. Set `VITE_API_URL` in Vercel
4. Test chat functionality end-to-end
5. Fix kintsu.io DNS (remove AAAA, update A record)

**Quick Test Command:**
```bash
# Test backend directly
curl https://careercoach-ai.onrender.com/api/v1/health

# Test via api subdomain (after DNS propagates)
curl https://api.kintsu.io/api/v1/health

# Test from frontend (after env var set)
# Open browser console on https://app.kintsu.io
# Open chat widget and send a message
# Check Network tab for API calls
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Vercel)                     │
│                                                          │
│  kintsu.io          → Marketing site                     │
│  app.kintsu.io      → SaaS Dashboard                     │
│  /app/onboarding    → 3-step wizard                      │
│  /app/coach         → Kinto chat UI                      │
│                                                          │
│  ChatWidget.tsx     → Calls VITE_API_URL/api/chat        │
└─────────────────────────────────────────────────────────┘
                             ↓
                    api.kintsu.io (CNAME)
                             ↓
┌─────────────────────────────────────────────────────────┐
│               Backend (Render - CareerCoach.ai)          │
│                                                          │
│  careercoach-ai.onrender.com                             │
│                                                          │
│  POST /api/v1/chat (?)   → Process chat messages         │
│  GET  /api/v1/ai/health  → AI service status             │
│  GET  /api/v1/health     → Backend health                │
│                                                          │
│  Uses: FastAPI, Anthropic API, OpenAI API                │
└─────────────────────────────────────────────────────────┘
```

---

## Success Criteria

**Step 1 Complete When:**
- ✅ Frontend deployed to Vercel
- ✅ Custom domains configured (kintsu.io, app.kintsu.io)
- ✅ All routes accessible
- ⚠️ DNS fully propagated (pending fixes)

**Step 2 Complete When:**
- [ ] api.kintsu.io DNS configured
- [ ] Chat endpoint identified
- [ ] Environment variable set
- [ ] Chat widget successfully sends/receives messages
- [ ] End-to-end test passes

**Production Ready When:**
- [ ] All DNS issues resolved
- [ ] All domains show "Valid Configuration" in Vercel
- [ ] Chat functionality works on production
- [ ] No CORS errors
- [ ] SSL certificates valid everywhere
