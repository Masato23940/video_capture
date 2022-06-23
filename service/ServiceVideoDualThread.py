# from concurrent.futures import thread
import sys
sys.path.append('../')
import threading
import time
import cv2
import datetime
# from controller.video_capture import Camera
from ServiceVideoTripleThread import *

class ServiceVideoDualThread(ServiceVideo):
  def __init__(self):
      super().__init__()

  def start(self):  
    thread_video = threading.Thread(target=self.run)
    thread_video.start()

  def stop(self):
    self.isRecording = False
    self.camera.close()


if __name__ == '__main__':
  video = ServiceVideoDualThread()
  video.start()
  time.sleep(10)
  video.stop()
#   video.serve(10)
  print('simulation done')

