"""
Test script to post a reel immediately (for testing)
"""
import sys
from scheduler import ReelScheduler
from utils import logger

def main():
    """Run a test post"""
    logger.info("Running test post...")
    
    scheduler = ReelScheduler()
    success = scheduler.post_daily_reel()
    
    if success:
        logger.info("Test post completed successfully!")
        sys.exit(0)
    else:
        logger.error("Test post failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
