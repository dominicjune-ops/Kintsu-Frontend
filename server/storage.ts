import { 
  type Job, 
  type InsertJob,
  type ContactInquiry,
  type InsertContactInquiry,
  type NewsletterSubscription,
  type InsertNewsletterSubscription,
  jobs,
  contactInquiries,
  newsletterSubscriptions
} from "@shared/schema";
import { db } from "../db";
import { eq, desc, ilike, or, and, arrayOverlaps } from "drizzle-orm";

export interface IStorage {
  // Jobs
  createJob(job: InsertJob): Promise<Job>;
  getJob(id: string): Promise<Job | undefined>;
  getApprovedJobs(): Promise<Job[]>;
  searchJobs(query?: string, tags?: string[]): Promise<Job[]>;
  updateJobStatus(id: string, status: "pending" | "approved" | "rejected"): Promise<Job | undefined>;
  
  // Contact Inquiries
  createContactInquiry(inquiry: InsertContactInquiry): Promise<ContactInquiry>;
  
  // Newsletter Subscriptions
  createNewsletterSubscription(subscription: InsertNewsletterSubscription): Promise<NewsletterSubscription>;
}

export class DbStorage implements IStorage {
  async createJob(insertJob: InsertJob): Promise<Job> {
    const [job] = await db.insert(jobs).values(insertJob).returning();
    return job;
  }

  async getJob(id: string): Promise<Job | undefined> {
    const [job] = await db.select().from(jobs).where(eq(jobs.id, id)).limit(1);
    return job;
  }

  async getApprovedJobs(): Promise<Job[]> {
    return db.select().from(jobs).where(eq(jobs.status, "approved")).orderBy(desc(jobs.createdAt));
  }

  async searchJobs(query?: string, tags?: string[]): Promise<Job[]> {
    let conditions = [eq(jobs.status, "approved")];

    if (query) {
      const searchConditions = or(
        ilike(jobs.roleTitle, `%${query}%`),
        ilike(jobs.companyName, `%${query}%`),
        ilike(jobs.location, `%${query}%`)
      );
      if (searchConditions) {
        conditions.push(searchConditions);
      }
    }

    // Filter by tags if provided - use arrayOverlaps for SQL-level filtering
    if (tags && tags.length > 0) {
      conditions.push(arrayOverlaps(jobs.tags, tags));
    }

    return db.select()
      .from(jobs)
      .where(and(...conditions))
      .orderBy(desc(jobs.createdAt));
  }

  async createContactInquiry(insertInquiry: InsertContactInquiry): Promise<ContactInquiry> {
    const [inquiry] = await db.insert(contactInquiries).values(insertInquiry).returning();
    return inquiry;
  }

  async createNewsletterSubscription(insertSubscription: InsertNewsletterSubscription): Promise<NewsletterSubscription> {
    const [subscription] = await db.insert(newsletterSubscriptions).values(insertSubscription).returning();
    return subscription;
  }

  async updateJobStatus(id: string, status: "pending" | "approved" | "rejected"): Promise<Job | undefined> {
    const [job] = await db.update(jobs)
      .set({ status })
      .where(eq(jobs.id, id))
      .returning();
    return job;
  }
}

export const storage = new DbStorage();
