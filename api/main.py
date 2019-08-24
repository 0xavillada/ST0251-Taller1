from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Information about the sensor
measureType = { 'sensor':'HC-SR04', 'variable':'DISTANCIA', 'unidades':'Centimetros' }

# Initial values for measures of HC-SR04 sensor
measures = [
    {'fecha': '2019-08-10 11:23:08', **measureType, 'valor':26},
    {'fecha': '2019-08-9 11:22:08', **measureType, 'valor':30},
    {'fecha': '2019-08-8 11:22:37', **measureType, 'valor':32},
    {'fecha': '2019-08-8 11:22:55', **measureType, 'valor':29}
    ]

# Return all measures
@app.route('/HC-SR04/getAll', methods=['GET'])
def getAll():
    return jsonify(measures)

# Return the media value of measures
@app.route('/HC-SR04/getMedia', methods=['GET'])
def getMedia():
    measuresCounter = 0
    media = 0.0
    for measure in measures:
        media = measure['valor'] + media
        measuresCounter += 1
    media = media / measuresCounter
    return jsonify({'media':media})

# Save a value of the sensor with additional information
@app.route('/HC-SR04/pushOne', methods=['POST'])
def pushOne():
    body = request.json
    fecha = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
    try:
        body['valor'] = int(body['valor'])
        measures.append({'fecha':fecha, **measureType, **body })
        return jsonify(measures)
    except:
        return jsonify({'mensaje': 'Error: json malformado'})

# Edit an register of measures
@app.route('/HC-SR04/editOne', methods=['PUT'])
def editOne():
    body = request.json
    for x in range(0,len(measures)):
        try:
            if measures[x]['fecha'] == body['fecha']:
                measures[x]['valor'] = body['valor']
                return jsonify(measures)
        except:
            return jsonify({'mensaje': 'Error: json malformado'})
    return jsonify({'mensaje': 'Error: registro no encontrado'})

# Removes an register of measures
@app.route('/HC-SR04/deleteOne', methods=['DELETE'])
def deleteOne():
    body = request.json
    for x in range(0,len(measures)):
        try:
            if measures[x]['fecha'] == body['fecha']:
                measures.pop(x)
                return jsonify(measures)
        except:
            return jsonify({'mensaje': 'Error: json malformado'})
    return jsonify({'mensaje': 'Error: registro no encontrado'})

app.run(port=5000, debug=True)