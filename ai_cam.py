# A wrapper class that handles the comunication to other PI's and the
# control of the attached camera 
#
#   Written by Team CCC
#

## [Imports]
from time import sleep      # Used to make sure the connection is connected
from webcam import camera   # The code to control the camera that is attached
import socketio             # Used to handel TCP data transfer from Pi to Pi

# Main Class
#   Functions:
#       Constructor - Sets up the camera object with the values passed in
#       Destructor  - Disconects from the Pi server and closes the camera
#       sendframe   - Sends a frame from the camera to the Pi
class ai_cam:
    def __init__(self, CAMID, WIDTH, HEIGHT, FPS, WEIGHTS, CFG, COCO, PI_URL):

        # Creating the camera object with the supplied variables
        self._CAM = camera(CAMID, WIDTH, HEIGHT, FPS, WEIGHTS, CFG, COCO)

        # Creaking the websocket client
        self._SOCK = socketio.Client(logger=False, engineio_logger=False)

        # Starts the Connection to the other PI
        self._PI_URL = PI_URL
        self.connect(self._PI_URL)
        
        # Once a connection has been made start sending video feed
        while(self._SOCK.connected == True):
            self.sendframe()
        
        # If connection dropped after sending frame attempt to reconnect
        if(self._SOCK.connected != True):
            self.connect(self._PI_URL)
        
        return

    # Connects to the Main Pi server from the supplied URL
    def connect(self, PI_URL):
        
        # Attempts to connect to server forever until a connection has been made
        while(self._SOCK.connected != True):

            # Tries to connect to the server
            try:
                self._SOCK.connect(PI_URL, socketio_path="/socket.io/")

            # Sleeps for 5 secons if a connection failed
            except:
                sleep(5)

    # Gets a frame from the AI camera and packages it in the correct format to 
    # send to the main PI.
    def sendframe(self):
        
        # Gets the latest frame from the AI cam
        frame, person = self._CAM.getFrame()
        
        # Packing the data
        payload = {"frame" : frame, "person" : person}
        
        # Attempting to send to the server under the 'cam' message tag
        try:
            self._SOCK.emit("cam", payload)

        # Check if it got disconnected midsend and attempt a reconnection
        except:
            if(self._SOCK.connected != True):
                self.connect(self._PI_URL)
        
        return
    
    # Destructor function to clean up applications on close
    def __del__(self):
        self._SOCK.disconnect()
        self._CAM.__del__()
