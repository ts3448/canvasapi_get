#!/usr/bin/env python3
"""
Test script to get courses from account 439 using canvasapi_get library.

This script demonstrates the basic functionality of the library by fetching
courses from a specific account using environment variables for configuration.
"""

import os
import sys
import logging
from pprint import pprint
from dotenv import load_dotenv

# Add the parent directory to the path so we can import canvasapi_get
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from canvasapi_get import Canvas


def setup_logging():
    """Configure detailed logging for debugging."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Enable debug logging for our library modules
    logging.getLogger('canvasapi_get').setLevel(logging.DEBUG)


def main():
    """Test getting courses from account 439."""
    # Set up detailed logging
    setup_logging()
    
    # Load environment variables from .env file
    load_dotenv()

    # Get configuration from environment variables
    canvas_url = os.getenv("CANVAS_API_URL")
    api_key = os.getenv("CANVAS_API_KEY")

    if not canvas_url:
        print("Error: CANVAS_API_URL environment variable not set")
        print("Please add CANVAS_API_URL=https://your-canvas-instance.com to .env file")
        sys.exit(1)

    if not api_key:
        print("Error: CANVAS_API_KEY environment variable not set")
        print("Please set it like: export CANVAS_API_KEY='your-api-key-here'")
        sys.exit(1)

    print(f"Connecting to Canvas at: {canvas_url}")
    print("API Key: " + "*" * (len(api_key) - 4) + api_key[-4:])  # Mask most of the key

    try:
        print("Initializing Canvas API client...")
        logging.info(f"Creating Canvas client with URL: {canvas_url}")
        canvas = Canvas(canvas_url, api_key)
        print("SUCCESS: Canvas client initialized successfully")

        # Add timeout handling and more debug info
        print(f"\nFetching account 439...")
        logging.info("About to call canvas.get_account(439)")
        
        import signal
        import time
        
        def timeout_handler(signum, frame):
            print("WARNING: Request timed out after 30 seconds!")
            raise TimeoutError("Request timed out")
        
        # Set a 30 second timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)
        
        try:
            start_time = time.time()
            account = canvas.get_account(439)
            end_time = time.time()
            signal.alarm(0)  # Cancel the alarm
            
            print(f"SUCCESS: Account retrieved: {account.name} (ID: {account.id})")
            print(f"TIMING: Request took {end_time - start_time:.2f} seconds")
            
        except TimeoutError:
            print("ERROR: The request timed out. This suggests a hanging issue.")
            logging.error("Request to get_account(439) timed out")
            sys.exit(1)

        # Get courses in the account
        print(f"\nFetching courses in account {account.id}...")
        courses = account.get_courses()

        print(f"SUCCESS: Found {len(courses)} courses")

        # Display first few courses
        print(f"\nFirst 10 courses:")
        print("-" * 80)
        for i, course in enumerate(courses[:10]):
            print(f"{i+1:2d}. {course.name} (ID: {course.id})")
            if hasattr(course, "course_code"):
                print(f"    Code: {course.course_code}")
            if hasattr(course, "enrollment_term_id"):
                print(f"    Term ID: {course.enrollment_term_id}")
            print()

        if len(courses) > 10:
            print(f"... and {len(courses) - 10} more courses")

        print(f"\nSUCCESS: Test completed successfully!")

    except Exception as e:
        print(f"ERROR: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Full traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
