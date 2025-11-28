"""
Create Supabase tables from migration files
Run this to set up your database schema
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print(" Missing Supabase credentials!")
    exit(1)

print("🔌 Connecting to Supabase...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
print(" Connected!\n")

# SQL to create candidates table
candidates_sql = """
-- Create candidates table
CREATE TABLE IF NOT EXISTS public.candidates (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    candidate_id INTEGER UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(50),
    location VARCHAR(255),
    master_resume TEXT,
    core_skills TEXT[],
    target_roles TEXT[],
    salary_min INTEGER,
    salary_max INTEGER,
    salary_currency VARCHAR(3) DEFAULT 'USD',
    profile_data JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(50) DEFAULT 'active',
    is_active BOOLEAN DEFAULT true,
    linkedin_url VARCHAR(500),
    github_url VARCHAR(500),
    portfolio_url VARCHAR(500),
    years_of_experience INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_candidates_email ON public.candidates(email);
CREATE INDEX IF NOT EXISTS idx_candidates_status ON public.candidates(status);
CREATE INDEX IF NOT EXISTS idx_candidates_user_id ON public.candidates(user_id);
CREATE INDEX IF NOT EXISTS idx_candidates_profile_data ON public.candidates USING GIN(profile_data);
CREATE INDEX IF NOT EXISTS idx_candidates_skills ON public.candidates USING GIN(core_skills);

-- Enable RLS
ALTER TABLE public.candidates ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY IF NOT EXISTS "Users can view own candidates" 
ON public.candidates FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY IF NOT EXISTS "Users can insert own candidates" 
ON public.candidates FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY IF NOT EXISTS "Users can update own candidates" 
ON public.candidates FOR UPDATE 
USING (auth.uid() = user_id);

CREATE POLICY IF NOT EXISTS "Users can delete own candidates" 
ON public.candidates FOR DELETE 
USING (auth.uid() = user_id);

-- Service role can do everything
CREATE POLICY IF NOT EXISTS "Service role has full access to candidates"
ON public.candidates
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);
"""

# SQL to create job_postings table  
job_postings_sql = """
-- Create enums
DO $$ BEGIN
    CREATE TYPE job_type_enum AS ENUM ('full-time', 'part-time', 'contract', 'temporary', 'internship', 'volunteer');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE work_location_enum AS ENUM ('on-site', 'remote', 'hybrid');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create job_postings table
CREATE TABLE IF NOT EXISTS public.job_postings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    industry VARCHAR(100),
    job_description TEXT,
    job_board_source VARCHAR(100),
    job_board_url VARCHAR(1000),
    salary_min INTEGER,
    salary_max INTEGER,
    salary_currency VARCHAR(3) DEFAULT 'USD',
    job_type job_type_enum,
    work_location work_location_enum,
    posting_date DATE,
    application_deadline DATE,
    required_skills TEXT[],
    preferred_skills TEXT[],
    experience_level VARCHAR(50),
    education_requirement VARCHAR(100),
    benefits TEXT[],
    posting_data JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(50) DEFAULT 'active',
    is_active BOOLEAN DEFAULT true,
    company_size VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_job_postings_company ON public.job_postings(company_name);
CREATE INDEX IF NOT EXISTS idx_job_postings_location ON public.job_postings(location);
CREATE INDEX IF NOT EXISTS idx_job_postings_status ON public.job_postings(status);
CREATE INDEX IF NOT EXISTS idx_job_postings_job_type ON public.job_postings(job_type);
CREATE INDEX IF NOT EXISTS idx_job_postings_posting_date ON public.job_postings(posting_date);
CREATE INDEX IF NOT EXISTS idx_job_postings_posting_data ON public.job_postings USING GIN(posting_data);
CREATE INDEX IF NOT EXISTS idx_job_postings_required_skills ON public.job_postings USING GIN(required_skills);

-- Enable RLS
ALTER TABLE public.job_postings ENABLE ROW LEVEL SECURITY;

-- RLS Policies (all authenticated users can read)
CREATE POLICY IF NOT EXISTS "Authenticated users can view job postings" 
ON public.job_postings FOR SELECT 
TO authenticated
USING (true);

