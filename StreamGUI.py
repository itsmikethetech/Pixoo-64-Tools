import logging
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageGrab, Image, ImageTk, ImageDraw, ImageFilter
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

# Variable to keep track of the current resize method (default is BICUBIC)
resize_method = Image.BICUBIC

# Global variables for preview refresh
last_source_image = None  # The last raw image (screenshot or loaded) to reprocess on option changes

# Dictionary for available filters
filter_options = {
    "NONE": None,
    "BLUR": ImageFilter.BLUR,
    "CONTOUR": ImageFilter.CONTOUR,
    "DETAIL": ImageFilter.DETAIL,
    "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
    "EDGE_ENHANCE_MORE": ImageFilter.EDGE_ENHANCE_MORE,
    "EMBOSS": ImageFilter.EMBOSS,
    "FIND_EDGES": ImageFilter.FIND_EDGES,
    "SHARPEN": ImageFilter.SHARPEN,
    "SMOOTH": ImageFilter.SMOOTH,
    "SMOOTH_MORE": ImageFilter.SMOOTH_MORE
}

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
    Update the preview_label with the given image (already sized 512x512).
    """
    preview_image = draw_grid(image.copy())  # apply the grid if show_grid is True
    preview_image_tk = ImageTk.PhotoImage(preview_image)
    preview_label.config(image=preview_image_tk)
    preview_label.image = preview_image_tk

def crop_center(image):
    """Crop the image to a centered square based on the smallest dimension."""
    width, height = image.size
    new_edge = min(width, height)
    left = (width - new_edge) // 2
    top = (height - new_edge) // 2
    right = left + new_edge
    bottom = top + new_edge
    return image.crop((left, top, right, bottom))

def process_image(image):
    """
    Process the image by:
      1. Cropping to a centered square if 'Crop to 1:1' is enabled.
      2. Resizing to 64x64 using the selected scaling method.
      3. Applying the selected filter (if not 'NONE').
    """
    if crop_to_square_mode.get():
        image = crop_center(image)
    processed = image.resize((64, 64), resize_method)
    selected_filter = filter_mode_var.get()
    if selected_filter != "NONE" and filter_options[selected_filter] is not None:
        processed = processed.filter(filter_options[selected_filter])
    return processed

def refresh_preview():
    """
    If a source image is available, re-process it using current options and update the preview.
    """
    if last_source_image is not None:
        processed_image = process_image(last_source_image)
        # Scale up for preview display (512x512)
        preview_image = processed_image.resize((512, 512), resize_method)
        update_preview_label(preview_image)

def screen_capture():
    global last_source_image
    while streaming.is_set():
        if pixoo is None:
            time.sleep(0.5)
            continue

        start_time = time.time()
        try:
            screenshot = ImageGrab.grab()
            last_source_image = screenshot.copy()
            processed_image = process_image(screenshot)
            pixoo.draw_image(processed_image)
            pixoo.push()

            # Update the preview (scale processed image from 64x64 to 512x512)
            preview_image = processed_image.resize((512, 512), resize_method)
            update_preview_label(preview_image)
        except Exception as e:
            logging.error(f"Error during screen capture: {e}")
        
        elapsed_time = time.time() - start_time
        time_to_sleep = frame_duration - elapsed_time
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

def browse_image():
    global last_source_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if not file_path:
        return
    if pixoo is None:
        messagebox.showwarning("Not Connected", "Please connect to a Pixoo device first.")
        return

    try:
        image = Image.open(file_path).convert("RGB")
        last_source_image = image.copy()
        processed_image = process_image(image)
        pixoo.draw_image(processed_image)
        pixoo.push()

        # Update the preview
        preview_image = processed_image.resize((512, 512), resize_method)
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
    """Toggle the grid overlay on the preview."""
    global show_grid
    show_grid = not show_grid
    # Reapply preview update with the new grid setting
    refresh_preview()

def on_resize_mode_change(event=None):
    global resize_method
    mode = resize_mode_var.get()
    if mode == "NEAREST":
        resize_method = Image.NEAREST
    elif mode == "BILINEAR":
        resize_method = Image.BILINEAR
    elif mode == "BICUBIC":
        resize_method = Image.BICUBIC
    elif mode == "LANCZOS":
        resize_method = Image.LANCZOS
    elif mode == "BOX":
        resize_method = Image.BOX
    elif mode == "HAMMING":
        resize_method = Image.HAMMING
    refresh_preview()

def on_filter_change(event=None):
    refresh_preview()

def on_crop_toggle():
    refresh_preview()

# --- GUI Setup ---
root = tk.Tk()
root.title("Pixoo 64 Tools by MikeTheTech")

# Set up style for theme toggling
style = ttk.Style(root)
# Global variable to track current theme
current_theme = "light"

def apply_theme(theme):
    if theme == "dark":
        bg = "#2e2e2e"      # Dark background
        fg = "#ffffff"      # Light foreground
    else:
        bg = "#ffffff"      # Light background
        fg = "#000000"      # Dark foreground
    style.theme_use('clam')
    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TButton", background=bg, foreground=fg)
    style.configure("TCheckbutton", background=bg, foreground=fg)
    style.configure("TCombobox", fieldbackground=bg, background=bg, foreground=fg)
    root.configure(bg=bg)

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme(current_theme)

# Apply the initial theme
apply_theme(current_theme)

# IP Connection Frame
ip_frame = ttk.Frame(root)
ip_frame.pack(padx=10, pady=10, fill="x")

ip_label = ttk.Label(ip_frame, text="Pixoo IP:")
ip_label.pack(side=tk.LEFT, padx=5)

ip_entry = ttk.Entry(ip_frame, width=20)
ip_entry.pack(side=tk.LEFT, padx=5)
ip_entry.insert(0, DEFAULT_PIXOO_IP)

connect_button = ttk.Button(ip_frame, text="Connect", command=on_connect_button_click)
connect_button.pack(side=tk.LEFT, padx=5)

# Preview Label
preview_label = ttk.Label(root)
preview_label.pack(padx=10, pady=10)

# Control Buttons Frame
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

# Toggle Theme Button
toggle_theme_button = ttk.Button(button_frame, text="Toggle Theme", command=toggle_theme)
toggle_theme_button.pack(side=tk.LEFT, padx=5)

# --- Scaling Method Combobox ---
resize_mode_var = tk.StringVar(value="BICUBIC")  # default
resize_mode_combobox = ttk.Combobox(
    button_frame,
    textvariable=resize_mode_var,
    values=["NEAREST", "BILINEAR", "BICUBIC", "LANCZOS", "BOX", "HAMMING"],
    state="readonly",
    width=10
)
resize_mode_combobox.pack(side=tk.LEFT, padx=5)
resize_mode_combobox.bind("<<ComboboxSelected>>", on_resize_mode_change)

# --- Filter Combobox ---
filter_mode_var = tk.StringVar(value="NONE")
filter_combobox = ttk.Combobox(
    button_frame,
    textvariable=filter_mode_var,
    values=list(filter_options.keys()),
    state="readonly",
    width=12
)
filter_combobox.pack(side=tk.LEFT, padx=5)
filter_combobox.bind("<<ComboboxSelected>>", on_filter_change)

# --- Crop Toggle Checkbutton ---
crop_to_square_mode = tk.BooleanVar(value=False)
crop_checkbutton = ttk.Checkbutton(
    button_frame,
    text="Crop to 1:1",
    variable=crop_to_square_mode,
    command=on_crop_toggle
)
crop_checkbutton.pack(side=tk.LEFT, padx=5)

# Attempt initial connection to default IP (optional)
connected = connect_to_pixoo(DEFAULT_PIXOO_IP)
if not connected:
    logging.error("Initial connection to Pixoo failed. Please update IP and reconnect.")

root.mainloop()
