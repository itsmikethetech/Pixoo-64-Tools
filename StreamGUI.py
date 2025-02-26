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

# Set the desired frames per second
fps = 60
frame_duration = 1 / fps

# Variable to control the streaming state
streaming = threading.Event()

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
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=line_color, width=line_width)
    return image

def screen_capture():
    while streaming.is_set():
        if pixoo is None:
            time.sleep(0.5)
            continue

        start_time = time.time()
        try:
            screenshot = ImageGrab.grab()
            resized_screenshot = screenshot.resize((64, 64), Image.BICUBIC)
            pixoo.draw_image(resized_screenshot)
            pixoo.push()
            preview_image = resized_screenshot.resize((512, 512), Image.BICUBIC)
            preview_image_with_grid = draw_grid(preview_image)
            preview_image_tk = ImageTk.PhotoImage(preview_image_with_grid)
            preview_label.config(image=preview_image_tk)
            preview_label.image = preview_image_tk
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
    try:
        image = Image.open(file_path).convert("RGB")
        resized_image = image.resize((64, 64), Image.BICUBIC)
        pixoo.draw_image(resized_image)
        pixoo.push()
        preview_image = resized_image.resize((512, 512), Image.BICUBIC)
        preview_image_with_grid = draw_grid(preview_image)
        preview_image_tk = ImageTk.PhotoImage(preview_image_with_grid)
        preview_label.config(image=preview_image_tk)
        preview_label.image = preview_image_tk
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

root = tk.Tk()
root.title("Pixoo Display Controller")

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

connected = connect_to_pixoo(DEFAULT_PIXOO_IP)
if not connected:
    logging.error("Initial connection to Pixoo failed. Please update IP and reconnect.")

root.mainloop()