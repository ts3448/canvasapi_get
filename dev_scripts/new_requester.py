import os
from canvasapi_get import Canvas

# Canvas API URL and key from environment variables
CANVAS_API_URL = os.environ.get("CANVAS_API_URL")
CANVAS_API_KEY = os.environ.get("CANVAS_API_KEY")

print(CANVAS_API_URL)

# Initialize a new Canvas object
canvas = Canvas(CANVAS_API_URL, CANVAS_API_KEY)

print(canvas)
