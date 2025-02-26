import logging
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageGrab, Image, ImageTk, ImageDraw
from pixoo import Pixoo

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Default Pixoo IP address
DEFAULT_PIXOO_IP = '192.168.1.215'

# Global reference to Pixoo device (will be set by connect_to_pixoo)
pixoo = None

# Frames per second and frame duration
fps = 60
frame_duration = 1 / fps

# Control streaming state
streaming = threading.Event()

# Flag for showing/hiding grid
show_grid = True

# Variable to keep track of the current resize method
# The user will pick from "BICUBIC" or "NEAREST".
resize_method = Image.BICUBIC

# Store last preview image so we can refresh on toggle
last_preview_image = None

def connect_to_pixoo(ip_address: str) -> bool:
    global pixoo
    try:
        logging.info(f"Connecting to Pixoo at IP: {ip_address}")
        new_pixoo = Pixoo(ip_address)
        logging.info("Successfully connected to Pixoo.")
        pixoo = new_pixoo
        return True
    except Exception as e:
        logging.error(f"Failed to connect to Pixoo: {e}")
        return False

def draw_grid(image, grid_size=8, line_color=(200, 200, 200), line_width=1):
    """Draw grid lines on the given image if show_grid is True."""
    if not show_grid:
        return image  # Return unchanged if grid is not shown

    draw = ImageDraw.Draw(image)
    width, height = image.size
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=line_color, width=line_width)
    return image

def update_preview_label(image: Image.Image):
    """
    Update the global preview_label with the given image (already sized 512x512).
    Store a copy in last_preview_image so we can refresh on grid toggle or resizing mode change.
    """
    global last_preview_image
    last_preview_image = image.copy()
    preview_image = draw_grid(image.copy())  # apply the grid if show_grid is True

    preview_image_tk = ImageTk.PhotoImage(preview_image)
    preview_label.config(image=preview_image_tk)
    preview_label.image = preview_image_tk

def screen_capture():
    while streaming.is_set():
        if pixoo is None:
            time.sleep(0.5)
            continue

        start_time = time.time()
        try:
            screenshot = ImageGrab.grab()
            # Use the selected resize_method
            resized_screenshot = screenshot.resize((64, 64), resize_method)
            pixoo.draw_image(resized_screenshot)
            pixoo.push()

            # Update the preview (512x512) in the UI
            preview_image = resized_screenshot.resize((512, 512), resize_method)
            update_preview_label(preview_image)
        except Exception as e:
            logging.error(f"Error during screen capture: {e}")
        
        elapsed_time = time.time() - start_time
        time_to_sleep = frame_duration - elapsed_time
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if not file_path:
        return
    if pixoo is None:
        messagebox.showwarning("Not Connected", "Please connect to a Pixoo device first.")
        return

    try:
        image = Image.open(file_path).convert("RGB")
        # Use the selected resize_method
        resized_image = image.resize((64, 64), resize_method)
        pixoo.draw_image(resized_image)
        pixoo.push()

        # Update the preview
        preview_image = resized_image.resize((512, 512), resize_method)
        update_preview_label(preview_image)

        logging.info(f"Successfully sent image to Pixoo: {file_path}")
    except Exception as e:
        logging.error(f"Failed to process the selected image: {e}")

def start_streaming():
    if not streaming.is_set():
        if pixoo is None:
            messagebox.showerror("Connection Error", "No Pixoo device connected. Please connect first.")
            return
        logging.info("Starting screen streaming to Pixoo.")
        streaming.set()
        threading.Thread(target=screen_capture, daemon=True).start()

def stop_streaming():
    logging.info("Stopping screen streaming.")
    streaming.clear()

def on_connect_button_click():
    ip_address = ip_entry.get().strip()
    if not ip_address:
        messagebox.showwarning("Empty IP", "Please enter a valid IP address.")
        return
    success = connect_to_pixoo(ip_address)
    if success:
        messagebox.showinfo("Connected", f"Successfully connected to Pixoo at {ip_address}")
    else:
        messagebox.showerror("Connection Failed", f"Could not connect to Pixoo at {ip_address}")

def toggle_grid():
    """Toggle the global show_grid flag and refresh the preview if available."""
    global show_grid, last_preview_image
    show_grid = not show_grid

    if last_preview_image is not None:
        update_preview_label(last_preview_image)

def on_resize_mode_change(event=None):
    """
    Called whenever the user picks a new resize method from the Combobox.
    Updates global resize_method and refreshes the preview if available.
    """
    global resize_method, last_preview_image
    mode = resize_mode_var.get()
    if mode == "NEAREST":
        resize_method = Image.NEAREST
    else:
        resize_method = Image.BICUBIC
    if last_preview_image is not None:
        update_preview_label(last_preview_image)

# --- GUI Setup ---
root = tk.Tk()
root.title("Pixoo 64 Tools by MikeTheTech")

ip_frame = ttk.Frame(root)
ip_frame.pack(padx=10, pady=10, fill="x")

ip_label = ttk.Label(ip_frame, text="Pixoo IP:")
ip_label.pack(side=tk.LEFT, padx=5)

ip_entry = ttk.Entry(ip_frame, width=20)
ip_entry.pack(side=tk.LEFT, padx=5)
ip_entry.insert(0, DEFAULT_PIXOO_IP)

connect_button = ttk.Button(ip_frame, text="Connect", command=on_connect_button_click)
connect_button.pack(side=tk.LEFT, padx=5)

preview_label = ttk.Label(root)
preview_label.pack(padx=10, pady=10)

button_frame = ttk.Frame(root)
button_frame.pack(padx=10, pady=10)

start_button = ttk.Button(button_frame, text="Start Streaming", command=start_streaming)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = ttk.Button(button_frame, text="Stop Streaming", command=stop_streaming)
stop_button.pack(side=tk.LEFT, padx=5)

browse_button = ttk.Button(button_frame, text="Browse Image", command=browse_image)
browse_button.pack(side=tk.LEFT, padx=5)

grid_button = ttk.Button(button_frame, text="Toggle Grid", command=toggle_grid)
grid_button.pack(side=tk.LEFT, padx=5)

# --- Combobox for selecting resize method ---
resize_mode_var = tk.StringVar(value="BICUBIC")  # default
resize_mode_combobox = ttk.Combobox(
    button_frame,
    textvariable=resize_mode_var,
    values=["BICUBIC", "NEAREST"],
    state="readonly"
)
resize_mode_combobox.pack(side=tk.LEFT, padx=5)
resize_mode_combobox.bind("<<ComboboxSelected>>", on_resize_mode_change)

# Attempt initial connection to default IP (optional)
connected = connect_to_pixoo(DEFAULT_PIXOO_IP)
if not connected:
    logging.error("Initial connection to Pixoo failed. Please update IP and reconnect.")

root.mainloop()
