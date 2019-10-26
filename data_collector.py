import audioop
import json
import time
from collections import defaultdict
from datetime import datetime
from statistics import mean
from threading import Lock

import numpy
import pyaudio
from flask import Response

from audio import FORMAT, CHANNELS, RATE, CHUNK, RECORD_SECONDS


class DataCollector:
    def __init__(self):
        self.stream_infos = {}
        self.stream_objects = {}
        self.time_interval = 0.5
        self.stored_stream_data = defaultdict(list)

    def create_data_point(self, device_index=1, device_name="Default stream name"):
        if device_index in self.stream_infos:
            return self.stream_infos[device_index]
        audio = pyaudio.PyAudio()
        stream = audio.open(input_device_index=device_index,
                            format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        self.stream_objects[device_index] = stream
        self.stream_infos[device_index] = device_name

    def read_from_stream(self, stream_number=1):
        frames = []
        stream = self.stream_objects[int(stream_number)]
        stream: pyaudio.Stream
        if stream.is_stopped():
            stream.start_stream()
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            rms = audioop.rms(data, 2)

            frames.append(numpy.log10(rms) * 20)
        return mean(frames)

    def get_single_stream_data(self, stream_number):
        def get_data():
            while True:
                lock = Lock()
                lock.acquire(blocking=True)
                json_data = json.dumps(
                    {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     'value': self.read_from_stream(stream_number)}
                )
                self.stored_stream_data[stream_number].append(json_data)
                yield f"data:{json_data}\n\n"
                time.sleep(self.time_interval)
                lock.release()

        return Response(get_data(), mimetype='text/event-stream')

    def change_configuration(self, configuration):
        if 'time_interval' in configuration:
            time_interval = configuration['time_interval']
            self.time_interval = time_interval

    def fetch_stored_data(self):
        stored_data = self.stored_stream_data
        self.stored_stream_data = defaultdict(list)
        return stored_data
