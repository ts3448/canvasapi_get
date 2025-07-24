#!/usr/bin/env python3
"""Test script to retrieve all courses from enrollment term 583 without timeout."""

import asyncio
import logging
import os
import sys
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from canvasapi_get.canvas import Canvas

# Load environment variables
load_dotenv()

# Configure logging for detailed output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Set specific loggers for debugging
logging.getLogger('canvasapi_get.async_requester').setLevel(logging.INFO)
logging.getLogger('canvasapi_get.rate_limit_coordinator').setLevel(logging.INFO)
logging.getLogger('canvasapi_get.paginated_list').setLevel(logging.INFO)

logger = logging.getLogger(__name__)

def main():
    """Test retrieving all courses from enrollment term 583."""
    
    # Get environment variables
    canvas_url = os.getenv('CANVAS_API_URL')
    api_key = os.getenv('CANVAS_API_KEY')
    
    if not canvas_url or not api_key:
        logger.error("Missing required environment variables:")
        logger.error("- CANVAS_API_URL: Canvas instance URL")
        logger.error("- CANVAS_API_KEY: Canvas API token")
        return 1
    
    logger.info(f"Canvas URL: {canvas_url}")
    logger.info("API Key: [REDACTED]")
    
    try:
        # Initialize Canvas instance
        logger.info("Initializing Canvas instance...")
        canvas = Canvas(canvas_url, api_key)
        logger.info("Canvas instance created successfully")
        
        # Get the current user first to verify connection
        logger.info("Testing API connection...")
        user = canvas.get_current_user()
        logger.info(f"Connected successfully as: {user.name} (ID: {user.id})")
        
        # Get courses from account 439 with enrollment term 583
        logger.info("Retrieving courses from account 439 with enrollment term 583...")
        start_time = time.time()
        
        # Get the account first
        account = canvas.get_account(439)
        logger.info(f"Retrieved account: {account.name} (ID: {account.id})")
        
        # Request courses from the account with enrollment_term_id filter
        courses = account.get_courses(enrollment_term_id=583)
        
        # Count courses as we iterate
        course_count = 0
        last_log_time = start_time
        log_interval = 10  # Log progress every 10 seconds
        
        logger.info("Starting course enumeration...")
        
        for course in courses:
            course_count += 1
            
            # Log progress periodically
            current_time = time.time()
            if current_time - last_log_time >= log_interval:
                elapsed = current_time - start_time
                logger.info(f"Progress: {course_count} courses retrieved in {elapsed:.1f} seconds")
                last_log_time = current_time
            
            # Optional: Log first few courses for verification
            if course_count <= 5:
                logger.info(f"Course {course_count}: {course.name} (ID: {course.id})")
        
        # Final results
        end_time = time.time()
        total_time = end_time - start_time
        
        logger.info("=== FINAL RESULTS ===")
        logger.info(f"Total courses retrieved: {course_count}")
        logger.info(f"Total time: {total_time:.2f} seconds")
        
        if course_count > 0:
            logger.info(f"Average time per course: {(total_time / course_count) * 1000:.1f} ms")
        
        logger.info("Course retrieval completed successfully!")
        
        # Clean up async sessions to prevent warnings
        logger.info("Cleaning up async sessions...")
        from canvasapi_get.async_requester import AsyncRequester
        import asyncio
        
        async def cleanup():
            await AsyncRequester.cleanup_all_sessions()
        
        try:
            asyncio.run(cleanup())
            logger.info("Session cleanup completed")
        except Exception as e:
            logger.debug(f"Cleanup error (non-critical): {e}")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        return 130
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full traceback:")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)