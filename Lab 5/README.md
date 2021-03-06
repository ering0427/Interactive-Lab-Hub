# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

In Lab 5 part 1, we focus on detecting and sense-making.

In Lab 5 part 2, we'll incorporate interactive responses.


## Prep

1.  Pull the new Github Repo.
2.  Read about [OpenCV](https://opencv.org/about/).
3.  Read Belloti, et al's [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf)

### For the lab, you will need:

1. Raspberry Pi
1. Raspberry Pi Camera (2.1)
1. Microphone (if you want speech or sound input)
1. Webcam (if you want to be able to locate the camera more flexibly than the Pi Camera)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.


## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

Befor you get started connect the RaspberryPi Camera V2. [The Pi hut has a great explanation on how to do that](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera).  

#### OpenCV
A more traditional to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python.

Additionally, we also included 4 standard OpenCV examples. These examples include contour(blob) detection, face detection with the ``Haarcascade``, flow detection(a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (I.e. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example.

```shell
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```
#### Filtering, FFTs, and Time Series data.
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the set up from the [Lab 3 demo](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Spring2021/Lab%203/demo) and the accelerometer, try the following:

**1. Set up threshold detection** 

The threshold is set to 2 for all axes.

**2. Set up averaging** 

The signal is averaged in 10-sample blocks.

**3. Set up peak detection** 

[Code here](https://github.com/ering0427/Interactive-Lab-Hub/tree/Spring2021/Lab%205/demo)

#### Teachable Machines (beta, optional)
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple.  However, its simplicity is very useful for experimenting with the capabilities of this technology.

You can train a Model on your browser, experiment with its performance, and then port it to the Raspberry Pi to do even its task on the device.

Here is Adafruit's directions on using Raspberry Pi and the Pi camera with Teachable Machines:

1. [Setup](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/raspberry-pi-setup)
2. Install Tensorflow: Like [this](https://learn.adafruit.com/running-tensorflow-lite-on-the-raspberry-pi-4/tensorflow-lite-2-setup), but use this [pre-built binary](https://github.com/bitsy-ai/tensorflow-arm-bin/) [the file](https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl) for Tensorflow, it will speed things up a lot.
3. [Collect data and train models using the PiCam](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/training)
4. [Export and run trained models on the Pi](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/transferring-to-the-pi)

Alternative less steps option is [here](https://github.com/FAR-Lab/TensorflowonThePi).

#### PyTorch  
As a note, the global Python install contains also a PyTorch installation. That can be experimented with as well if you are so inclined.

### Part B
### Construct a simple interaction.

**Describe and detail the interaction, as well as your experimentation.**

I used the object detection model to detect my dog Martin and my cat Bella. The model is able to detect 90 classes of objects and when it detects a dog, it draws a purple rectangle around the dog and prints the text "dog". When it detects a cat, it draws a green rectangle around the cat and prints the text "cat". The model does not print on the screen for other objects detected.

This system is developed to make sure that my dog does not steal my cat's food. Ideally the camera will be placed in front of my cat's bowl and will "beep" when it detects my dog Martin to keep him away :)

Here are two screenshots of the successful examples:
![plot](cat_detected.png)
![plot](dog_detected.png)

### Part C
### Test the interaction prototype

**note your observations**:

The system works well when there's ambient light and the animal's whole body is in the scene. It fails when the environment is dark and when the animal is partially in the scene. The system can detect my cat pretty well but fails several times for my dog. See examples below.

Martin is detected as a cat when he is partially in the scene:
![plot](dog_detected_as_cat.png)

Martin is detected both as a dog and as a cat when he is partially in the scene and is not facing the camera:
![plot](failed_example.png)

The system may also fail when the animal is partially occluded by objects (e.g. a bowl). 

**Think about someone using the system. Describe how you think this will work.**

It will be very bad if my cat is accidentally detected as a dog (although not very likely) and the system beeps her away. In the case where my dog is detected as a cat, he will eat all of my cat's food. To make my system better detect and classify my dog and my cat, I will put the camera near a good light source and adjust the detection confidence level.

### Part D
### Characterize your own Observant system

**characterize their behavior**.

**Include a short video demonstrating the answers to these questions.**

* The system can be used to prevent my dog from eating my cat's food (after adding other modalities). It can also be used to prevent my pets from getting close to dangerous objects such as stove tops and electrical outlets.
* A good environment for the system should have ambient light. The placement of the camera can largely affect the detection result. So the camera should be placed slightly higher than the pet but not too high so that it can detect the whole body of the animal.
* The system is good for detecting cats. 
* It doesn't work as well for dogs that of similar sizes as cats. Plush toys can also be misclassified as animals and they should be avoided in the scene.
![plot](plush_toys.png)

The setup is here:
![plot](Lab5_setup.jpg)


Here's a video showing cat detection:
https://youtu.be/oCCLB-fc9Sc

And dog detection:
https://youtu.be/erWvOf7L32U

## Part 2.

**Include a short video demonstrating the finished result.**

In Part 2, I added sound to the system. The Pi is connected to a bluetooth speaker placed near the bowl. It makes a sound when the camera detects a dog. I didn't make the sound loud enough so that Martin won't be scared away :)

![plot](Lab5_part2.jpg)

The video is here:
https://youtu.be/vhFsw3b8faE

The video is slightly slower than the audio.
