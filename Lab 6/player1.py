import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_mpr121
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors

import paho.mqtt.client as mqtt
import uuid

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # the rate  the screen talks to the pi
# Create the ST7789 display:
spi = board.SPI()

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

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

def report(current, turn, state):

    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    l1 = 'First to exceed 21 loses!'
    l2 = 'Current sum is '+str(current)
    if(state == 0):
    	l3 = "Player "+str(turn)+", what do you add?"
    elif(state == 1):
    	l3 = "Player 1 wins!"
    elif(state == 2):
    	l3 = "player 2 wins!"

    y = top
    draw.text((x, y), l1, font=font, fill="#FFFFFF")
    y += font.getsize(l1)[1]
    draw.text((x, y), l2, font=font, fill="#FFFFFF")
    y += font.getsize(l2)[1]
    draw.text((x, y), l3, font=font, fill="#FFFFFF")
    disp.image(image, rotation)


send_to = f"IDD/test/helen"

read_from = f"IDD/test/erin"

def on_connect(client, userdata, flags, rc):
	client.subscribe(read_from)

def on_message(cleint, userdata, msg):
	message = msg.payload.decode('UTF-8').split(',')
	global current
	global turn
	global state
	current, turn, state =  int(message[0]), int(message[1]), int(message[2])

client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

current = 0
state = 0
turn = 1
move = False
while True:

    client.loop()

    if (turn == 1):

    	if (state == 0):

            val = random.randrange(1,11)
            if (mpr121[0].value):
                turn = 1
                client.publish(send_to, str(current) + "," str(turn) + "," + str(state))
            elif(mpr121[1].value):
                current += val
                move = True

            if(current == 21):
                state = 2
                client.publish(send_to, str(current)+","+str(turn)+","+str(state)) 
            elif(current > 21):
                state = 1
                client.publish(send_to,str(current)+","+str(turn)+","+str(state))
            elif (move): 
                turn = 2
                move = False
		    
                client.publish(send_to, str(current)+","+str(turn)+","+str(state))
			
    report(current, turn, state)





