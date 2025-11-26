# Kintsu Frontend Deployment Guide

## Step 1: Deploy Frontend to kintsu.io

This guide covers deploying the Kintsu frontend (marketing site + SaaS app + ChatWidget) to **kintsu.io**.

---

## Prerequisites

1. **GitHub Repository**: Code is already in `dominicjune-ops/Kintsu-Replit`
2. **Custom Domain**: kintsu.io (configured in your DNS provider)
3. **Hosting Account**: Choose one:
   - Vercel (Recommended)
   - Netlify
   - Cloudflare Pages

---

## Option A: Deploy with Vercel (Recommended)

### 1. Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### 2. Deploy via Vercel Web Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Import from GitHub: `dominicjune-ops/Kintsu-Replit`
4. Configure Project:
   - **Framework Preset**: Vite
   - **Root Directory**: `./` (leave default)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist/public`
5. Add Environment Variables (optional for now):
   - `VITE_API_URL`: `http://localhost:3001` (or leave empty to configure later)
6. Click **"Deploy"**

### 3. Configure Custom Domain

1. In Vercel project settings → **Domains**
2. Add domain: `kintsu.io`
3. Add domain: `www.kintsu.io`
4. Vercel will provide DNS records to configure

### 4. Update DNS Records

In your DNS provider (GoDaddy, Cloudflare, etc.):

**For root domain (kintsu.io)**:
```
Type: A
Name: @
Value: 76.76.21.21
```

**For www subdomain**:
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

### 5. Verify Deployment

- Visit `https://kintsu.io` → Should show marketing site
- Visit `https://kintsu.io/app` → Should show dashboard
- Visit `https://kintsu.io/app/coach` → Should show Kinto chat

---

## Option B: Deploy with Netlify

### 1. Deploy via Netlify Web Dashboard

1. Go to [netlify.com](https://netlify.com)
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect to GitHub: `dominicjune-ops/Kintsu-Replit`
4. Configure Build Settings:
   - **Base directory**: `./`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist/public`
5. Click **"Deploy site"**

### 2. Configure Custom Domain

1. In Netlify site settings → **Domain management**
2. Add custom domain: `kintsu.io`
3. Netlify will provide DNS records

### 3. Update DNS Records

**For root domain**:
```
Type: A
Name: @
Value: 75.2.60.5
```

**For www subdomain**:
```
Type: CNAME
Name: www
Value: [your-site-name].netlify.app
```

---

## Option C: Deploy with Cloudflare Pages

### 1. Deploy via Cloudflare Dashboard

1. Go to Cloudflare dashboard → **Pages**
2. Click **"Create a project"**
3. Connect GitHub: `dominicjune-ops/Kintsu-Replit`
4. Configure Build:
   - **Build command**: `npm run build`
   - **Build output directory**: `dist/public`
5. Click **"Save and Deploy"**

### 2. Configure Custom Domain

1. Add `kintsu.io` as custom domain
2. Cloudflare automatically handles DNS if domain is on Cloudflare

---

## Post-Deployment Configuration

### 1. Test All Routes

Visit these URLs after deployment:

- ✅ `https://kintsu.io/` → Marketing homepage
- ✅ `https://kintsu.io/app` → SaaS dashboard
- ✅ `https://kintsu.io/app/onboarding` → Onboarding flow
- ✅ `https://kintsu.io/app/coach` → Kinto AI chat
- ✅ Chat widget (bottom-right bubble) → Should open/close

### 2. Configure Backend API

Currently, the ChatWidget calls `http://localhost:3001/api/chat`. You have two options:

**Option 1: Use Internal RAG Backend** (server folder in this repo)
- Deploy `server/` folder to Railway/Render/Vercel
- Update environment variable: `VITE_API_URL=https://your-backend.railway.app`

**Option 2: Use External Backend** (CareerCoach.ai)
- Update environment variable: `VITE_API_URL=https://api.careercoach.ai`

To update environment variables in Vercel:
1. Go to Project Settings → **Environment Variables**
2. Add `VITE_API_URL` with your backend URL
3. Redeploy

### 3. Update ChatWidget API URL

If you want to hardcode the backend URL instead of using env vars, edit:

**File**: `client/src/components/ChatWidget.tsx`

```typescript
// Line 86 - Update this:
const response = await fetch("http://localhost:3001/api/chat", {
  // ... to:
const response = await fetch(import.meta.env.VITE_API_URL + "/api/chat" || "http://localhost:3001/api/chat", {
```

Or hardcode:
```typescript
const response = await fetch("https://your-backend-url.com/api/chat", {
```

---

## Deployment Checklist

- [ ] Frontend deployed to hosting provider
- [ ] Custom domain `kintsu.io` configured with DNS
- [ ] SSL certificate active (auto via Vercel/Netlify/Cloudflare)
- [ ] All routes tested (marketing, app, onboarding, coach)
- [ ] Chat widget appears and opens
- [ ] Backend API configured (choose internal RAG or external)
- [ ] Environment variables set
- [ ] Favicon displays correctly

---

## Current Status

**Frontend Structure**:
```
kintsu.io/                  → Marketing homepage (Hero, Features, etc.)
kintsu.io/app               → SaaS Dashboard with Journey Map
kintsu.io/app/onboarding    → 3-step onboarding wizard
kintsu.io/app/coach         → Kinto AI chat interface
kintsu.io/app/insights      → Insights page (placeholder)
kintsu.io/app/pathways      → Pathways page (placeholder)
```

**Backend Options**:
- **Internal**: RAG engine in `server/` folder (40 KB articles, hybrid search, confidence scoring)
- **External**: CareerCoach.ai backend (to be configured)

---

## Troubleshooting

### Issue: Routes not working (404 errors)

**Solution**: Ensure rewrites are configured for SPA routing.

**Vercel**: Already configured in `vercel.json`

**Netlify**: Create `client/public/_redirects`:
```
/*    /index.html   200
```

**Cloudflare Pages**: Create `client/public/_redirects`:
```
/*    /index.html   200
```

### Issue: Chat widget not connecting to backend

**Check**:
1. Backend is deployed and accessible
2. CORS is configured on backend to allow `https://kintsu.io`
3. API URL is correct in environment variables

### Issue: Favicon too small

**Fixed**: Already updated `client/index.html` to use larger favicon sizes

### Issue: Build fails on deployment

**Common causes**:
- TypeScript errors: Run `npm run check` locally
- Missing dependencies: Run `npm install` locally
- Wrong build command: Should be `npm run build`
- Wrong output directory: Should be `dist/public`

---

## Next Steps After Deployment

1. **Monitor Performance**: Use Vercel Analytics or Google Analytics
2. **Add Backend**: Deploy `server/` folder or configure CareerCoach.ai
3. **Test with Users**: Share `https://kintsu.io` and gather feedback
4. **Enable Real LLM**: Swap mock responses with OpenAI/Anthropic

---

## Support

- Vercel Docs: https://vercel.com/docs
- Netlify Docs: https://docs.netlify.com
- Cloudflare Pages Docs: https://developers.cloudflare.com/pages

For issues, check logs in your hosting provider's dashboard.
