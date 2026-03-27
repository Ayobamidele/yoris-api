"""
app/utils/scheduler.py  —  Background job scheduler.
Add periodic tasks here using APScheduler or any compatible library.
"""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def log_api_status():
    """
    Background job to log the status of the API every 2 minutes.
    """
    logger.info("API Status: ACTIVE - The Yoris API is running.")

def init_scheduler() -> None:
    """
    Initialise background jobs.
    Called once during app startup (lifespan).
    Extend this function to register APScheduler jobs, cron tasks, etc.
    """
    scheduler.add_job(log_api_status, 'interval', minutes=2)
    scheduler.start()
    logger.info("Scheduler initialised (status log job registered to run every 2 minutes).")
