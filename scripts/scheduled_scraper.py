"""
Scheduled Google Jobs Scraper for Cloud Deployment

This script runs the Google Jobs scraper on a schedule (every 6 hours)
and can be deployed to Google Cloud Run Jobs or Cloud Functions.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from typing import Dict, Any, List

# Import our services
try:
    from src.google_jobs_service import GoogleJobsService
    from src.job_data_normalizer import JobDataNormalizer
except ImportError:
    print(" Unable to import services - ensure dependencies are installed")
    exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScheduledJobScraper:
    """Manages scheduled job scraping operations"""
    
    def __init__(self):
        self.google_jobs_service = GoogleJobsService()
        self.search_configs = [
            # High-demand tech jobs
            {"query": "software engineer", "location": "San Francisco", "max_results": 30},
            {"query": "python developer", "location": "Remote", "max_results": 30},
            {"query": "data scientist", "location": "New York", "max_results": 25},
            {"query": "full stack developer", "location": "Austin", "max_results": 25},
            {"query": "machine learning engineer", "location": "Seattle", "max_results": 20},
            {"query": "devops engineer", "location": "Remote", "max_results": 20},
            {"query": "product manager", "location": "San Francisco", "max_results": 20},
            {"query": "frontend developer", "location": "Remote", "max_results": 25},
            {"query": "backend engineer", "location": "Chicago", "max_results": 20},
            {"query": "mobile developer", "location": "Los Angeles", "max_results": 15},
        ]
        
    async def run_scraping_cycle(self) -> Dict[str, Any]:
        """Run a complete scraping cycle for all configured searches"""
        cycle_start = datetime.now(timezone.utc)
        logger.info(f" Starting scheduled scraping cycle at {cycle_start}")
        
        total_jobs = 0
        total_searches = len(self.search_configs)
        successful_searches = 0
        all_results = []
        errors = []
        
        for i, config in enumerate(self.search_configs, 1):
            try:
                logger.info(f"[{i}/{total_searches}] Scraping: {config['query']} in {config['location']}")
                
                result = await self.google_jobs_service.search_jobs(
                    query=config['query'],
                    location=config['location'],
                    max_results=config['max_results']
                )
                
                if result['status'] == 'success':
                    jobs_found = result['total_found']
                    total_jobs += jobs_found
                    successful_searches += 1
                    all_results.append(result)
                    
                    logger.info(f" Found {jobs_found} jobs for '{config['query']}' in {config['location']}")
                else:
                    error_msg = f"Failed to scrape {config['query']}: {result.get('message', 'Unknown error')}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    
                # Add delay between searches to be respectful
                await asyncio.sleep(3)
                
            except Exception as e:
                error_msg = f"Exception scraping {config['query']}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                continue
        
        cycle_end = datetime.now(timezone.utc)
        duration = (cycle_end - cycle_start).total_seconds()
        
        summary = {
            "cycle_start": cycle_start.isoformat(),
            "cycle_end": cycle_end.isoformat(),
            "duration_seconds": duration,
            "total_searches_configured": total_searches,
            "successful_searches": successful_searches,
            "total_jobs_found": total_jobs,
            "success_rate": (successful_searches / total_searches * 100) if total_searches > 0 else 0,
            "errors": errors,
            "status": "completed"
        }
        
        logger.info(f" Scraping cycle completed!")
        logger.info(f"    {successful_searches}/{total_searches} searches successful")
        logger.info(f"    {total_jobs} total jobs found")
        logger.info(f"    Duration: {duration:.1f} seconds")
        logger.info(f"    Success rate: {summary['success_rate']:.1f}%")
        
        # Store results (in production, save to database)
        await self._store_results(all_results, summary)
        
        return summary
    
    async def _store_results(self, results: List[Dict], summary: Dict) -> None:
        """Store scraping results (placeholder for database integration)"""
        try:
            # In production, this would save to MongoDB Atlas or similar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save summary
            summary_file = f"scraping_summary_{timestamp}.json"
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            logger.info(f" Saved summary to {summary_file}")
            
            # Save job data (for demo purposes, just log stats)
            total_jobs = sum(len(result.get('jobs', [])) for result in results)
            logger.info(f" Would save {total_jobs} jobs to database in production")
            
        except Exception as e:
            logger.error(f"Error storing results: {e}")
    
    async def get_trending_summary(self) -> Dict[str, Any]:
        """Get summary of trending jobs across all categories"""
        try:
            trending = await self.google_jobs_service.get_trending_jobs()
            high_salary = await self.google_jobs_service.get_high_salary_jobs(min_salary=120000)
            
            return {
                "trending_jobs_count": trending.get('total_found', 0),
                "high_salary_jobs_count": high_salary.get('total_found', 0),
                "categories_trending": trending.get('categories', []),
                "status": "success",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting trending summary: {e}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


async def main():
    """Main execution function for scheduled scraper"""
    logger.info(" CareerCoach.ai Scheduled Job Scraper Starting...")
    
    scraper = ScheduledJobScraper()
    
    try:
        # Run the scraping cycle
        result = await scraper.run_scraping_cycle()
        
        # Get trending summary
        trending = await scraper.get_trending_summary()
        
        # Final summary
        logger.info(" FINAL SUMMARY:")
        logger.info(f"   Jobs Found: {result['total_jobs_found']}")
        logger.info(f"   Success Rate: {result['success_rate']:.1f}%")
        logger.info(f"   Duration: {result['duration_seconds']:.1f}s")
        logger.info(f"   Trending Jobs: {trending.get('trending_jobs_count', 0)}")
        logger.info(f"   High Salary Jobs: {trending.get('high_salary_jobs_count', 0)}")
        
        return {
            "scraping_result": result,
            "trending_summary": trending,
            "overall_status": "success"
        }
        
    except Exception as e:
        logger.error(f" Scheduled scraper failed: {e}")
        return {
            "overall_status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Cloud Run Job entry point
def cloud_run_job_handler():
    """Entry point for Google Cloud Run Job"""
    logger.info("📦 Running as Google Cloud Run Job")
    result = asyncio.run(main())
    
    if result["overall_status"] == "success":
        logger.info(" Job completed successfully")
        exit(0)
    else:
        logger.error(" Job failed")
        exit(1)


# Cloud Function entry point  
def cloud_function_handler(request):
    """Entry point for Google Cloud Function (HTTP trigger)"""
    logger.info(" Running as Google Cloud Function")
    
    try:
        result = asyncio.run(main())
        return {
            "statusCode": 200,
            "body": json.dumps(result, default=str),
            "headers": {"Content-Type": "application/json"}
        }
    except Exception as e:
        logger.error(f"Cloud Function error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }


if __name__ == "__main__":
    # Local development/testing
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test mode - run once
        logger.info(" Running in test mode")
        result = asyncio.run(main())
        print(f"\n Test Result: {result['overall_status']}")
    else:
        # Production mode - could be set up with cron or scheduler
        logger.info("🏭 Running in production mode")
        result = asyncio.run(main())
        
        # In production, this could run every 6 hours
        # For now, just run once
        logger.info(" Production run completed")