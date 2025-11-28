# Kintsu - Career Transformation Platform

Transform career setbacks into golden opportunities with AI-powered career tools.

## Features

- **Marketing Website**: Beautiful kintsugi-inspired design with home, pricing, about, and legal pages
- **Job Board**: Browse and search approved job listings with real-time filtering
- **Employer Portal**: Submit job postings for review (with approval workflow)
- **Contact System**: Contact forms and newsletter subscriptions
- **AI Chatbot**: Career coaching chatbot with session persistence and user authentication
- **User Authentication**: Supabase-powered authentication with session linking
- **Dark Mode**: Full dark mode support with user preferences

## Tech Stack

- **Frontend**: React + TypeScript + TailwindCSS + Shadcn UI + Vite
- **Backend**: FastAPI + Python (separate repository)
- **Database**: PostgreSQL (Neon) with Drizzle ORM + Supabase for Auth
- **Authentication**: Supabase Auth with session linking
- **Deployment**: Vercel (Frontend) + Render (Backend)

## Getting Started

### Prerequisites

- Node.js 20+
- Supabase project (for authentication)
- Backend API deployed (FastAPI on Render/Vercel)

### Installation

```bash
npm install
```

### Environment Setup

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Fill in your Supabase credentials in `.env`:
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
VITE_API_URL=https://your-backend-api.vercel.app
```

### Database Setup

The database schema is automatically synced using Drizzle:

```bash
npm run db:push
```

### Running the Application

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Verification

Run the comprehensive verification script to ensure all components work:

```bash
npm run verify
```

This will test:
- ✅ Anonymous chat functionality
- ✅ User registration
- ✅ User login
- ✅ Session linking
- ✅ Authenticated chat
- ✅ Database connectivity

## API Integration

### Chat Endpoints
- `POST /api/chat` - Send chat message (supports anonymous and authenticated users)
- `POST /api/link-session` - Link anonymous session to authenticated user

### Authentication Flow
1. Users can chat anonymously (sessions stored locally)
2. When users sign up/login, their current session is automatically linked
3. Authenticated users maintain chat history across devices
4. Session linking preserves conversation context

## Project Structure

```
├── client/                 # Frontend React application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   │   ├── ChatWidget.tsx    # Main chat interface
│   │   │   └── AuthExample.tsx   # Authentication demo
│   │   ├── hooks/
│   │   │   └── use-auth.ts       # Supabase auth hook
│   │   ├── lib/
│   │   │   ├── session-linking.ts # Session linking utilities
│   │   │   └── utils.ts          # General utilities
│   │   ├── pages/         # Page components
│   │   └── hooks/         # Custom React hooks
├── shared/                 # Shared types and schemas
│   └── schema.ts          # Drizzle database schema
├── db/                     # Database configuration
│   └── index.ts           # Drizzle client setup
├── verify.js              # Verification script
└── .env.example           # Environment template
```

## Authentication Setup

### Supabase Configuration

1. Create a new Supabase project at https://supabase.com
2. Go to Authentication > Settings
3. Configure your site URL and redirect URLs
4. Copy your project URL and anon key to `.env`

### Session Linking

The platform supports seamless session linking:
- Anonymous users can start chatting immediately
- When they authenticate, their conversation history is preserved
- Sessions are linked using JWT tokens and backend validation

## Production Deployment

### Vercel Deployment

1. Connect your GitHub repository to Vercel
2. Add environment variables in Vercel dashboard:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
   - `VITE_API_URL`
3. Deploy automatically on git push

### Backend Requirements

Ensure your FastAPI backend supports:
- `/api/chat` endpoint with session management
- `/api/link-session` endpoint for session linking
- CORS configuration for your frontend domain

## Security Considerations

- **Authentication**: All sensitive operations require valid Supabase JWT tokens
- **Session Management**: Sessions are validated on both frontend and backend
- **CORS**: Properly configured CORS policies
- **Rate Limiting**: Implement rate limiting on chat endpoints
- **Data Validation**: All inputs are validated using Zod schemas

## License

Private - Kintsu © 2025
