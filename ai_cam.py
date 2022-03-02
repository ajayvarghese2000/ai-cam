from webcam import camera
import serial

class ai_cam:
    def __init__(self,CAMID, WIDTH, HEIGHT, FPS, WEIGHTS, CFG, COCO):

        # Creating the camera object with the supplied variables
        self._CAM = camera(CAMID, WIDTH, HEIGHT, FPS, WEIGHTS, CFG, COCO)

        self._serialport = serial.Serial("/dev/ttyS0", 9600, timeout=1)
        self._serialport.flush()
        return
    def get_frame_serial(self):
        frame, person = self._CAM.getFrame()
        self._serialport.write(str.encode(frame + '\n'))
        return


CAMID = 0 			                                # The Cam ID, usually 0, but if you have many cams attached it may change
CAM_HEIGHT = 360	                                # The height of the camera frame, higher you go, slower performance (don't change unless needed)
CAM_WIDTH = 640		                                # The width of the camera frame, higher you go, slower performance (don't change unless needed)
FPS = 15                                            # The FPS to try and capture at
WEIGHTS = "detection models/yolov4-tiny.weights"    # Files path to the detection model weights
CFG = "detection models/yolov4-tiny.cfg"            # Files path to the detection model configuration
COCO= "detection models/coco.names"                 # Files path to the COCO name data set

cam = ai_cam(CAMID, CAM_WIDTH, CAM_HEIGHT, FPS, WEIGHTS, CFG, COCO)

while 1:
    cam.get_frame_serial()