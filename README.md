# Kintsu - Career Transformation Platform

Transform career setbacks into golden opportunities with AI-powered career tools.

## Features

- **Marketing Website**: Beautiful kintsugi-inspired design with home, pricing, about, and legal pages
- **Job Board**: Browse and search approved job listings with real-time filtering
- **Employer Portal**: Submit job postings for review (with approval workflow)
- **Contact System**: Contact forms and newsletter subscriptions
- **Dark Mode**: Full dark mode support with user preferences

## Tech Stack

- **Frontend**: React + TypeScript + TailwindCSS + Shadcn UI
- **Backend**: Express + TypeScript
- **Database**: PostgreSQL (Neon) with Drizzle ORM
- **Deployment**: Replit

## Getting Started

### Prerequisites

- Node.js 20+
- PostgreSQL database (automatically configured on Replit)

### Installation

```bash
npm install
```

### Database Setup

The database schema is automatically synced using Drizzle:

```bash
npm run db:push
```

### Seeding Sample Data

To populate the database with sample job postings:

```sql
-- Run this in the database console or using the execute_sql_tool
INSERT INTO jobs (company_name, role_title, location, is_remote, salary_range, job_description, contact_email, tags, type, status) VALUES
('TechVision Inc', 'Senior Product Manager', 'San Francisco, CA', false, '$140k - $180k', 'Lead product strategy for our enterprise SaaS platform.', 'hiring@techvision.io', ARRAY['Product', 'SaaS', 'Leadership'], 'Full-time', 'approved'),
('Startup Labs', 'Frontend Engineer', 'Remote', true, '$120k - $160k', 'Build beautiful, performant user interfaces with React and TypeScript.', 'jobs@startuplabs.com', ARRAY['React', 'TypeScript', 'Remote'], 'Full-time', 'approved'),
('Analytics Co', 'Data Scientist', 'New York, NY', false, '$130k - $170k', 'Apply machine learning to solve complex business problems.', 'careers@analyticsco.com', ARRAY['Python', 'ML', 'Analytics'], 'Full-time', 'approved'),
('CloudScale', 'DevOps Engineer', 'Austin, TX', true, '$125k - $165k', 'Build and maintain cloud infrastructure at scale.', 'talent@cloudscale.io', ARRAY['AWS', 'Kubernetes', 'Remote'], 'Full-time', 'approved'),
('DesignFirst', 'UX Designer', 'Remote', true, '$110k - $145k', 'Design delightful experiences for our mobile and web applications.', 'design@designfirst.com', ARRAY['Figma', 'User Research', 'Remote'], 'Full-time', 'approved')
ON CONFLICT DO NOTHING;
```

### Running the Application

```bash
npm run dev
```

The application will be available at `http://localhost:5000`

## API Endpoints

### Jobs
- `GET /api/jobs` - List approved jobs (with optional ?search= and ?tags= query params)
- `GET /api/jobs/:id` - Get job by ID
- `POST /api/jobs` - Create new job posting (status: pending)
- `PATCH /api/jobs/:id/status` - Update job status (admin only - requires auth in production)

### Contact & Newsletter
- `POST /api/contact` - Submit contact inquiry
- `POST /api/newsletter` - Subscribe to newsletter

## Project Structure

```
├── client/                 # Frontend React application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   └── lib/           # Utilities and query client
├── server/                 # Backend Express server
│   ├── routes.ts          # API routes
│   └── storage.ts         # Database storage layer
├── shared/                 # Shared types and schemas
│   └── schema.ts          # Drizzle database schema
└── db/                     # Database configuration
    └── index.ts           # Drizzle client setup
```

## Database Schema

### Jobs Table
- `id`: UUID (primary key)
- `company_name`: Company name
- `role_title`: Job title
- `location`: Job location
- `is_remote`: Remote work flag
- `salary_range`: Salary range
- `job_description`: Full description
- `contact_email`: Contact email
- `company_website`: Company URL (optional)
- `tags`: Array of tags for filtering
- `type`: Job type (Full-time, Part-time, etc.)
- `status`: Approval status (pending, approved, rejected)
- `created_at`: Timestamp

### Contact Inquiries Table
- `id`: UUID (primary key)
- `name`: Contact name
- `email`: Contact email
- `subject`: Inquiry subject
- `message`: Inquiry message
- `created_at`: Timestamp

### Newsletter Subscriptions Table
- `id`: UUID (primary key)
- `email`: Subscriber email (unique)
- `created_at`: Timestamp

## Production Considerations

### Security
- **Admin Routes**: The `PATCH /api/jobs/:id/status` route currently has no authentication. In production, implement proper authentication and authorization before deploying.
- **Rate Limiting**: Consider adding rate limiting to prevent abuse
- **CORS**: Configure CORS policies appropriately

### Performance
- **Caching**: Implement caching for approved job listings
- **Indexing**: Add database indexes on frequently queried columns (tags, status, created_at)
- **Pagination**: Add pagination to job listings for large datasets

### Monitoring
- Set up error tracking (e.g., Sentry)
- Monitor database performance
- Track API usage and response times

## Environment Variables

Required environment variables (automatically configured on Replit):
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Session encryption key

## License

Private - Kintsu © 2025
