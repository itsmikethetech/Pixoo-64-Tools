import logging
import time
import threading
import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab, Image, ImageTk, ImageDraw
from pixoo import Pixoo
from screeninfo import get_monitors  # For enumerating screens

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

# ============================================================
# MONITOR SELECTION DROPDOWN
# ============================================================
monitors = get_monitors()
monitor_var = tk.StringVar()

def get_monitor_display_text(monitor, index):
    """Helper to generate a display string for each monitor."""
    return f"Monitor {index + 1}: {monitor.width}x{monitor.height} at ({monitor.x},{monitor.y})"

monitor_choices = [get_monitor_display_text(m, i) for i, m in enumerate(monitors)]

monitor_dropdown = ttk.Combobox(root, textvariable=monitor_var, values=monitor_choices, state="readonly")
monitor_dropdown.pack(pady=5)

# Set default selection to the first monitor (if available)
if monitors:
    monitor_dropdown.current(0)

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
    """Capture a 1:1 region of the selected monitor and update the Pixoo display."""
    while streaming.is_set():
        start_time = time.time()

        try:
            # Determine which monitor is selected
            selected_index = monitor_dropdown.current()
            if selected_index < 0:
                # No valid selection
                time.sleep(1)
                continue
            monitor = monitors[selected_index]

            # Calculate a centered square bounding box for the monitor
            left = monitor.x
            top = monitor.y
            width = monitor.width
            height = monitor.height

            final_size = min(width, height)

            # Center the square region
            left += (width - final_size) // 2
            top += (height - final_size) // 2
            right = left + final_size
            bottom = top + final_size

            bbox = (left, top, right, bottom)

            # Capture just the square from the selected monitor
            screenshot = ImageGrab.grab(bbox=bbox)
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
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

start_button = ttk.Button(button_frame, text="Start Streaming", command=start_streaming)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(button_frame, text="Stop Streaming", command=stop_streaming)
stop_button.pack(side=tk.LEFT, padx=10)

# Run the GUI event loop
root.mainloop()
