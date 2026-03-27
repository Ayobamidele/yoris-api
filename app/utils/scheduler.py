"""
app/utils/scheduler.py  —  Background job scheduler.
Add periodic tasks here using APScheduler or any compatible library.
"""
import logging

logger = logging.getLogger(__name__)


def init_scheduler() -> None:
    """
    Initialise background jobs.
    Called once during app startup (lifespan).
    Extend this function to register APScheduler jobs, cron tasks, etc.
    """
    logger.info("Scheduler initialised (no jobs registered yet).")
