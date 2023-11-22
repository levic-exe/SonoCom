import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
from soco import SoCo
from flask import Flask
import os
import socket
from soco.discovery import by_name, discover
import sys
from scipy.io.wavfile import write
import time
import pydub

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()
source_file = "static/test.mp3"
destination_file = "test.mp3"
def stupid_timer_thing():
    time.sleep(15)
    sys.exit(0)
def run_sonos_controller():
    # Create a Sonos controller instance
    zone = SoCo('192.168.4.34')
    sonos = (zone)  # Pass in the IP of your Sonos speaker

    # Play the specified media file through the Sonos speaker
    sonos.play_uri(f'http://{ip_address}:8000/static/test.mp3')

    # Get information about the currently playing track
    track = sonos.get_current_track_info()

    # Print the title of the currently playing track
    print(track['title'])

    # Pause the playback
    sonos.pause()

    # Play a stopped or paused track
    sonos.play()

def run_flask():
    # Create a Flask application instance
    app = Flask(__name__)

    # Run the Flask application on the specified host and port
    app.run(host=ip_address, port=8000, use_reloader=False)

# Record audio to a wav
sound = pydub.AudioSegment.from_wav("audio.wav")
sound.export("test.mp3", format="mp3")
os.replace(destination_file, source_file)
print("done recording")
print(ip_address)

# Create threads for the Sonos controller and the Flask application
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
sonos_thread = threading.Thread(target=run_sonos_controller)
sonos_thread.daemon = True
timer_thread = threading.Thread(target=stupid_timer_thing)

# Start the threads
flask_thread.start()
timer_thread.start()
sonos_thread.start()