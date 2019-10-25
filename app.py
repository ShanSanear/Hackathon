#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import audioop
import json
import random
import time
from datetime import datetime
from statistics import mean
import numpy

import pyaudio
from flask import Flask, Response, render_template

application = Flask(__name__)
random.seed()  # Initialize the random number generator

FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 0.1



# start Recording
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
stream.start_stream()

def read():
    # stream.start_stream()
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)

        frames.append(numpy.log10(rms) * 20)
    # stream.stop_stream()
    return mean(frames)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': read()})
            yield f"data:{json_data}\n\n"
            #time.sleep(0.1)

    return Response(generate_random_data(), mimetype='text/event-stream')


if __name__ == '__main__':
    application.run(debug=True, threaded=True)
