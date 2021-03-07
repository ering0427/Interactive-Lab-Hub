import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.hx8357 as hx8357
import adafruit_rgb_display.st7735 as st7735
import adafruit_rgb_display.ssd1351 as ssd1351
import adafruit_rgb_display.ssd1331 as ssd1331 

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

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

# setup for buttons
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
image1 = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
draw1 = ImageDraw.Draw(image1)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
draw1.rectangle((0,0,width,height),outline=0,fill=(0,0,0))
disp.image(image, rotation)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

image1 = Image.open("red.jpg")

# Scale image to smaller screen dimension
image_ratio = image.width / image.height
screen_ratio = width / height
if screen_ratio < image_ratio:
    scaled_width = image.width * height // image.height
    scaled_height = height
else:
    scaled_width = width
    scaled_height = image.height * width // image.width
image1 = image1.resize((scaled_width, scaled_height), Image.BICUBIC)

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw1.rectangle((0,0,width,height),outline=0,fill=0)
    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py
    # Display image.
    
    if buttonA.value and buttonB.value:
        backlight.value = False
    else:
        backlight.value = True
    
    if buttonB.value and not buttonA.value: # just button A pressed
        clocktime = time.strftime("%m/%d/%Y %H:%M:%S")
        draw.text((x,top), clocktime, font=font, fill="#FFFFFF")
        disp.image(image, rotation)
        time.sleep(1)
    if buttonA.value and not buttonB.value: # just button B pressed
        draw.rectangle((0,0,width,height),outline=0,fill=0)
        x1 = scaled_width // 2 - width // 2
        y1 = scaled_height // 2 - height // 2
        image1 = image1.crop((x1,y1,x1+width, y1+height))
        draw.rectangle((0,0,width,height),outline=0,fill=0)
        disp.image(image1, rotation)
	
