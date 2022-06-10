import cv2
from datetime import datetime

#/ dev/video0
DEV_ID = 0

# vodeo param
WIDTH = 640
HEIGHT = 480
FPS = 30

# capture time [s] 
REC_SEC = 5

def main():
    # specify camera
    cap = cv2.VideoCapture(DEV_ID)

    # set parameter
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    
    # file name
    date = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = "../Videos/Capture_Video/" + date + ".mp4"
    
    # video parameters for codec 
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter(path, fourcc, FPS, (WIDTH, HEIGHT))
    
    # capture
    for _ in range(FPS * REC_SEC):
        ret, frame = cap.read()
        out.write(frame)
    
    #release
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return

if __name__=="__main__":
    main()