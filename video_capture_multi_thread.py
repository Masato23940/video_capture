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
        path = "../Videos/Capture_Video/" + date + ".mp4"
    
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
        
class Button():
    def __init__(self):
        self.PIN = 5
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.toggle = False
        self.button_has_pushed = False
            
    def isButtonPushed(self):
        return not GPIO.input(self.PIN) # pushed True / unpushed False
    
    def buttonPushedEvent(self):
        while True:
            if self.isButtonPushed() and not self.button_has_pushed:                
                self.toggle = not self.toggle
                self.button_has_pushed = True
                
            elif not self.isButtonPushed() and self.button_has_pushed:
                self.button_has_pushed = False

if __name__ == '__main__':
    button = Button()
    camera = Camera()

    thread_button = threading.Thread(target=button.buttonPushedEvent)
    thread_button.start()
    while True:
        try:
            if button.toggle == True and not camera.isActivated:
                camera.start()
            elif button.toggle == True and camera.isActivated:
                camera.capture()
                print("{}".format(button.toggle))
            elif button.toggle == False and camera.isActivated:
                camera.stop()
            #print("{}".format(button.toggle))
                
        except KeyboardInterrupt:
            camera.stop()
            camera.close()
