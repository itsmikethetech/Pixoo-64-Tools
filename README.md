# Pixoo 64 Tools by MikeTheTech

Pixoo-64-Tools is a collection of Python scripts designed to interact with the Pixoo 64, a 64×64 pixel LED display from Divoom. These tools allow you to stream your screen, send text messages, and display screenshots on the Pixoo 64 with ease.

With a simple setup and an intuitive interface, you can transform your Pixoo 64 into a live screen mirroring display, a custom message board, or a real-time pixel art showcase. Whether you're experimenting with visuals, developing new integrations, or just having fun, Pixoo-64-Tools makes it easy to unlock the full potential of your device.

## [Purchase a Pixoo 64 from Divoom here.](https://collabs.shop/1eue7d)
[![divoompixoo64 2](https://github.com/user-attachments/assets/d54e03ac-10aa-4415-b33d-0af6850f4866)
](https://collabs.shop/1eue7d)

[![image](https://github.com/user-attachments/assets/9d642211-f854-4fee-93e8-3bcc83fe8803)
](https://collabs.shop/1eue7d)
# **📌 Requirements**

Before using these scripts, ensure you have the following dependencies installed:

- **[Pixoo](https://github.com/SomethingWithComputers/pixoo)** – A library to help you make the most out of your Pixoo 64
- **Pillow** – For image processing
- **ScreenInfo** – For screen size detection

Install the required dependencies using pip:

`pip install pillow pixoo screeninfo`

# 🚀 **Usage**

- Find Your Pixoo 64's IP Address
  - Open the Divoom app
  - Navigate to Device Settings
  - Locate and copy the IP address
- Run a Script
  - Replace the placeholder IP address in the script with your Pixoo 64’s IP
  - Execute the script using Python

# **Available Scripts**

🖥️ **Screen Streaming GUI**

`python StreamGUI.py`
- A Python-based GUI that captures your screen and streams it as a 64×64 display. Features:
  - Start/stop functionality
  - Live image preview

🔤 **Send Text**

`python SendText.py`
- A simple test script to send a line of text to the Pixoo 64 display.

📸 **Send Screenshot**

`python SendScreenshot.py`
- Captures a screenshot of your screen and sends it to the display.
