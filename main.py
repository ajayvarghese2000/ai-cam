from ai_cam import ai_cam
from threading import Thread	

CAMID = 0 			                                # The Cam ID, usually 0, but if you have many cams attached it may change
CAM_HEIGHT = 360	                                # The height of the camera frame, higher you go, slower performance (don't change unless needed)
CAM_WIDTH = 640		                                # The width of the camera frame, higher you go, slower performance (don't change unless needed)
CAM_FPS = 15
WEIGHTS = "detection models/yolov4-tiny.weights"    # Files path to the detection model weights
CFG = "detection models/yolov4-tiny.cfg"            # Files path to the detection model configuration
COCO= "detection models/coco.names"                 # Files path to the COCO name data set
PI_URL = "http://192.168.0.5:12345"                 # The server URL the Pi is running on

# Creating a new thread to start the Camera on
thread1 = Thread(target=ai_cam, args=(CAMID, CAM_HEIGHT, CAM_WIDTH, CAM_FPS, WEIGHTS, CFG, COCO, PI_URL))
thread1.start()
