# How to load a Tensorflow model using OpenCV
# Jean Vitor de Paulo Blog - https://jeanvitor.com/tensorflow-object-detecion-opencv/
# David edited some stuff
from __future__ import print_function
import numpy as np
import cv2
import sys
from pyimagesearch.notifications import TwilioNotifier
from pyimagesearch.utils import Conf
from imutils.video import VideoStream
from imutils.io import TempFile
from datetime import datetime
from datetime import date
import argparse
import imutils
import signal
import time
import pygame
pygame.mixer.init()
pygame.mixer.music.load("beep1.ogg")

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="Path to the input configuration file")
args = vars(ap.parse_args())

# load the configuration file and initialize the Twilio notifier
conf = Conf(args["conf"])
tn = TwilioNotifier(conf)

catAppear = False
notifSent = False
intruderFound = False

writer = None
W = None
H = None

# Load a model imported from Tensorflow
tensorflowNet = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

CLASSES = ["background", "person", "bicycle", "car", "motorcycle",
            "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
            "unknown", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
            "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "unknown", "backpack",
            "umbrella", "unknown", "unknown", "handbag", "tie", "suitcase", "frisbee", "skis",
            "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
            "surfboard", "tennis racket", "bottle", "unknown", "wine glass", "cup", "fork", "knife",
            "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
            "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "unknown", "dining table",
            "unknown", "unknown", "toilet", "unknown", "tv", "laptop", "mouse", "remote", "keyboard",
            "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "unknown",
            "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush" ]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
img = None
webCam = False
#if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
#   try:
#      print("I'll try to read your image");
#      img = cv2.imread(sys.argv[1])
#      if img is None:
#         print("Failed to load image file:", sys.argv[1])
#   except:
#      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
#else:

try:
  print("Trying to open the Webcam.")
  cap = cv2.VideoCapture(0)
  if cap is None or not cap.isOpened():
     raise("No camera")
  webCam = True
except:
  img = cv2.imread("../data/test.jpg")
  print("Using default image.")


while(True):
    if webCam:
        ret, img = cap.read()

    catPrevAppear = catAppear

    rows, cols, channels = img.shape

    # Use the given image as input, which needs to be blob(s).
    tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))

    # Runs a forward pass to compute the net output
    networkOutput = tensorflowNet.forward()

    # Loop on the outputs
    for detection in networkOutput[0,0]:
        score = float(detection[2])
        idx = int(detection[1])
        # if a dog is detected
        if CLASSES[idx]=='dog':
            if score > 0.2:
                left = detection[3] * cols
                top = detection[4] * rows
                right = detection[5] * cols
                bottom = detection[6] * rows
                cv2.imwrite('intruder.jpg',img)
                print("Intruder detected!")
                msg = "Intruder detected!"
                if not intruderFound:
                    intruderFound = True
                    tn.send(msg, 'intruder.jpg')
                #draw a red rectangle around detected objects
                cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), COLORS[idx], thickness=2)
                y = int(top) - 15 if int(top) - 15 > 15 else int(top) + 15
                cv2.putText(img, CLASSES[idx], (int(left), y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                pygame.mixer.music.play()

        elif CLASSES[idx] == 'cat':
            if score > 0.2:
                left = detection[3] * rows
                top = detection[4] * cols
                right = detection[5] * cols
                bottom = detection[6] * rows
                #draw a red rectangle around detected objects
                cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), COLORS[idx], thickness=2)
                y = int(top) - 15 if int(top) - 15 > 15 else int(top) + 15
                cv2.putText(img, CLASSES[idx], (int(left), y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                catAppear = True
                # if cat just appeared
                if catAppear and not catPrevAppear:
                    startTime = datetime.now()
                    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                    writer = cv2.VideoWriter('/home/pi/Interactive-Lab-Hub/Final_Project/object-detection/output.mp4', fourcc, 30, (cols, rows),True)
                    
                    print("Cat appeared!")
                # if cat previously appeared
                elif catPrevAppear:
                    timeDiff = (datetime.now() - startTime).seconds
                    # if cat appears for more than 20 seconds
                    if catAppear and timeDiff > 20:
                        if not notifSent:
                            msg = "Bella is still eating!"
                            writer.release()
                            writer = None
                            tn.send(msg, 'output.mp4')
                            notifSent = True
                            print("Bella is still eating!")
        
        else:
            # Bella left
            if catPrevAppear:
                catPrevAppear = False
                if notifSent:
                    notifSent = False
                else:
                    endTime = datetime.now()
                    totalSeconds = (endTime - startTime).seconds
                    dateAppeared = date.today().strftime("%A, %B %d %Y")
                    msg = "Bella ate her food on {} at {} for {} " \
					"seconds.".format(dateAppeared,
					startTime.strftime("%I:%M%p"), totalSeconds)
                    if writer is not None:
                        writer.release()
                    writer = None
                    tn.send(msg, 'output.mp4')
            
                        
                
         

    if webCam:
        if sys.argv[-1] == "noWindow":
           print("Finished a frame")
           cv2.imwrite('detected_out.jpg',img)
           continue
        cv2.imshow('detected (press q to quit)',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break
    if writer is not None:
        writer.write(img)

if writer is not None:
    writer.release()

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()


