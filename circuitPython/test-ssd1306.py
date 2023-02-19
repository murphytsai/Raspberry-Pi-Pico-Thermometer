# SPDX-FileCopyrightText: Tony DiCola
# SPDX-License-Identifier: CC0-1.0

# Basic example of clearing and drawing pixels on a SSD1306 OLED display.
# This example and library is meant to work with Adafruit CircuitPython API.

# Import all board pins.
#from board import SCL, SDA
import board
import busio

# Import the SSD1306 module.
import adafruit_ssd1306

i2c_lcd = busio.I2C (scl=board.GP1, sda=board.GP0) # This RPi Pico way to call I2C

# Create the I2C interface.
#i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c_lcd)
# Alternatively you can change the I2C address of the device with an addr parameter:
# display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x31)

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
oled.fill(0)
oled.text('hello world here', 0,0, None)
oled.show()