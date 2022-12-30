# Test program 
# Note -- to edit this via Visual Studio SSH, simply visit the folder in question and:
# sudo chmod -R 777 ./ 
import RPi.GPIO as GPIO
from time import sleep 

SOLENOID_PINS = [16, 26, 6, 5, 13] # in BCM (Broadcom) format 


VALVE_1 = 16
VALVE_2 = 5
VALVE_3 = 6

PUMP_PIN = 21

DURATION_PUMP_CYCLE_SECONDS = 1

# Valves. Need to be able to send a puff of air to 4 different outputs.
# To do this, we first configure the solenoids, and then turn on the pump. 
# In each case, let's turn the relays back to default (i.e., depower all solenoids)
# puff_1
# puff_2 
# puff_3 
# puff_4 
# all jets off (same as jet 4 on)

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in SOLENOID_PINS:
        GPIO.setup(pin, GPIO.OUT)
    GPIO.setup(PUMP_PIN, GPIO.OUT)

def pump_on():
    GPIO.output(PUMP_PIN, GPIO.HIGH)
    return

def pump_off():
    GPIO.output(PUMP_PIN, GPIO.LOW)
    return 

def puff_1():
    # valve 1: closed
    GPIO.output(VALVE_1, GPIO.HIGH)
    # turn on pump 
    # sleep(0.1)
    pump_on()
    sleep(DURATION_PUMP_CYCLE_SECONDS)
    # turn off pump
    pump_off()
    valves_off()
    return

def puff_2():
    # valve 1: open 
    GPIO.output(VALVE_1, GPIO.LOW)
    # valve 2: closed 
    GPIO.output(VALVE_2, GPIO.HIGH)
    # turn on pump 
    # sleep(0.1)

    pump_on()
    sleep(DURATION_PUMP_CYCLE_SECONDS)
    # turn off pump
    pump_off()
    valves_off()
    return

def puff_3():
    # valve 1: open 
    GPIO.output(VALVE_1, GPIO.LOW)
    # valve 2: open 
    GPIO.output(VALVE_2, GPIO.LOW)
    # valve 3: closed 
    GPIO.output(VALVE_3, GPIO.HIGH)
    # turn on pump 
    #sleep(0.1)

    pump_on()
    sleep(DURATION_PUMP_CYCLE_SECONDS)
    # turn off pump
    pump_off()
    valves_off()
    return

def puff_4():
    # valve 1: open 
    GPIO.output(VALVE_1, GPIO.LOW)
    # valve 2: open 
    GPIO.output(VALVE_2, GPIO.LOW)
    # valve 3: open 
    GPIO.output(VALVE_3, GPIO.LOW)
     # turn on pump 
    #sleep(0.1)

    pump_on()
    sleep(DURATION_PUMP_CYCLE_SECONDS)
    # turn off pump
    pump_off()
    return

def valves_off():
    GPIO.output(VALVE_1, GPIO.LOW)
    GPIO.output(VALVE_2, GPIO.LOW)
    GPIO.output(VALVE_2, GPIO.LOW)
    return; 


def activate_solenoid(sol_number):
    if (sol_number > len(SOLENOID_PINS)):
        return 
    if (sol_number == 0):
        return 

    #setup()
    GPIO.output(SOLENOID_PINS[sol_number-1], GPIO.HIGH)
    sleep(0.2)  
    GPIO.output(SOLENOID_PINS[sol_number-1], GPIO.LOW)
    sleep(0.2)  
    GPIO.output(SOLENOID_PINS[sol_number-1], GPIO.HIGH)
    sleep(2) #delay 
    GPIO.output(SOLENOID_PINS[sol_number-1], GPIO.LOW)
    #cleanup()

def cleanup():
    GPIO.cleanup()

def pulse_light_on_off():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5,GPIO.OUT)
    led = GPIO.PWM(5,100)
    led.start(0)
    pause_time = 0.02
    for i in range(0, 100+1):
        led.ChangeDutyCycle(i)
        sleep(pause_time)
    pause_time = 0.01
    for i in range(100, 0, -3):
        led.ChangeDutyCycle(i)
        sleep(pause_time)
    GPIO.cleanup()



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

