# A class to get a frame from a webcam and convert it into a format that can be used with GUI's
#
#   Written by Team CCC
#

## [Imports]
import cv2                      # Used to get the webcam feed
import base64                   # Used to convert the webcam frame into a base64 string
from ai_detect import detector  # Used to run the frame generated through the neural net

## Main Class
#   Functions:
#       Constructor - Initialises the camera from the camID the user supplies, sets cam height, width
#                     and fps.
#       getFrame    - Gets the current frame from the camera that is selected. Converts it into an base64
#                     string and returns is
#       Destructor  - Makes sure the camera that was used is properly released so other apps can use it
#   Variables:
#       cam         - holds the cv2 camera object
#       width       - width of the cam
#       height      - height of the cam
#       fps         - fps of the cam
class camera:
    
    # Gets the current frame from the selected camera
    #   Takes no inputs
    #   Returns a frame if successfully found or an error if it failed
    #   a thermal fake of the frame
    #   and if a person was found
    def getFrame(self):

        # Reads a frame, returns a  bool if it was successful
        success, frame = self.cam.read()

        # Checks if we successfully got a frame
        if not success:

            # Raises an error if the program can not get a frame
            raise IOError("Can not get Frame") 
        else:

            # Takes the frame given then runs it through the detection
            frame, person = self.detector.detect(frame)

            # Encodes the frame into a jpeg format
            retval, frame = cv2.imencode('.jpeg', frame)

            # Converts the jpeg to a base64 string
            frame = base64.b64encode(frame)
            frame = frame.decode("utf-8")


            # Returns the converted frame
            return frame, person
    
    # The constructor function, sets up the camera to get frames from
    #   Takes in, the ID, width and fps of the camera
    #   returns nothing - will raise an error if the camera failed to open
    def __init__(self,camID, width, height, fps, WEIGHTS, CFG, COCO):

        # Uses cv2 to capture the camera using DirectShow
        self.cam = cv2.VideoCapture(camID)

        # Checks if the cam can be opened, if not it errors out
        if not self.cam.isOpened():
            raise IOError("Can not open webcam") 

        # sets the camera parameters for both the class and the cv2 object
        self.width = width
        self.height = width
        self.fps = fps
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cam.set(cv2.CAP_PROP_FPS, fps)

        # Creating the detection object so frames can be passed through
        self.detector = detector(WEIGHTS, CFG, COCO)
        
        return

    # Destructor Function, cleans up the the variables
    #   takes no input
    #   returns nothing
    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()
        return