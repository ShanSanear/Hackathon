import audioop
import json
from datetime import datetime
from statistics import mean
import numpy

from flask import Flask, Response, render_template

from audio import stream, RATE, CHUNK, RECORD_SECONDS

application = Flask(__name__)


def read():
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)

        frames.append(numpy.log10(rms) * 20)
    return mean(frames)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/chart-data')
def chart_data():
    def get_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': read()})
            yield f"data:{json_data}\n\n"

    return Response(get_data(), mimetype='text/event-stream')


if __name__ == '__main__':
    application.run(debug=True, threaded=True)
