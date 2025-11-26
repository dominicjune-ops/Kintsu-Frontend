# 🚀 Kintsu.io Production Setup Checklist

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       kintsu.io                             │
│              (Frontend - Vercel)                            │
│   React UI, ChatWidget, Marketing Pages                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ HTTPS API Calls
                      │ (VITE_API_URL)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   api.kintsu.io                             │
│              (Backend - Render)                             │
│   Python FastAPI, RAG Engine, ML Models                    │
│   ATS Scorers, Job Scrapers, Pipelines                     │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Step 1: Vercel Frontend Configuration

### 1.1 Repository
- ✅ **Repo**: `dominicjune-ops/Kintsu-Frontend`
- ✅ **Vercel Project**: `kintsu-frontend`
- ✅ **Production Domain**: `kintsu.io`

### 1.2 Add Environment Variable in Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Select project: **kintsu-frontend**
3. Navigate to: **Settings** → **Environment Variables**
4. Add new variable:
   ```
   Name: VITE_API_URL
   Value: https://api.kintsu.io
   Environment: Production ✓
   ```
5. Click **Save**

### 1.3 Redeploy

After adding the environment variable:
1. Go to **Deployments** tab
2. Click **"..."** on the latest deployment
3. Select **Redeploy**
4. Wait for deployment to complete (~2 minutes)

---

## ✅ Step 2: DNS Configuration in Hostinger

### 2.1 Frontend Domain (Already Configured)
- ✅ `kintsu.io` → Vercel (ALIAS/A record)
- ✅ `www.kintsu.io` → `cname.vercel-dns.com` (CNAME)

### 2.2 Backend API Domain (NEW)

Add this CNAME record in Hostinger:

| Type  | Name | Target (Value)                         | TTL   |
|-------|------|----------------------------------------|-------|
| CNAME | api  | `<your-render-service>.onrender.com`   | 14400 |

**To find your Render service URL:**
1. Go to https://render.com/dashboard
2. Select your backend service (likely `careercoach-ai` or similar)
3. Look for the service URL (e.g., `careercoach-ai.onrender.com`)
4. Use that as the CNAME target

**Example:**
```
Type: CNAME
Name: api
Target: careercoach-ai.onrender.com
TTL: 14400
```

**DNS Propagation Time:** 15-40 minutes

---

## ✅ Step 3: Render Backend Configuration

### 3.1 Add Custom Domain

1. Go to https://render.com/dashboard
2. Select your Python backend service
3. Navigate to: **Settings** → **Custom Domains**
4. Click **Add Custom Domain**
5. Enter: `api.kintsu.io`
6. Click **Save**

Render will provide a CNAME target (use this in Step 2.2 above)

### 3.2 Enable CORS for Frontend

In your backend code (FastAPI example):

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kintsu.io", "https://www.kintsu.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Location to update:**
- Likely in: `backend/main.py` or `backend/api/app.py`
- Or wherever your FastAPI app is initialized

**After updating:**
1. Commit and push changes to your backend repo
2. Render will auto-deploy (check deployment logs)

### 3.3 Verify Backend Endpoint

Find your chat endpoint in the backend code:

Common patterns:
```python
@app.post("/api/chat")
@app.post("/api/v1/chat")
@app.post("/chat")
```

**Search for files like:**
- `conversation_memory.py`
- `ai_intelligence_engine.py`
- `ai_client.py`
- Any file with `@app.post` decorators

**Document the exact endpoint path here:**
```
Backend Chat Endpoint: /api/___________
```

---

## ✅ Step 4: Test the Setup

### 4.1 Test Backend API (After DNS Propagates)

**Health Check:**
```bash
curl https://api.kintsu.io
```

Expected: Some response (even a 404 or "not found" means DNS works)

**Chat Endpoint:**
```bash
curl -X POST https://api.kintsu.io/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test_123"}'
```

Expected: JSON response from your Python backend

### 4.2 Test Frontend

1. Visit: https://kintsu.io
2. Open chat widget (bottom right)
3. Send a test message: "How do I upload my resume?"
4. **Check browser console (F12)** for:
   - ✅ No CORS errors
   - ✅ Request goes to `https://api.kintsu.io/api/chat`
   - ✅ Response received

---

## ✅ Step 5: Clean Up Old Deployments (Optional)

### Option A: Deprecate `app.kintsu.io`
1. Remove domain binding from old Vercel project
2. Redirect `app.kintsu.io` → `kintsu.io`

### Option B: Convert to Admin Dashboard
- Keep `app.kintsu.io` for internal tools
- Analytics dashboard
- Beta testing UI

### Option C: User Dashboard
- Logged-in experience
- Separate from marketing site

**Decision:** _______________ (choose after main setup works)

---

## 🐛 Troubleshooting

### DNS Not Propagating
```bash
# Check DNS resolution
nslookup api.kintsu.io

# Expected output: CNAME pointing to Render
```

### CORS Errors in Browser
- Verify CORS is enabled in backend (Step 3.2)
- Check backend logs in Render dashboard
- Ensure `allow_origins` includes `https://kintsu.io`

### 404 on API Endpoint
- Verify custom domain added in Render (Step 3.1)
- Check Render deployment logs for errors
- Confirm endpoint path matches frontend call

### Frontend Not Using New API URL
- Verify environment variable added in Vercel (Step 1.2)
- Check that you redeployed after adding env var (Step 1.3)
- View deployment logs to confirm env var is set

---

## 📊 Success Criteria

Once everything is working:

✅ `https://kintsu.io` loads frontend
✅ `https://api.kintsu.io` responds (even if just health check)
✅ Chat widget sends messages successfully
✅ No CORS errors in browser console
✅ Backend processes requests and returns responses
✅ DNS resolves correctly for both domains

---

## 🎉 Final Architecture Benefits

✅ **Frontend (Vercel)**: Global CDN, instant deploys, serverless
✅ **Backend (Render)**: Full Python stack, persistent workers, ML models
✅ **Clean Separation**: Frontend and backend can scale independently
✅ **No Serverless Limits**: Heavy ML work runs on Render without timeouts
✅ **Professional Setup**: Industry-standard microservices architecture

---

## 📝 Notes

**Frontend Repo**: https://github.com/dominicjune-ops/Kintsu-Frontend
**Backend Repo**: https://github.com/dominicjune-ops/CareerCoach.ai

**Deployment Status:**
- Frontend: https://vercel.com/dashboard
- Backend: https://render.com/dashboard

**DNS Management**: Hostinger

---

*Last Updated: 2025-11-26*
*Architecture: Frontend (Vercel) + Backend (Render)*
