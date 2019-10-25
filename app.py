from flask import Flask, render_template, request, jsonify
from flask_apscheduler import APScheduler

import atexit

from data_collector import DataCollector

app = Flask(__name__)
cron = APScheduler()
cron.init_app(app)
cron.start()


@cron.task('interval', seconds=10)
def job_function():
    print("CRON JOB")


data_collector = DataCollector()


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

@app.route('/streams', methods=['GET'])
def get_streams():
    message = data_collector.get_stream_infos()
    resp = jsonify(message)
    resp.status_code = 200
    print(resp)
    return resp

if __name__ == '__main__':
    atexit.register(lambda: cron.shutdown(wait=False))
    app.run(debug=True, threaded=True)
