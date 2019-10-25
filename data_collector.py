import audioop
import json
import time
from datetime import datetime
from statistics import mean

import numpy
import pyaudio
from flask import Response

from audio import FORMAT, CHANNELS, RATE, CHUNK, RECORD_SECONDS


class DataCollector:
    def __init__(self):
        self.stream_infos = []
        self.stream_objects = []
        self.audios = []
        self.create_data_point()
        self.time_interval = 0.5

    def create_data_point(self):
        audio = pyaudio.PyAudio()
        self.audios.append(audio)
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        stream_info = {
            "stream_name": "Default stream name",
            "stream_id": len(self.stream_infos)
        }
        self.stream_objects.append(stream)
        self.stream_infos.append(stream_info)

    def read_from_stream(self, stream_number=0):
        frames = []
        stream = self.stream_objects[stream_number]['stream']
        stream.start_stream()
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            rms = audioop.rms(data, 2)

            frames.append(numpy.log10(rms) * 20)
        stream.stop_stream()
        return mean(frames)

    def get_chart_data(self):
        def get_data():
            while True:
                json_data = json.dumps(
                    {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     'value': self.read_from_stream()}
                )
                yield f"data:{json_data}\n\n"
                time.sleep(self.time_interval)

        return Response(get_data(), mimetype='text/event-stream')

    def get_single_stream_data(self, stream_number):
        def get_data():
            while True:
                json_data = json.dumps(
                    {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     'value': self.read_from_stream(stream_number)}
                )
                yield f"data:{json_data}\n\n"
                time.sleep(self.time_interval)

        return Response(get_data(), mimetype='text/event-stream')

    def change_configuration(self, configuration):
        if 'time_interval' in configuration:
            time_interval = configuration['time_interval']
            self.time_interval = time_interval

    def get_stream_infos(self):
        return self.stream_infos
