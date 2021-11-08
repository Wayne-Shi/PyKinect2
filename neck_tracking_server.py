from flask import Flask, request, jsonify
from datetime import datetime
import requests
import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from django.http import HttpResponse
from flask import send_file
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
time = []
angle = []
data = []
app = Flask(__name__)

@app.route('/take_data', methods=['POST'])
def take_data():
    in_data = request.get_json()
    data.append(in_data)
    time.append(in_data['time'])
    angle.append(in_data['angle'])
    return "Added data_point {}".format(in_data)

@app.route('/data', methods=['GET'])
def show_data():
    return "Database for User 1 {}".format(data)


@app.route('/data/plot_angle')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    fig.suptitle('Neck Angle vs Time', fontsize=20)
    axis.set_xlabel('Sampling @30fps', fontsize=15)
    axis.set_ylabel('Neck Angle (degrees)', fontsize=15)
    axis.plot(angle)
    return fig

@app.route('/data/get_log', methods=['GET'])
def get_log():
    csv_columns = ['time', 'angle']
    with open('neck_tracking_log.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(data)
    filename = 'neck_tracking_log.csv'
    return send_file(filename)

def main():
    app.debug = True
    app.run(host="0.0.0.0", port=5011)


if __name__ == '__main__':
    main()