# Main Raspberry Pi control, which handles the GPIO
# The functions declared here are called by the Flask app rose.py 

# To edit this via Visual Studio SSH, be sure to sign in with root 
# privileges. E.g., ssh root@192.168.11.1 (when you've connected to the 
# EnchantRose network).
# EnchantRose wifi password: "beourguest!" 

import RPi.GPIO as GPIO
from time import sleep 

PUMP_PINS = [16, 26, 6, 5] # in BCM (Broadcom) format 
STEMLIGHT_PIN = 25 
# !PIN 18 IS RESERVED FOR NEOPIXEL -- see the file neopixel_control.py

DURATION_PUMP_CYCLE_SECONDS = 1

# Need to be able to send a puff of air to 4 different tubes.
# Each tube has its own motor. 

# Tell the board the pins we want to use 
def setup_rpi():
    GPIO.setmode(GPIO.BCM)
    for pin in PUMP_PINS:
        GPIO.setup(pin, GPIO.OUT)
    GPIO.setup(STEMLIGHT_PIN, GPIO.OUT)

def puff_pump(pump_number):
    if (pump_number > 3):
        return 
    if (pump_number < 0):
        return 
    GPIO.output(PUMP_PINS[pump_number], GPIO.HIGH)
    sleep(DURATION_PUMP_CYCLE_SECONDS)
    GPIO.output(PUMP_PINS[pump_number], GPIO.LOW)
    return "Petal %s: activated BCM PIN #%s" % (pump_number+1, PUMP_PINS[pump_number])

# raspberry pi happens to have an 8550 transistor 
# so, to turn on the light, set the "emitter" pin to low 
def stemlight_on():
    GPIO.output(STEMLIGHT_PIN, GPIO.LOW)
    return "Stemlight on; PIN #%s set to LOW" % STEMLIGHT_PIN

def stemlight_off():
    GPIO.output(STEMLIGHT_PIN, GPIO.HIGH)
    return "Stemlight off; PIN #%s set to HIGH" % STEMLIGHT_PIN

def cleanup():
    GPIO.cleanup()

# --------------------------------

if __name__ == "__main__":
    setup()
    print("Puff 1")
    puff_1()
    print("Puff 2")
    puff_2()
    print("Puff 3")
    puff_3()
    print("Puff 4")
    puff_4()
    cleanup()

# GPIO.output(VALVE_3, GPIO.HIGH)
#sleep(2)
# GPIO.output(VALVE_3, GPIO.LOW)

