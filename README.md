<p align="center">
	<a href="https://github.com/lboroWMEME-TeamProject/CCC-ProjectDocs"><img src="https://i.imgur.com/VwT4NrJ.png" width=650></a>
	<p align="center"> This repository is part of  a collection for the 21WSD001 Team Project. 
	All other repositories can be access below using the buttons</p>
</p>

<p align="center">
	<a href="https://github.com/lboroWMEME-TeamProject/CCC-ProjectDocs"><img src="https://i.imgur.com/rBaZyub.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Dashboard"><img src="https://i.imgur.com/fz7rgd9.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Cloud-Server"><img src="https://i.imgur.com/bsimXcV.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Drone-Firmware"><img src="https://i.imgur.com/yKFokIL.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Simulated-Drone"><img src="https://i.imgur.com/WMOZbrf.png" alt="drawing" height = 33/></a>
</p>

------------
# Ai-Cam

This repo contains the code base for setting up and deploying the Ai-Camera Subsystem. It takes an image from the webcam and runs it through a pretrained deep neural net to identify specific objects in the frame.

This repo comes with, and uses the YOLOv4-Tiny training model due to its accurate and quick detection for identifying people. However, if you need to change the model or want to use your own, simple add the `.weights` and `.cfg` files to the `detection models\` directory and update the detection model with in `main.py`.

`main.py` :
```
from ai_cam import ai_cam
from threading import Thread	

CAMID = 0 			                                # The Cam ID, usually 0, but if you have many cams attached it may change
CAM_HEIGHT = 360	                                # The height of the camera frame, higher you go, slower performance (don't change unless needed)
CAM_WIDTH = 640		                                # The width of the camera frame, higher you go, slower performance (don't change unless needed)
CAM_FPS = 15
WEIGHTS = "<CHANGE ME>"                             # Files path to the detection model weights
CFG = "<CHANGE ME>"                                 # Files path to the detection model configuration
COCO= "detection models/coco.names"                 # Files path to the COCO name data set
PI_URL = "http://192.168.0.5:12345"                 # The server URL the Pi is running on

```

------------

## Table of Contents

- [Subsystem Overview](#Subsystem-Overview)
- [Code Overview](#Code-Overview)
- [Installation](#Installation)
- [Deployment](#Deployment)

------------

## Subsystem Overview

This subsystem is composed of a USB camera and a Raspberry Pi 4, originally it was meant to use a Nvidia Jetson Nano which allows for CUDA however due to the global chip shortage it was unable to be procured. The AI detection code however is flexible and will work on both CPU processing and CUDA processing is available.

**Subsystem Diagram :**

<p align="center">
	<img src="https://i.imgur.com/ZnWuAav.jpg" alt="drawing"/>
</p>

The camera is connected via USB to the Pi 4 (or whatever neural processor you have). You can also use the camera ribbon connector if a USB cam is unavailable. Once all the processing has been done that frame data is sent to the Main Pi using a TCP socket over the ethernet ports. The Main Pi must be running a socket server for the data to be received.

------------

## Code Overview

The code is split into 4 major classes with each instantiated inside each other like a Matryoshka doll.

`main.py` - The main file that is run, sets up the configuration variable and creates the required objects for the subsystem to function.

`ai_cam.py` - The Wrapper class that contains the camera object as will as the code to handle communication between the two Raspberry Pi's

`webcam.py` - Contains the Webcam class that has all the logic for connecting to the attached webcam and getting the feed from the camera. It also contains the AI detector object.

`ai_detect.py` - Contains the detector class that allows you to run a frame through OpenCV's Deep Neural Net using a pretrained model.

------------

## Installation

**Step 0** : Setup a Raspberry Pi/Jetson Nano/Other Neural Processor with linux.

**Step 1** : Clone the repo to the target device, If you have git installed you can do so by running the following.

```
git clone https://github.com/lboroWMEME-TeamProject/ai-cam.git
```

**Step 3** : Install the Python dependencies using pip.

```
pip install -r requirements.txt
```

**Step 4** : Edit the configuration variables in `main.py` to match your setup.

`main.py` :
```
CAMID = 0 			                                # The Cam ID, usually 0, but if you have many cams attached it may change
CAM_HEIGHT = 360	                                # The height of the camera frame, higher you go, slower performance (don't change unless needed)
CAM_WIDTH = 640		                                # The width of the camera frame, higher you go, slower performance (don't change unless needed)
CAM_FPS = 15
WEIGHTS = "detection models/yolov4-tiny.weights"    # Files path to the detection model weights
CFG = "detection models/yolov4-tiny.cfg"            # Files path to the detection model configuration
COCO= "detection models/coco.names"                 # Files path to the COCO name data set
PI_URL = "URL of Sockets Server"                 # The server URL the Pi is running on
```

**Step 5** : Run `main.py` and you will see data being collected and sent to the other Raspberry Pi

------------

## Deployment

Once you have the code installed and setup, you can deploy the package as a systemd service that auto starts up at boot. An example `.service` file is included in the project repo, you can use that or tweak the values to match your specific setup.

`aicam.service` :

```
[Unit]
Description=Auto Start AI-Cam Server
After=network.target

[Service]
User=<User To Run App>
Group=<User Group>
WorkingDirectory=<Path to Working Directory>
ExecStart=python3 main.py

[Install]
WantedBy=multi-user.target
```

Once you have setup your `.service` file you need to enable it on the system by first copying the file to the systemd service location.

You can do so by executing the following command

```
sudo cp aicam.service /etc/systemd/system
```

Then you need to activate the service,

```
sudo systemctl enable aicam.service
```

Then you can start the service

```
sudo systemctl start aicam.service
```

Now on boot after the device has an internet connection the detection will automatically start.

------------