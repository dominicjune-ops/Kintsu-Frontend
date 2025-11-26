# 🚀 Deploy Kintsu Chat Server to Render

## Problem Identified

The chat widget is failing because:
- ❌ Vercel serverless functions were crashing (dependencies too heavy)
- ❌ Python backend at `api.kintsu.io` doesn't have `/api/chat` endpoint
- ✅ This repo has a complete Node.js chat server in `/server` directory

## Solution: Deploy `/server` to Render

Deploy the TypeScript/Node.js chat backend from this repo to Render at `api.kintsu.io`.

---

## 📁 What's in `/server`

```
server/
├── index.ts                  # Express server (port 3001)
├── api/
│   └── chat.ts               # Chat endpoint handlers
├── services/
│   ├── rag-engine.ts         # RAG orchestration
│   ├── retrieval.ts          # Hybrid search
│   ├── confidence-scorer.ts  # Confidence scoring
│   └── pii-redaction.ts      # PII protection
├── data/
│   └── kb/
│       └── knowledge-base.json  # 40 career coaching articles
├── types/
│   └── index.ts              # TypeScript interfaces
└── package.json              # Dependencies
```

**Endpoints:**
- `GET /health` - Health check
- `POST /api/chat` - Chat endpoint (RAG-powered)

---

## 🔧 Step-by-Step Deployment

### Option A: Deploy via Render Dashboard (Recommended)

1. **Go to Render Dashboard**
   - Visit: https://render.com/dashboard
   - Click: **New** → **Web Service**

2. **Connect Repository**
   - Select: `dominicjune-ops/Kintsu-Frontend`
   - Branch: `main`

3. **Configure Service**
   ```
   Name: kintsu-chat-api
   Region: Oregon (US West)
   Branch: main
   Root Directory: server
   Runtime: Node
   Build Command: npm install && npm run build
   Start Command: npm start
   ```

4. **Add Environment Variables**
   ```
   NODE_ENV=production
   FRONTEND_URL=https://kintsu.io
   ```

5. **Configure Health Check**
   ```
   Health Check Path: /health
   ```

6. **Select Plan**
   - Free tier is fine for now
   - Click **Create Web Service**

7. **Add Custom Domain**
   - After deployment completes
   - Go to: Settings → Custom Domains
   - Add: `api.kintsu.io`
   - Note the CNAME target (should be same as current Python backend)

---

### Option B: Deploy via render.yaml (Auto-deploy)

1. **Ensure render.yaml exists** (already created)

2. **Connect in Render Dashboard**
   - New → Blueprint
   - Connect repository
   - Render will detect `render.yaml` automatically

3. **Configure** (if needed)
   - Verify settings match render.yaml
   - Deploy

---

## ✅ Post-Deployment

### 1. Update DNS (if needed)

If you're replacing the Python backend:
- Hostinger DNS already points `api.kintsu.io` to Render
- Update CNAME if new service has different URL

### 2. Test Endpoints

**Health Check:**
```bash
curl https://api.kintsu.io/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Kinto Chat API",
  "timestamp": "2025-11-26T..."
}
```

**Chat Endpoint:**
```bash
curl -X POST https://api.kintsu.io/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I upload my resume?",
    "session_id": "test_123"
  }'
```

Expected response:
```json
{
  "answer_text": "You can upload your resume...",
  "confidence_score": 79,
  "confidence_label": "Medium",
  "provenance": [...],
  "suggested_next_steps": [...],
  "ui_actions": {...}
}
```

### 3. Update Vercel Environment Variable

**Remove or update** `VITE_API_URL`:

Option A - Use api.kintsu.io:
```
VITE_API_URL=https://api.kintsu.io
```

Option B - Use relative paths (if deploying on same domain):
```
VITE_API_URL=
(leave empty)
```

Then redeploy frontend on Vercel.

### 4. Test Chat Widget

1. Visit: https://kintsu.io
2. Click chat widget
3. Send message: "How do I upload my resume?"
4. Should receive intelligent response with confidence score

---

## 🐛 Troubleshooting

### Build Fails

**Error**: `Cannot find module`

**Fix**: Ensure all dependencies are in `server/package.json`:
```bash
cd server
npm install
npm run build
npm start  # Test locally first
```

### Server Crashes on Start

**Error**: `Port already in use`

**Fix**: Render assigns port automatically via `process.env.PORT`
- Server already handles this in `server/index.ts:12`

### CORS Errors

**Error**: `CORS policy: No 'Access-Control-Allow-Origin'`

**Fix**: Update `server/index.ts:15-18`:
```typescript
app.use(cors({
  origin: ["https://kintsu.io", "https://www.kintsu.io"],
  credentials: true
}));
```

### Chat Returns Empty Response

**Check**:
1. Render logs: Dashboard → Service → Logs
2. Look for errors in RAG engine initialization
3. Verify knowledge base JSON loaded correctly

---

## 📊 Architecture After Deployment

```
┌─────────────────────────────────────────┐
│           kintsu.io                     │
│      (Frontend - Vercel)                │
│   React, ChatWidget, Marketing          │
└───────────────┬─────────────────────────┘
                │
                │ HTTPS API Calls
                │ (VITE_API_URL)
                ▼
┌─────────────────────────────────────────┐
│        api.kintsu.io                    │
│   (Chat Backend - Render Node.js)       │
│  Express, RAG Engine, 40 KB Articles    │
└─────────────────────────────────────────┘
```

**vs. Old Python Backend:**

The Python backend at `api.kintsu.io` handles:
- Resume parsing
- Job matching
- Applications
- Stripe/billing

The Node.js backend will handle:
- Chat widget AI responses

**You can run both**:
- Option 1: Keep both, use different subdomains
  - `chat.kintsu.io` → Node.js chat
  - `api.kintsu.io` → Python backend
- Option 2: Replace Python backend entirely
- Option 3: Merge them later

---

## 🎯 Success Criteria

✅ Render service deployed and running
✅ `/health` endpoint returns 200 OK
✅ `/api/chat` returns intelligent responses
✅ Chat widget on kintsu.io works end-to-end
✅ No CORS errors in browser console
✅ Confidence scores and provenance display correctly

---

## 📝 Next Steps

After chat is working:

1. **Monitor Performance**
   - Check Render logs for errors
   - Monitor response times
   - Track confidence score distribution

2. **Enhance RAG Engine**
   - Replace mock LLM with real OpenAI/Anthropic
   - Add conversation memory
   - Implement user context

3. **Scale Up**
   - Upgrade Render plan if needed
   - Add Redis for caching
   - Implement rate limiting

---

*Generated: 2025-11-26*
*Target: Deploy Node.js chat backend to api.kintsu.io*
