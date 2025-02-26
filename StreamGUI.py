import logging
import time
import threading
import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab, Image, ImageTk, ImageDraw
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

# Set the desired frames per second
fps = 60
frame_duration = 1 / fps

# Initialize the main application window
root = tk.Tk()
root.title("Pixoo Display Controller")

# Create a label to display the preview image
preview_label = ttk.Label(root)
preview_label.pack(padx=10, pady=10)

# Variable to control the streaming state
streaming = threading.Event()

def draw_grid(image, grid_size=8, line_color=(200, 200, 200), line_width=1):
    """Draw a grid over the image."""
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Draw vertical lines
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)

    # Draw horizontal lines
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=line_color, width=line_width)

    return image

def screen_capture():
    """Capture the screen and update the Pixoo display."""
    while streaming.is_set():
        start_time = time.time()

        # Capture the current screen
        try:
            screenshot = ImageGrab.grab()
        except Exception as e:
            logging.error(f"Failed to capture the screen: {e}")
            continue

        # Resize the screenshot to 64x64 pixels for Pixoo
        try:
            resized_screenshot = screenshot.resize((64, 64), Image.NEAREST)
        except Exception as e:
            logging.error(f"Failed to resize the screenshot: {e}")
            continue

        # Send the image to Pixoo
        try:
            pixoo.draw_image(resized_screenshot)
            pixoo.push()
        except Exception as e:
            logging.error(f"Failed to send the image to Pixoo: {e}")
            continue

        # Resize the 64x64 image to 512x512 pixels for preview
        try:
            preview_image = resized_screenshot.resize((512, 512), Image.NEAREST)
        except Exception as e:
            logging.error(f"Failed to resize the screenshot for preview: {e}")
            continue

        # Draw grid on the preview image
        try:
            preview_image_with_grid = draw_grid(preview_image)
        except Exception as e:
            logging.error(f"Failed to draw grid on the preview image: {e}")
            continue

        # Update the preview image in the GUI
        preview_image_tk = ImageTk.PhotoImage(preview_image_with_grid)
        preview_label.config(image=preview_image_tk)
        preview_label.image = preview_image_tk  # Keep a reference to avoid garbage collection

        # Calculate elapsed time and sleep to maintain the desired fps
        elapsed_time = time.time() - start_time
        time_to_sleep = frame_duration - elapsed_time
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

def start_streaming():
    """Start the screen streaming in a separate thread."""
    if not streaming.is_set():
        streaming.set()
        threading.Thread(target=screen_capture, daemon=True).start()

def stop_streaming():
    """Stop the screen streaming."""
    streaming.clear()

# Create buttons to start and stop streaming
start_button = ttk.Button(root, text="Start Streaming", command=start_streaming)
start_button.pack(side=tk.LEFT, padx=10, pady=10)

stop_button = ttk.Button(root, text="Stop Streaming", command=stop_streaming)
stop_button.pack(side=tk.LEFT, padx=10, pady=10)

# Run the GUI event loop
root.mainloop()
