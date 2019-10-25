import audioop
import json
import time
from datetime import datetime
from statistics import mean
import numpy
import pyaudio

from flask import Flask, Response, render_template

from audio import RATE, CHUNK, RECORD_SECONDS, FORMAT, CHANNELS


class DataCollector:
    def __init__(self):
        self.streams = []
        self.audios = []

    def create_data_point(self):
        # start Recording
        audio = pyaudio.PyAudio()
        self.audios.append(audio)
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        self.streams.append(stream)

    def read_from_stream(self, stream_number=0):
        if not self.audios:
            self.create_data_point()
        frames = []
        stream = self.streams[stream_number]
        stream.start_stream()
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = self.streams[stream_number].read(CHUNK)
            rms = audioop.rms(data, 2)

            frames.append(numpy.log10(rms) * 20)
        stream.stop_stream()
        return mean(frames)


app = Flask(__name__)
data_collector = DataCollector()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart-data')
def chart_data():
    def get_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': data_collector.read_from_stream()})
            yield f"data:{json_data}\n\n"
            time.sleep(0.5)

    return Response(get_data(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
