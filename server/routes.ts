import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { 
  insertJobSchema,
  insertContactInquirySchema,
  insertNewsletterSubscriptionSchema
} from "@shared/schema";
import { z } from "zod";

const updateJobStatusSchema = z.object({
  status: z.enum(["pending", "approved", "rejected"])
});

export async function registerRoutes(app: Express): Promise<Server> {
  // Job routes
  app.post("/api/jobs", async (req, res) => {
    try {
      const validatedData = insertJobSchema.parse(req.body);
      const job = await storage.createJob(validatedData);
      res.status(201).json(job);
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ error: "Validation failed", details: error.errors });
      } else {
        res.status(500).json({ error: "Failed to create job posting" });
      }
    }
  });

  app.get("/api/jobs", async (req, res) => {
    try {
      const { search, tags } = req.query;
      const searchQuery = typeof search === "string" ? search : undefined;
      const tagArray = typeof tags === "string" ? tags.split(",").filter(Boolean) : undefined;
      
      const jobs = await storage.searchJobs(searchQuery, tagArray);
      res.json(jobs);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch jobs" });
    }
  });

  app.get("/api/jobs/:id", async (req, res) => {
    try {
      const job = await storage.getJob(req.params.id);
      if (!job) {
        res.status(404).json({ error: "Job not found" });
        return;
      }
      res.json(job);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch job" });
    }
  });

  // Admin route to approve/reject jobs (simple version - in production would need auth)
  app.patch("/api/jobs/:id/status", async (req, res) => {
    try {
      const validatedData = updateJobStatusSchema.parse(req.body);
      
      const job = await storage.updateJobStatus(req.params.id, validatedData.status);
      if (!job) {
        res.status(404).json({ error: "Job not found" });
        return;
      }
      
      res.json(job);
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ error: "Validation failed", details: error.errors });
      } else {
        res.status(500).json({ error: "Failed to update job status" });
      }
    }
  });

  // Contact inquiry routes
  app.post("/api/contact", async (req, res) => {
    try {
      const validatedData = insertContactInquirySchema.parse(req.body);
      const inquiry = await storage.createContactInquiry(validatedData);
      res.status(201).json({ message: "Contact inquiry received", id: inquiry.id });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ error: "Validation failed", details: error.errors });
      } else {
        res.status(500).json({ error: "Failed to submit contact inquiry" });
      }
    }
  });

  // Newsletter subscription routes
  app.post("/api/newsletter", async (req, res) => {
    try {
      const validatedData = insertNewsletterSubscriptionSchema.parse(req.body);
      const subscription = await storage.createNewsletterSubscription(validatedData);
      res.status(201).json({ message: "Subscribed successfully", id: subscription.id });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ error: "Validation failed", details: error.errors });
      } else {
        // Handle unique constraint violation for duplicate emails
        res.status(400).json({ error: "Email already subscribed" });
      }
    }
  });

  const httpServer = createServer(app);

  return httpServer;
}
