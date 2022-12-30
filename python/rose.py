# Raspberry Pi app -- install this on your RPi. 
# Uses GPIO pins to drive solenoids and potentially LED lighting

# ! TO RUN THE FLASK APP, YOU NEED TO DO THIS
# ! STEP 1: install libraries
# pip3 install flask 
# pip3 install flask_cors

# ! STEP 2: run the app to test it out
# python rose.py

# ! STEP 2a: Manual test 
# You should be able to visit http://localhost:5001/status and see a status message 

# ! STEP 3: make sure this python flask app runs at every device boot 
# pip install gunicorn

# modify /etc/rc.local to start gunicorn with the flask app at every boot:
# add this line to the end of /etc/rc.local (assuming your flask code "rose.py" is in /root/rose/enchantedrosepython/python)
# gunicorn -c /root/rose/enchantedrosepython/python/gunicorn.conf.py --chdir /root/rose/enchantedrosepython/python rose:app
#
# contents of "gunicorn.conf.py":
# bind="0.0.0.0:5001"
# workers=2

# ! Development Notes
# To kill gunicorn process while developing: 
# pkill gunicorn
# 
# then you can test out the new flask app simply with 
# python rose.py
#
# when done, push changes to the Github repository 

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from rpi_control import setup_rpi, puff_pump, stemlight_on, stemlight_off
import os 
import subprocess 
from subprocess import Popen, PIPE
from subprocess import check_output
from testshell import run_the_script
from neopixel_control import doChase, doRainbow, pixelsOff, doColor
from time import sleep 

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

setup_rpi()

@app.route('/')
@cross_origin()
def home():
    return jsonify(message="Hello, world, from the Enchanted Rose prop.")

# PETAL DROPPING ENDPOINTS
@app.route("/drop/1")
@cross_origin()
def drop1(): 
    msg = puff_pump(0)
    return jsonify(message=msg)

@app.route("/drop/2")
@cross_origin()
def drop2(): 
    msg = puff_pump(1)
    return jsonify(message=msg)

@app.route("/drop/3")
@cross_origin()
def drop3(): 
    msg = puff_pump(2)
    return jsonify(message=msg)

@app.route("/drop/4")
@cross_origin()
def drop4(): 
    msg = puff_pump(3)
    return jsonify(message=msg)

# STEM LIGHTS ----------------------
@app.route("/stemlight/on")
@cross_origin()
def do_stemlight_on():
    msg = stemlight_on()
    return jsonify(message=msg)

@app.route("/stemlight/off")
@cross_origin()
def do_stemlight_off():
    msg = stemlight_off()
    return jsonify(message=msg)


# NEOPIXEL ACCENT LIGHTS ----------------------
@app.route("/neo/rainbow")
@cross_origin()
def neo_rainbow(): 
    try:
        doRainbow()

    except Exception as e:
        return jsonify(message="encountered an error "+str(e))

    return jsonify(message="Did a rainbow")

@app.route("/neo/chase")
@cross_origin()
def neo_chase(): 
    try:
        doChase()
        sleep(3)
        pixelsOff()

    except Exception as e:
        return jsonify(message="encountered an error "+str(e))

    return jsonify(message="Did a chase")

@app.route("/neo/off")
@cross_origin()
def neo_off(): 
    try:
        pixelsOff()

    except Exception as e:
        return jsonify(message="encountered an error "+str(e))

    return jsonify(message="Turned off neopixels")

@app.route("/neo/color")
@cross_origin()
def do_neo_color(): 
    args = request.args
    r = args.get('r', default=0, type=int) 
    g = args.get('g', default=0, type=int) 
    b = args.get('b', default=0, type=int) 
    
    try:
        doColor(r, g, b)

    except Exception as e:
        return jsonify(message="encountered an error "+str(e))

    return jsonify(message="Color set to "+str(r)+","+str(g)+","+str(b))

@app.route('/status')
@cross_origin()
def status():
    return jsonify(message='Connection successful!')


if __name__=='__main__':
    app.run(host="0.0.0.0", port=5001)

