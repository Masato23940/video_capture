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
        self.cmd = "./Live_v2.sh"
        
    def start(self):
        self.isRecording = True
#         self.proc = subprocess.Popen("exec " + self.cmd, shell=True)
        self.proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        
    def stop(self):
#         self.proc.kill()
        os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        
if __name__ == '__main__':
    live = YouTubeLive()
    live.start()
    time.sleep(20)
    live.stop()
    exit()


