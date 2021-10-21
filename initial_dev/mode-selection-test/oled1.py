import time
import os

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from modeDisplay import modeType

import subprocess

#pin configuration,on the OLED this pin isnt used
RST = None

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=1, gpio=1)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

#Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

#Draw some shapes.
# First define some constants to allow easy resizing of shapes.
paddling = -2
top = paddling
bottom = height-paddling
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# def main():
#     while True:
#         # Draw a black filled box to clear the image.
#         draw.rectangle((0,0,width,height), outline=0, fill=0)
#
#
#         draw.text()
#         draw.text()
#         draw.text()
#         draw.text()
#
#         # Diaplay image.
#         disp.image(image)
#         disp.display()
#         # time.sleep(.5)
#
# if __name__ == "__main__":
#     try :
#         main()
#     except KeyboardInterrupt:
#         print(" Program closed! ")
#         pass