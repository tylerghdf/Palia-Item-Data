import time
import os
import pygetwindow as pgw
from PIL import Image, ImageGrab
from pynput.keyboard import Key, Listener

# Title of the window you want to try to capture
title = 'Discord'

# Where you want your screenshots to be saved
output_path = 'screenshots'

# How frequent the screenshots are taken
screenshot_interval = 1

# Key to toggle recording
recording_hotkey = 'g'

recording = False
current_recording = None

# Probably not necessary for this to be a function, but may help in future
def take_screenshot(left, top, right, bottom):
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

    return screenshot

def on_press(key):
    global recording
    global current_recording
    
    try:
        if key.char == recording_hotkey and not recording:
            #Grouping each series of screenshots into a 'recording'
            current_recording = f'{output_path}/{round(time.time())}'
            os.mkdir(current_recording)
            
            recording = True
            print('Recording started')
        elif key.char == recording_hotkey:
            recording = False
            print('Recording stopped')
    except:
        pass

if __name__ == '__main__':
    # pynput listener is a thread
    listener = Listener(on_press=on_press)
    listener.start()

    if not os.path.exists(output_path):
        print('Creating output path')
        os.mkdir(output_path)
    
    while True:
        try:
            window = pgw.getWindowsWithTitle(title)[0]

            if not window.isMinimized and recording:
                left, top = window.topleft
                right, bottom = window.bottomright

                screenshot = take_screenshot(left, top, right, bottom)
                screenshot.save(f'{current_recording}/{round(time.time())}.jpg')
        except IndexError:
            print(f'Program "{title}" is not currently running!')
        except Exception as exception:
            print(exception)

        time.sleep(screenshot_interval)
