# Final Project

Using the tools and techniques you learned in this class, design, prototype and test an interactive device.

Project Github page set up - May 3

Functional check-off - May 10
 
Final Project Presentations (video watch party) - May 12

Final Project Documentation due - May 19

 
## Description
For this project, I built a security camera to understand my cat Bella's eating schedule. The camera is placed in front of Bella's bowl and it sends an image/video clip via text message to my phone when it detects Bella. The system allows me to have a better understanding of Bella's eating habbit especially when I'm not at home. It can also detect intruders (in my case, a dog) and send a photo of the intruder to my phone. When it detects an intruder, the system plays a pre-recorded audio: " No! Bad boy!"

## The Process

I used AWS S3 to store recorded videos/images and Twilio to send the stored videos/images to my phone via text messages.

Security Camera V 1.0 can only detect my cat Bella. The system starts counting when my cat is in the scene. It sends a 2 seconds video to my phone if the cat stays in the scene for 2 seconds.

Security Camera V 2.0 can protect Bella's food. It detects my dog Martin as an intruder and sends a message to my phone. It also plays a pre-recorded audio "No! Bad boy!"

Here are some of the issues I found:
1. The detection accuracy is not great. My dog and my cat can be misdetected very often. When my cat is detected as both as a dog and as a cat in continuous frames, I will receive multiple messages. Here is a video showing a failure example: https://youtu.be/voapi1MoN7Y
2. If Bella sits in front of the camera for the entire afternoon, my phone will explode (because the system will keep sending me videos).


1. Documentation of design process
2. Archive of all code, design patterns, etc. used in the final design. (As with labs, the standard should be that the documentation would allow you to recreate your project if you woke up with amnesia.)
3. Video of someone using your project (or as safe a version of that as can be managed given social distancing)
4. Reflections on process (What have you learned or wish you knew at the start?)

## Examples

[Here is a list of good final projects from previous classes.](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/wiki/Previous-Final-Projects)
This version of the class is very different, but it may be useful to see these.
