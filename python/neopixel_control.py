# to install neopixel libraries:
# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo python3 -m pip install --force-reinstall adafruit-blinka

import board
import neopixel
import RPi.GPIO as GPIO
from time import sleep 

NUM_PIXELS = 60 

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

def doColor(r, g, b):
    pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS)
    for i in range(0,60,1):
        pixels[i-1] = (r,g,b)

def doChase():
    pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS)
    # pixels[0] = (100, 0, 0)
    # pixels[1] = (0, 100, 0)
    for i in range(0,60,1):
        pixels[i-1] = (80,0,0)
        sleep(0.01)
    for i in range(60,0,-1):
        pixels[i-1] = (0,5,0)
        sleep(0.01)
    for i in range(0,60,1):
        pixels[i-1] = (0,0,5)
        sleep(0.01)
    for i in range(60,0,-1):
        pixels[i-1] = (0,0,0)
        sleep(0.01)

def pixelsOff():
    pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS)
    doColor(0,0,0)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def doRainbow():
    pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS, brightness=0.3)
    
    for i in range(NUM_PIXELS):
        rc_index = (i * 256 // NUM_PIXELS)
        pixels[i] = wheel(rc_index & 255)
    pixels.write()
    

if __name__ == "__main__":
    doRainbow()
    sleep(1)
    pixelsOff()