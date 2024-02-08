import time
import os
import cv2
import keyboard
import numpy as np
import pygetwindow as pgw
from PIL import ImageGrab

window_title = 'Palia' # Program window title
output_path = 'recordings' # Output directory
screenshot_interval = 1 # Screen capture rate

video_writer = None
recording = False

def new_video_writer():
    global video_writer

    # Modify these for changes to video output
    output_file_path = f'{output_path}/{round(time.time())}.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    fps = 10
    size = (1920, 1080)
    video_writer = cv2.VideoWriter(output_file_path, fourcc, fps, size) 

def toggle_recording():
    global recording, video_writer

    if not recording:
        print('Recording started')
        
        recording = True
        
        new_video_writer()  
    else:
        print('Recording stopped')
        
        recording = False
        
        if video_writer:
            video_writer.release()

if __name__ == '__main__':
    keyboard.add_hotkey('-', toggle_recording)

    if not os.path.exists:
        os.mkdir(output_path)
    
    while True:
        # Try block is for cases where there's no windows with the given title
        try:
            window = pgw.getWindowsWithTitle(window_title)[0]

            if not window.isMinimized and recording:
                screenshot = ImageGrab.grab()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                video_writer.write(frame)
        except IndexError:
            print(f'Program "{window_title}" is not currently running!')
        except Exception as e:
            print(e)

        time.sleep(screenshot_interval)

#Cleanup
if video_writer:
    video_writer.release()
