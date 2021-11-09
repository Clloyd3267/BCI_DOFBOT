import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# import subprocess


class Draw:
    def __init__(self):
        # pin configuration,on the OLED this pin isn't used
        RST = None

        # 128x32 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=1, gpio=1)

        # Initialize library.
        self.disp.begin()

        # Clear display.
        self.disp.clear()
        self.disp.display()

        # Create blank image for drawing.
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

    def printToOled(self, modeName):

        #while True:
            # Draw a black filled box to clear the image.
            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

            self.draw.text((self.x, self.top), modeName, font=self.font, fill=255)
            # draw.text()
            # draw.text()
            # draw.text()

            # Display image.
            self.disp.image(self.image)
            self.disp.display()
            # time.sleep(.5)

