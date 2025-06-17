import os
from canvasapi_get import Canvas
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

logging.getLogger("canvasapi").setLevel(logging.DEBUG)


# Canvas API URL and key from environment variables
CANVAS_API_URL = os.environ.get("CANVAS_API_URL")
CANVAS_API_KEY = os.environ.get("CANVAS_API_KEY")


canvas = Canvas(CANVAS_API_URL, CANVAS_API_KEY)

account = canvas.get_account(439)

courses = account.get_courses()

print(len(courses))
