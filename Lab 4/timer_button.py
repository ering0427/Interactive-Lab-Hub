import qwiic_button
import time
import board
import busio
import digitalio
import subprocess
from PIL import Image, ImageDraw, ImageFont
import adafruit_mpr121
import adafruit_rgb_display.st7789 as st7789
import webcolors


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000
# Setup SPI bus using hardware SPI:
spi = board.SPI()
# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)
# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

my_button = qwiic_button.QwiicButton()

state = 0
while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    if state == 0:
        clocktime = time.strftime("%A, %B %e, %Y")
        draw.text((x,top), clocktime, font=font, fill="#03cafc")
        clocktime2 = time.strftime("%H:%M:%S")
        y = top + font.getsize(clocktime)[1]
        draw.text((x, y), clocktime2, font=font, fill="#1303fc")
        disp.image(image, rotation)
        time.sleep(1)
    elif state == 1:
        clocktime = time.strftime("%A, %B %e, %Y")
        draw.text((x,top), clocktime, font=font, fill="#03cafc")
        clocktime2 = time.strftime("%I:%M:%S")
        y = top + font.getsize(clocktime)[1]
        draw.text((x,y), clocktime2, font=font, fill="#7703fc")
        disp.image(image, rotation)
        time.sleep(1)    
    if state == 0 and my_button.is_button_pressed()==True:
        state = 1
    elif state == 1 and my_button.is_button_pressed()==True:
        state = 0
