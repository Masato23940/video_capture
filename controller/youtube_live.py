import RPi.GPIO as GPIO
import threading
import time
import datetime
import threading
import shlex
import subprocess
import os
import signal

class YouTubeLive():
    def __init__(self):
        self.isLiving = False
        self.DEV_ID = 0
        self.WIDTH = 640
        self.HEIGHT = 480
        self.FPS = 30
        self.cmd = 'Live_v2'
        self.script_path = '/home/pi/Documents/Live/Live_v2.sh'
        
    def start(self):
        self.isRecording = True
        tokens = shlex.split(self.cmd)
        self.proc = subprocess.Popen(['sh', self.script_path], stdout=subprocess.PIPE)
#              
    def stop(self):
#         self.proc.taskkill()
        self.proc.terminate()
#         os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
#     def close(self):
#         
        
if __name__ == '__main__':
    live = YouTubeLive()
    #camera.capture_CPT_for(10)
    live.start()
    time.sleep(20)
    live.stop()


