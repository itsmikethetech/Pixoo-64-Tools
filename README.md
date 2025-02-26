# Pixoo 64 Tools by MikeTheTech

Pixoo-64-Tools is a collection of Python scripts designed to interact with the Pixoo 64, a 64×64 pixel LED display from Divoom. These tools allow you to stream your screen, send text messages, and display screenshots on the Pixoo 64 with ease.

With a simple setup and an intuitive interface, you can transform your Pixoo 64 into a live screen mirroring display, a custom message board, or a real-time pixel art showcase. Whether you're experimenting with visuals, developing new integrations, or just having fun, Pixoo-64-Tools makes it easy to unlock the full potential of your device.

## [Purchase a Pixoo 64 from Divoom here.](https://collabs.shop/1eue7d)
[![divoompixoo64 2](https://github.com/user-attachments/assets/d54e03ac-10aa-4415-b33d-0af6850f4866)
](https://collabs.shop/1eue7d)

[![image](https://github.com/user-attachments/assets/9d642211-f854-4fee-93e8-3bcc83fe8803)
](https://collabs.shop/1eue7d)

<img src="https://github.com/user-attachments/assets/b3493a02-860f-4666-aad9-1ab2d4a5b141" width="49%"></img>
<img src="https://github.com/user-attachments/assets/c5d1f93f-a5ec-4f42-a865-8edddb2085c0" width="49%"></img>


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

## Pixoo Variables/Parameters.

These are the currently supported REST calls, and can be made with both POST and GET calls. 

| Pixoo equivalent          | URL and variables                                                                                                                |
|---------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| clear                     | `/clear/<int:r>/<int:g>/<int:b>`                                                                                                 |
| draw_character            | `/drawcharacter/<string:character>/<int:x>/<int:y>/<int:r>/<int:g>/<int:b>`                                                      |
| draw_filled_rectangle     | `/drawfilledrectangle/<int:top_left_x>/<int:top_left_y>/<int:bottom_right_x>/<int:bottom_right_y>/<int:r>/<int:g>/<int:b>`       |
| draw_line                 | `/drawline/<int:start_x>/<int:start_y>/<int:stop_x>/<int:stop_y>/<int:r>/<int:g>/<int:b>`                                        |
| draw_pixel_at_index       | `/drawpixel/<int:index>/<int:r>/<int:g>/<int:b>`                                                                                 |
| draw_pixel_at_location    | `/drawpixel/<int:x>/<int:y>/<int:r>/<int:g>/<int:b>`                                                                             |
| draw_text_at_location     | `/drawtext/<string:text>/<int:x>/<int:y>/<int:r>/<int:g>/<int:b>`                                                                |
| device_configuration      | `/deviceconfigurations`                                                                                                          |
| device_time               | `/devicetime`                                                                                                                    |
| fill                      | `/fill/<int:r>/<int:g>/<int:b>`                                                                                                  |
| play_local_gif            | `/playlocalgif/<path:file_path>`                                                                                                 |
| play_local_gif_directory  | `/playlocalgifdirectory/<path:path>`                                                                                             |
| play_gif_file_url         | `/playnetgif/<path:gif_file_url>`                                                                                                |
| push                      | `/push`                                                                                                                          |
| reboot                    | `/reboot`                                                                                                                        |
| send_text_at_location_rgb | `/sendtext/<int:x>/<int:y>/<int:r>/<int:g>/<int:b>/<int:identifier>/<int:font>/<int:width>/<int:movement_speed>/<int:direction>` |
| set_brightness            | `/setbrightness/<int:brightness>`                                                                                                |
| set_channel               | `/setchannel/<int:channel>`                                                                                                      |
| set_clock                 | `/setclock/<int:clock_id>`                                                                                                       |
| set_face                  | `/setface/<int:face_id>`                                                                                                         |
| set_high_light_mode       | `/sethighlight/<int:on>`                                                                                                         |
| set_mirror_mode           | `/setmirror/<int:on>`                                                                                                            |
| set_noise_status          | `/setnoise/<int:on>`                                                                                                             |
| set_score_board           | `/setscoreboard/<int:blue_score>/<int:red_score>`                                                                                |
| set_screen                | `/setscreen/<int:on>`                                                                                                            |
| set_visualizer            | `/setvisualizer/<int:equalizer_position>`                                                                                        |
| set_white_balance_rgb     | `/setwhitebalance/<int:white_balance_r>/<int:white_balance_g>/<int:white_balance_b>`                                             |
| sound_buzzer              | `/soundbuzzer/<int:active_cycle_time>/<int:inactive_cycle_time>/<int:total_time>`                                                |
