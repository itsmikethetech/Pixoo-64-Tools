## Pixoo-64-Tools

![image](https://github.com/user-attachments/assets/9d642211-f854-4fee-93e8-3bcc83fe8803)

# **📌 Requirements**

Before using these scripts, ensure you have the following dependencies installed:

- Pixoo – A library to help you make the most out of your Pixoo 64
- Pillow – For image processing
- ScreenInfo – For screen size detection

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

`python StreamGUI.py`
- A Python GUI that captures your screen and sends it as a 64x64 stream to the display. Includes start, stop, and image preview.

`SendText.py`
- A test script that sends a line of text to the display.

`python SendScreenshot.py`
- A test script that takes a screenshot and sends it to the display.
