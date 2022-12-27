# Raspberry Pi app -- install this on your RPi. 
# Uses GPIO pins to drive solenoids and potentially LED lighting

# ! TO RUN THE FLASK APP, YOU NEED TO DO THIS
# ! STEP 1: install libraries
# pip3 install flask 
# pip3 install flask_cors

# ! STEP 2: run the app to test it out
# python rose.py
# or py rose.py
# or python3 rose.py 
# ! STEP 2a: Manual test 
# You should be able to visit http://localhost:5001/status and see a status message 

# ! STEP 3: make sure this python flask app runs at every device boot 
# various strategies -- gunicorn, etc. 
# set that as a startup app 

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from solenoidcontrol import setup, cleanup, activate_solenoid, pulse_light_on_off, pump_on, pump_off, puff_1, puff_2, puff_3, puff_4
import os 
import subprocess 
from subprocess import Popen, PIPE
from subprocess import check_output
from testshell import run_the_script
from pix import doChase, doRainbow, pixelsOff, doColor
from time import sleep 

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_shell_script_output_using_check_output():
    stdout = check_output(['/home/pi/rose/python/runpix.sh']).decode('utf-8')
    return stdout

setup()

@app.route('/')
@cross_origin()
def home():
    return 'Hello there, from Raspberry Pi.'

@app.route("/pump/on")
@cross_origin()
def pumpon(): 
    pump_on()
    return jsonify(message="Pump on")

@app.route("/pump/off")
@cross_origin()
def pumpoff(): 
    pump_off()
    return jsonify(message="Pump off")

# PETAL DROPPING ENDPOINTS
@app.route("/drop/1")
@cross_origin()
def drop1(): 
    puff_1()
    return jsonify(message="dropped 1")

@app.route("/drop/2")
@cross_origin()
def drop2(): 
    puff_2()
    return jsonify(message="dropped 2")

@app.route("/drop/3")
@cross_origin()
def drop3(): 
    puff_3()
    return jsonify(message="dropped 3")

@app.route("/drop/4")
@cross_origin()
def drop4(): 
    puff_4()
    return jsonify(message="dropped 4")


@app.route("/neo")
@cross_origin()
def neo(): 
    # stream = os.popen('/home/pi/rose/python/runpix.sh')
    # output = stream.read()
    # os.system("sudo python /home/pi/rose/python/pix.py")

    # output = get_shell_script_output_using_check_output()
    try:
        doRainbow()
        sleep(2)
        pixelsOff()

    except Exception as e:
        return jsonify(message="encountered an error "+str(e))

    return jsonify(message="Ran the neopixel script")


@app.route("/color")
@cross_origin()
def color(): 
    args = request.args
    r = args.get('r', default=0, type=int) 
    g = args.get('g', default=0, type=int) 
    b = args.get('b', default=0, type=int) 
    
    try:
        doColor(r, g, b)

    except Exception as e:
        return jsonify(message="encountered an error "+str(e))

    return jsonify(message="Set the color to "+str(r)+","+str(g)+","+str(b))


@app.route('/status')
@cross_origin()
def status():
    return jsonify(message='Connection successful!')

@app.route('/activate/<solenoid>')
@cross_origin()
def drop(solenoid):
    if (not solenoid.isdigit()):
        return jsonify(message="Not numeric")
    sol_number = int(solenoid)
    activate_solenoid(sol_number)
    if ((sol_number<1) or (sol_number>4)):
        return jsonify(message='Invalid number')
    return jsonify(message='Dropped '+solenoid)

@app.route('/light/pulse')
@cross_origin()
def pulse_light():
    pulse_light_on_off()
    return jsonify(message='Pulsed')

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5001)

