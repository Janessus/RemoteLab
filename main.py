#!/usr/bin/env python


from gevent import monkey
monkey.patch_all()


from flask import Flask, render_template, Response, request
from camera import Camera
import AtMega as atmega
import os


host = '192.168.178.54'


def saveFile(name, content):
    f = open("avr/" + name, 'w')
    f.write(content)
    f.close()


def autoInstall():
    # flashing avr with raspberry
    # https://www.youtube.com/watch?v=npSwLOMfstY
    print("Installing...")
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

    saveFile('./avr/main.hex', json['file'])
    autoInstall()
    # print("data = " + str(json))
    return "uploaded"


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save("main.hex")
        autoInstall()
        return index()

        
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
    app.run(host=host, debug=True, threaded=True)

