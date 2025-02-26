import logging # This module helps with debugging
from pixoo import Pixoo # This module is just amazing. :)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Replace with your Pixoo's IP address
PIXOO_IP = '192.168.1.215'

# Initialize Pixoo device
try:
    logging.debug(f"Attempting to connect to Pixoo at IP: {PIXOO_IP}")
    pixoo = Pixoo(PIXOO_IP)
    logging.debug("Successfully connected to Pixoo.")
except Exception as e:
    logging.error(f"Failed to connect to Pixoo: {e}")
    exit(1)

# Clear the display
try:
    logging.debug("Clearing the display.")
    pixoo.clear()
    logging.debug("Display cleared.")
except Exception as e:
    logging.error(f"Failed to clear the display: {e}")
    exit(1)

# Draw text on the display
# You can adjust the position, color, and more using the variables below.
try:
    message = "Hello, Pixoo!"
    position = (0, 0)
    color = (255, 255, 255)  # White color
    logging.debug(f"Drawing text '{message}' at position {position} with color {color}.")
    pixoo.draw_text(message, position, color)
    logging.debug("Text drawn on the display buffer.")
except Exception as e:
    logging.error(f"Failed to draw text: {e}")
    exit(1)

# Push the buffer to the display
try:
    logging.debug("Pushing the buffer to the display.")
    pixoo.push()
    logging.debug("Buffer pushed successfully.")
except Exception as e:
    logging.error(f"Failed to push buffer to the display: {e}")
    exit(1)
