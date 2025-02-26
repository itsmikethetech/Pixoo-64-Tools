import logging
from PIL import ImageGrab, Image
from pixoo import Pixoo

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

# Capture the current screen
try:
    logging.debug("Capturing the screen.")
    screenshot = ImageGrab.grab()
    logging.debug("Screen captured successfully.")
except Exception as e:
    logging.error(f"Failed to capture the screen: {e}")
    exit(1)

# Resize the screenshot to 64x64 pixels
try:
    logging.debug("Resizing the screenshot to 64x64 pixels.")
    resized_screenshot = screenshot.resize((64, 64), Image.BICUBIC)
    logging.debug("Screenshot resized successfully.")
except Exception as e:
    logging.error(f"Failed to resize the screenshot: {e}")
    exit(1)

# Send the image to Pixoo
try:
    logging.debug("Sending the image to Pixoo.")
    pixoo.draw_image(resized_screenshot)
    pixoo.push()
    logging.debug("Image sent and displayed successfully.")
except Exception as e:
    logging.error(f"Failed to send the image to Pixoo: {e}")
    exit(1)
