from flask import Flask, jsonify, request
import csv
import json
import math

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flash!'

def filter_data():
    with open('camden.csv') as csvfile:
        reader = csv.reader(csvfile)
        longitude = []
        latitude = []
        for row in reader:
            if row[0] == "Longitude":
                longitude.append(row)
            elif row[0] == "Latitude":
                latitude.append(row)

    return map(int, longitude), map(int, latitude)


def make_json(index):
    with open('camden.csv') as csvfile:
        reader = list(csv.reader(csvfile))
        output = {}
        count = 0
        for entry in index:
            output[count] = {
                'Location': reader[20][entry],
                'Postcode': reader[5][entry],
                'Longitude': reader[14][entry],
                'Latitude': reader[15][entry]
            }
            count += 1

    return json.dumps(output)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


# add another variable to this in order to change the radius based on user input.
def location_returners(latitude, longtitude, targetLat, targetLon):
    """
    Calculate the indexes of the locations in the requested area
    """
    index = []
    for i in len(latitude):
        if haversine(targetLon, targetLat, longtitude[i], latitude[i]) < 1:
            index.append(i)
    return index


# def script():
#     longitude, latitude = filter_data()
#
#     index = location_returners(latitude, longitude, null, null)
#
#     return make_json(index)


@app.route('/query', methods=['GET'])
def perform_query():
    return request.args.get('longitude'), request.args.get('latitude')
