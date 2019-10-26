import os
import time

import pyaudio
from flask import Flask, render_template, request, jsonify
from flask_apscheduler import APScheduler

import atexit
import requests
from numpy import average

from data_collector import DataCollector


app = Flask(__name__)
cron = APScheduler()
cron.init_app(app)
data_collector = DataCollector()


def map_stream_data(stream_data):
    tmp = {'Average': average([point['value'] for point in stream_data]),
           'StartTime': stream_data[0]['time'],
           'EndTime': stream_data[-1]['time']}
    return tmp


def send_data_to_database(stream_data, device_name):
    endpoint_device = '127.0.0.1:5000/api/device'
    endpoint_entry = '127.0.0.1:5000/api/entry'
    mapped_stream_data = map_stream_data(stream_data)
    mapped_stream_data['Device'] = {
        'Name': device_name
    }
    r = requests.post(endpoint_entry, json={"key": "value"})


@cron.task(id='job_function', trigger='interval', seconds=10)
def job_function():
    # TODO Sending data to database
    sql_server_ip = "1.1.1.1"
    api_name = "Hackathon"

    print("CRON JOB {}".format(time.time()))
    stream_infos = data_collector.stream_infos
    data = data_collector.fetch_stored_data()
    computer_name = os.getenv("COMPUTER_NAME", "Unknown")
    for device_id, stream_data in data.items():
        device_name = f"{computer_name}_{device_id}"
        send_data_to_database(stream_data, device_name)


@app.route('/new_interval')
def change_sending_data_interval():
    cron.scheduler.reschedule_job(job_id='job_function', trigger='interval', seconds=20)
    return "Rescheduled"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart-data')
def get_chart_data():
    return data_collector.get_chart_data()


@app.route('/chart-data/<stream_number>')
def get_single_chart_data(stream_number):
    return data_collector.get_single_stream_data(int(stream_number))


@app.route('/configuration', methods=['POST'])
def change_configuration():
    configuration_data = request.get_json()
    return data_collector.change_configuration(configuration_data)


@app.route('/create_stream', methods=['POST'])
def create_stream():
    stream_configuration = request.get_json()
    device_index: int = stream_configuration['device_index']
    device_name: str = stream_configuration['device_name']
    data_collector.create_data_point(device_index, device_name)
    return "Stream created"


@app.route('/streams', methods=['GET'])
def get_streams():
    message = data_collector.stream_infos
    resp = jsonify(message)
    resp.status_code = 200
    print(resp)
    return resp


@app.route('/audio_devices')
def get_audio_devices():
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        device = p.get_device_info_by_index(i)
        devices.append(device)
    devices = [device for device in devices if
               'Sound Mapper' not in device['name']
               and device['maxInputChannels']]
    resp = jsonify(devices)
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    cron.start()
    atexit.register(lambda: cron.shutdown(wait=False))
    app.run(debug=True, threaded=True, use_reloader=False, port=5010)
