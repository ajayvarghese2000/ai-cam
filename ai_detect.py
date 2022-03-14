# A class that will take a frame from a cv2 video capture and run it through a trained
# neural network to detect objects from the coco training list
#
#   Written by Team CCC
#

## [Imports]
import cv2          # Used to detect objects
import numpy as np  # Used for fast math operations over arrays 

# Main Class
#   Functions:
#       Constructor - Loads the detection weights and creates the dnn object
#       detect      - Takes the input frame and runs it through the DNN
class detector:

    # The constructor function, sets up the cv2 neural network
    #       Takes in file paths to the weights, configuration files and the coco dataset
    #       returns nothing
    def __init__(self, WEIGHTS, CFG, COCO):
        # Load the weights using cv2's deep neural network
        self.net = cv2.dnn.readNet(WEIGHTS, CFG)

        # Reading the Coco training set names
        self.classes = []
        with open(COCO, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        # Getting the names and processing layers from the YOLO weights model
        self.layer_names = self.net.getLayerNames()
        try:

            # For CPU versions of openCV
            self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        except:

            # For CUDA versions of openCV
            self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # Creating colors for the detection boxes to use
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

        return

    # The detection function, runs a cv2 frame through the network to detect objects
    #       Takes in a cv2 frame
    #       returns a cv2 frame with labels and boxes drawn for objects 
    #       and a boolean for if there was a person detected.
    def detect(self, img):

        # Getting the height and width of the frame
        height, width, channels = img.shape

        # Preprocessing the frame so it can be passed into neural net
        blob = cv2.dnn.blobFromImage(img, 0.00392, (320, 320), (0, 0, 0), True, crop=False)

        # Sending the processed frame to the neural net
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        # Stores the ids of the objects detected, will be used to get names from coco list
        class_ids = []
        
        # Stores the confidences of the detected objects
        confidences = []
        
        # Store cordinates for the objects detected
        boxes = []

        # Generating the cordinates for the boxes to draw around the detected objects
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Only add the object if it is above a certian confidence level
                if confidence > 0.3:
                    
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.2)

        # Setting the font for the names
        font = cv2.FONT_HERSHEY_PLAIN

        # Default case is that there is no person in the frame to begin with
        person = False

        # Adding the boxes to the cv2 frame
        for i in range(len(boxes)):
            if i in indexes:
                
                # Getting the coordinates for the current object
                x, y, w, h = boxes[i]

                # Setting the label and setting the colour
                label = str(self.classes[class_ids[i]])
                
                # Checking if a person box was added
                if(label.lower() == 'person'):

                    # Updating the value if a person was found
                    person = True
                
                # Setting the colour for the box
                color = self.colors[i]

                # Drawing the rectangle onto the frame
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

                # Drawing the label onto the frame
                cv2.putText(img, label, (x, y - 10), font, 3, color, 2)
        
        # Returning the new frame and person value back to the cam
        return img, person