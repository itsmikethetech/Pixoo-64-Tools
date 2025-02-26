import logging
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageGrab, Image, ImageTk, ImageDraw
from pixoo import Pixoo

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Default Pixoo IP address
DEFAULT_PIXOO_IP = '192.168.1.215'

# Global reference to Pixoo device (will be set by connect_to_pixoo)
pixoo = None

# Set the desired frames per second
fps = 60
frame_duration = 1 / fps

# Variable to control the streaming state
streaming = threading.Event()

def connect_to_pixoo(ip_address: str) -> bool:
    """
    Attempt to connect to a Pixoo device at the provided IP address.
    Returns True if successful, False if it fails.
    """
    global pixoo
    try:
        logging.debug(f"Attempting to connect to Pixoo at IP: {ip_address}")
        new_pixoo = Pixoo(ip_address)
        logging.debug("Successfully connected to Pixoo.")
        pixoo = new_pixoo  # Assign the successfully connected device to the global pixoo
        return True
    except Exception as e:
        logging.error(f"Failed to connect to Pixoo: {e}")
        return False

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
        if pixoo is None:
            # If we have no valid pixoo device, just wait briefly and continue
            time.sleep(0.5)
            continue

        start_time = time.time()

        # Capture the current screen
        try:
            screenshot = ImageGrab.grab()
        except Exception as e:
            logging.error(f"Failed to capture the screen: {e}")
            continue

        # Resize the screenshot to 64x64 pixels for Pixoo
        try:
            resized_screenshot = screenshot.resize((64, 64), Image.BICUBIC)
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
            preview_image = resized_screenshot.resize((512, 512), Image.BICUBIC)
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
        if pixoo is None:
            messagebox.showerror("Connection Error", "No Pixoo device connected. Please connect first.")
            return
        streaming.set()
        threading.Thread(target=screen_capture, daemon=True).start()

def stop_streaming():
    """Stop the screen streaming."""
    streaming.clear()

def on_connect_button_click():
    """Handler for the 'Connect' button to update Pixoo IP and attempt reconnection."""
    ip_address = ip_entry.get().strip()
    if not ip_address:
        messagebox.showwarning("Empty IP", "Please enter a valid IP address.")
        return
    
    success = connect_to_pixoo(ip_address)
    if success:
        messagebox.showinfo("Connected", f"Successfully connected to Pixoo at {ip_address}")
    else:
        messagebox.showerror("Connection Failed", f"Could not connect to Pixoo at {ip_address}")

# Initialize the main application window
root = tk.Tk()
root.title("Pixoo Display Controller")

# Frame for IP entry and connection button
ip_frame = ttk.Frame(root)
ip_frame.pack(padx=10, pady=10, fill="x")

ip_label = ttk.Label(ip_frame, text="Pixoo IP:")
ip_label.pack(side=tk.LEFT, padx=5)

ip_entry = ttk.Entry(ip_frame, width=20)
ip_entry.pack(side=tk.LEFT, padx=5)
ip_entry.insert(0, DEFAULT_PIXOO_IP)  # Insert the default IP by default

connect_button = ttk.Button(ip_frame, text="Connect", command=on_connect_button_click)
connect_button.pack(side=tk.LEFT, padx=5)

# Create a label to display the preview image
preview_label = ttk.Label(root)
preview_label.pack(padx=10, pady=10)

# Create buttons to start and stop streaming
button_frame = ttk.Frame(root)
button_frame.pack(padx=10, pady=10)

start_button = ttk.Button(button_frame, text="Start Streaming", command=start_streaming)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = ttk.Button(button_frame, text="Stop Streaming", command=stop_streaming)
stop_button.pack(side=tk.LEFT, padx=5)

# Try initial connection with the default IP
connected = connect_to_pixoo(DEFAULT_PIXOO_IP)
if not connected:
    logging.error("Initial connection to Pixoo failed. Please update IP and reconnect.")

# Run the GUI event loop
root.mainloop()
