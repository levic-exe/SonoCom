#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
import subprocess
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()
command = "python send-audio-to-sonos.py"

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')
        subprocess.run(command, shell=True)
        return render_template('index.html', request="POST")
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, ssl_context=('cert.pem', 'key.pem'), host=ip_address)