-- Service role can do everything
CREATE POLICY IF NOT EXISTS "Service role has full access to job_postings"
ON public.job_postings
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);
"""

# SQL to create applications table
applications_sql = """
-- Create enums
DO $$ BEGIN
    CREATE TYPE application_status_enum AS ENUM (
        'draft', 'submitted', 'under_review', 'interview_scheduled', 
        'interviewing', 'offer_received', 'offer_accepted', 
        'offer_declined', 'rejected', 'withdrawn'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE application_method_enum AS ENUM (
        'online_portal', 'email', 'referral', 'recruiter', 
        'career_fair', 'linkedin', 'direct'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create applications table
CREATE TABLE IF NOT EXISTS public.applications (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    candidate_id UUID REFERENCES public.candidates(id) ON DELETE CASCADE NOT NULL,
    job_posting_id UUID REFERENCES public.job_postings(id) ON DELETE SET NULL,
    application_name VARCHAR(255),
    application_date DATE DEFAULT CURRENT_DATE,
    status application_status_enum DEFAULT 'draft',
    application_method application_method_enum,
    notes TEXT,
    resume_id UUID,
    cover_letter_id UUID,
    follow_up_date DATE,
    interview_date TIMESTAMP WITH TIME ZONE,
    offer_date DATE,
    offer_deadline DATE,
    rejection_date DATE,
    rejection_reason TEXT,
    application_data JSONB DEFAULT '{}'::jsonb,
    days_since_application INTEGER GENERATED ALWAYS AS (CURRENT_DATE - application_date) STORED,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(candidate_id, job_posting_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_applications_candidate ON public.applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_applications_job_posting ON public.applications(job_posting_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON public.applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_date ON public.applications(application_date);
CREATE INDEX IF NOT EXISTS idx_applications_follow_up ON public.applications(follow_up_date);
CREATE INDEX IF NOT EXISTS idx_applications_application_data ON public.applications USING GIN(application_data);

-- Enable RLS
ALTER TABLE public.applications ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY IF NOT EXISTS "Users can view own applications" 
ON public.applications FOR SELECT 
USING (
    candidate_id IN (
        SELECT id FROM public.candidates WHERE user_id = auth.uid()
    )
);

CREATE POLICY IF NOT EXISTS "Users can insert own applications" 
ON public.applications FOR INSERT 
WITH CHECK (
    candidate_id IN (
        SELECT id FROM public.candidates WHERE user_id = auth.uid()
    )
);

CREATE POLICY IF NOT EXISTS "Users can update own applications" 
ON public.applications FOR UPDATE 
USING (
    candidate_id IN (
        SELECT id FROM public.candidates WHERE user_id = auth.uid()
    )
);

CREATE POLICY IF NOT EXISTS "Users can delete own applications" 
ON public.applications FOR DELETE 
USING (
    candidate_id IN (
        SELECT id FROM public.candidates WHERE user_id = auth.uid()
    )
);

-- Service role can do everything
CREATE POLICY IF NOT EXISTS "Service role has full access to applications"
ON public.applications
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);
"""

# Create updated_at trigger function
trigger_sql = """
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables
DROP TRIGGER IF EXISTS update_candidates_updated_at ON public.candidates;
CREATE TRIGGER update_candidates_updated_at
    BEFORE UPDATE ON public.candidates
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_job_postings_updated_at ON public.job_postings;
CREATE TRIGGER update_job_postings_updated_at
    BEFORE UPDATE ON public.job_postings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_applications_updated_at ON public.applications;
CREATE TRIGGER update_applications_updated_at
    BEFORE UPDATE ON public.applications
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
"""

print(" This script will create the following tables in your Supabase instance:")
print("   • candidates (with RLS)")
print("   • job_postings (with RLS)")  
print("   • applications (with RLS)")
print()
print("  NOTE: This uses Supabase SQL Editor / PostgREST")
print("   You may need to run these SQL statements manually in the Supabase dashboard.")
print()

# Save SQL to files
with open('create_candidates_table.sql', 'w') as f:
    f.write(candidates_sql)
print(" Saved: create_candidates_table.sql")

with open('create_job_postings_table.sql', 'w') as f:
    f.write(job_postings_sql)
print(" Saved: create_job_postings_table.sql")

with open('create_applications_table.sql', 'w') as f:
    f.write(applications_sql)
print(" Saved: create_applications_table.sql")

with open('create_triggers.sql', 'w') as f:
    f.write(trigger_sql)
print(" Saved: create_triggers.sql")

print()
print("=" * 80)
print(" NEXT STEPS:")
print("=" * 80)
print()
print("1. Go to your Supabase SQL Editor:")
print(f"   {SUPABASE_URL}/project/ktitfajlacjysacdsfxf/sql")
print()
print("2. Run these SQL files in order:")
print("   a. create_candidates_table.sql")
print("   b. create_job_postings_table.sql")
print("   c. create_applications_table.sql")
print("   d. create_triggers.sql")
print()
print("3. Or copy/paste the SQL from the files above into the SQL Editor")
print()
print("4. After running, test with: python scripts/connect_to_supabase.py")
print()
