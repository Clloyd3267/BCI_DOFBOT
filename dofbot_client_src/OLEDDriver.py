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

MAX_LINE_WIDTH = 22

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
		# Draw a black filled box to clear the image.
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
		# Draw some shapes.
		# First define some constants to allow easy resizing of shapes.
		paddling = -2
		self.top = paddling
		self.bottom = self.height-paddling
		# Move left to right keeping track of the current x position for drawing shapes.
		self.x = 0
		# Load default font.
		self.font = ImageFont.load_default()

	def clearDisplay(self, lines):
		#clears display. if lines is "all", clears full. else, clears all but top line.
		if(lines!="all"):
			self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
		else:
			self.draw.rectangle((0, self.height-25, self.width, self.height), outline=0, fill=0)
		self.disp.image(self.image)
		self.disp.display()

	def printToLine(self, line, text):
		#writes to specified line, 4 lines of text with possible text overlapping with
		#characters which go below baseline.
		if(line==0):
			self.draw.rectangle((0, 0, self.width, self.height-26), outline=0, fill=0)
			self.draw.text((self.x, self.top), text, font=self.font, fill=255)
		elif(line==1):
			self.draw.rectangle((0, self.height-25, self.width, self.height-18), outline=0, fill=0)
			self.draw.text((self.x, self.height-26), text, font=self.font, fill=255)
		elif(line==2):
			self.draw.rectangle((0, self.height-17, self.width, self.height-10), outline=0, fill=0)
			self.draw.text((self.x, self.height-18), text, font=self.font, fill=255)
		elif(line==3):
			self.draw.rectangle((0, self.height-9, self.width, self.height), outline=0, fill=0)
			self.draw.text((self.x, self.height-10), text, font=self.font, fill=255)
		self.disp.image(self.image)
		self.disp.display()

	def printTo3Line(self, line, text):
		#writes to specified line, 3 lines of text with no overlapping.
		if(line==0):
			self.draw.rectangle((0, 0, self.width, self.height-24), outline=0, fill=255)
			self.draw.text((self.x, self.top), text, font=self.font, fill=0)
		elif(line==1):
			self.draw.rectangle((0, self.height-22, self.width, self.height-14), outline=0, fill=0)
			self.draw.text((self.x, self.height-23), text, font=self.font, fill=255)
		elif(line==2):
			self.draw.rectangle((0, self.height-12, self.width, self.height-4), outline=0, fill=0)
			self.draw.text((self.x, self.height-13), text, font=self.font, fill=255)
		self.disp.image(self.image)
		self.disp.display()
