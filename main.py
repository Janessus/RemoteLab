#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.

from gevent import monkey
monkey.patch_all()


from flask import Flask, render_template, Response, request
#from camera import VideoCamera
from camera import Camera
import AtMega as atmega
from threading import Thread
import cv2
import os

from gevent import pywsgi



def saveFile(name, content):
    f = open("avr/" + name, 'w')
    f.write(content)
    f.close()


def autoInstall():
    os.system("cd avr/ && make install")


app = Flask(__name__)
targetInterface = atmega.AtMega2561()
response = b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'



###################### API ######################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input', methods=['POST'])
def getInput():
    if request.is_json:
        json = request.get_json()
        inputType = json["inputType"]

        if inputType == "keyBoard":
            pass
        elif inputType == "buttons":
            targetInterface.buttons.input(int(json["portValue"]))
        elif inputType == "switches":
            targetInterface.switches.input(int(json["portValue"]))

        # print("data = " + str(json))
    return "Posted"


@app.route('/upload', methods=['POST'])
def getUpload():
    json = request.get_json()

    saveFile('main.hex', json['file'])
    autoInstall()
    # print("data = " + str(json))
    return "uploaded"


def frame():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError('Could not start camera.')

    while True:
        # read current frame
        _, img = camera.read()

        # encode as a jpeg image and return it
        yield cv2.imencode('.jpg', img)[1].tobytes()


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.178.56', debug=True, threaded=True)

