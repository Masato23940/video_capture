import RPi.GPIO as GPIO
import threading
import time
import cv2
import datetime

class Camera():
    def __init__(self):
        self.isActivated = False
        self.DEV_ID = 0
        self.WIDTH = 640
        self.HEIGHT = 480
        self.FPS = 30
        self.SLEEP_TIME = 1/self.FPS;
        self.RECODING_TIME_MAX = 10;
                
        
    def set_capture_params(self):
        self.cap = cv2.VideoCapture(self.DEV_ID)
        # set parameter
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, self.FPS)
        
    def prepare_codec(self):
        # file name
        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        path = "../../Videos/Capture_Video/" + date + ".mp4"
    
        # video parameters for codec 
        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        self.out = cv2.VideoWriter(path, fourcc, self.FPS, (self.WIDTH, self.HEIGHT))
        
    def start(self):
        self.isActivated = True
        self.set_capture_params()
        self.prepare_codec()
        #while True
        #    ret, frame = self.cap.read()
        #    self.out.write(frame)
            
    def capture(self):
        ret, frame = self.cap.read()
        self.out.write(frame)
        
    def stop(self):
        self.isActivated = False
        self.close()
        
    def close(self):
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()
        print("closed")
        
    def capture_CPT_for(self,REC_SEC):
        self.start()
        for _ in range(self.FPS * REC_SEC):
            self.capture()
        self.stop()
    
    def capture_CPT_while(self,REC_SEC):
        start_time = time.time()
        while True:
            if  time.time()-start_time > REC_SEC:
                break
            elif camera.isActivated:
                camera.capture()
            else:
                camera.start()
        camera.stop()
            
        
if __name__ == '__main__':
    camera = Camera()
    #camera.capture_CPT_for(10)
    camera.capture_CPT_while(10)

