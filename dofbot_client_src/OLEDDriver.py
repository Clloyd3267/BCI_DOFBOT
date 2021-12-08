# ------------------------------------------------------------------------------
# Name         : OLEDDriver.py
# Date Created : 11/16/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : Control library for Raspberry Pi GPIO.
# ------------------------------------------------------------------------------

# Imports
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

MAX_LINE_WIDTH = 20

class OLEDDriver:
	def __init__(self):
		# pin configuration,on the OLED this pin isn't used
		RST = None
		# 128x32 display with hardware I2C:
		self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=1, gpio=1)
		self.disp.begin()
		self.disp.clear()
		self.disp.display()
		# Make sure to create image with mode '1' for 1-bit color.
		self.width = self.disp.width
		self.height = self.disp.height
		self.image = Image.new('1', (self.width, self.height))
		# Get drawing object to draw on image
		self.draw = ImageDraw.Draw(self.image)
		# Draw some shapes.
		# First define some constants to allow easy resizing of shapes.
		paddling = -2
		self.top = paddling
		self.bottom = self.height-paddling
		# Move left to right keeping track of the current x position for drawing shapes.
		self.x = 0
		# Load default font.
		self.font = ImageFont.load_default()
		self.clearDisplay()

	def clearDisplay(self, lines="012"):
		#clears display. if lines is "all", clears full. else, clears all but top line.
		if '0' in lines:
			self.printToLine(0)
		if '1' in lines:
			self.printToLine(1)
		if '2' in lines:
			self.printToLine(2)

	def printToLine(self, line, text=""):
		#writes to specified line, 3 lines of text with no overlapping.

		# Crop to the right width
		text = text[:20]

		# Border
		self.draw.rectangle((0,            0,             self.width-1, 0           ),  fill=255)  # Top
		self.draw.rectangle((0,            self.height-1, self.width-1, self.height-1), fill=255)  # Bottom
		self.draw.rectangle((0,            0,             0,            self.height-1), fill=255)  # Left
		self.draw.rectangle((self.width-1, 0,             self.width-1, self.height-1), fill=255)  # Right

		if line == 0:
			self.draw.rectangle((1, 1, self.width-2, 11), fill=255)
			self.draw.text((3, -1), text, font=self.font, fill=0)
		if line == 1:
			self.draw.rectangle((1, 11, self.width-2, 21), fill=0)
			self.draw.text((3, 10), text, font=self.font, fill=255)
		if line == 2:
			self.draw.rectangle((1, 21, self.width-2, 30), fill=0)
			self.draw.text((3, 20), text, font=self.font, fill=255)

		self.disp.image(self.image)
		self.disp.display()

# oled = OLEDDriver()
# message =  "abcdefghijklmnopqrstuv"
# message1 = ""
# oled.printToLine(0, message)
# oled.printToLine(1, message)
# oled.printToLine(2, message)
# oled.clearDisplay()
# oled.printTo3Line(2, message[:22])
# oled.clearDisplay("1")
