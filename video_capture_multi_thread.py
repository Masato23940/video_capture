import RPi.GPIO as GPIO
import threading
import time
import cv2
import datetime
from video_capture import Camera
        
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
            camera.close()
            break
