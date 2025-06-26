from flask import Flask, request, jsonify
from flask_cors import CORS
from mlmodel import mlmodel
from dataframes import locDataFrame
import pandas as pd
app = Flask(__name__)
CORS(app)

model = mlmodel()
places = []

loc = locDataFrame()

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    received_message = data.get('message')
    mlreturn = model.finalfunc(str(received_message))
    if len(mlreturn)>1:
        return jsonify({'data_received': mlreturn})
    if loc.findy(mlreturn):
        print("yes")
        return jsonify({'data_received': mlreturn})
        return mlreturn
    else:
        print("no")
        return jsonify({'data_received': "NA"})
        return "NA"
    # Perform any processing you need on the received message
    # For now, let's just echo it back
    print(received_message)
    return jsonify({'data_received': mlreturn})

@app.route('/api/places', methods=['POST'])
def handle_places():
    data = request.json
    action = data.get('action')
    place_name = data.get('placeName')
    place_type = data.get('placeType')

    if action == 'insert':
        if not any(place['name'] == place_name for place in places):
            places.append({'name': place_name, 'type': place_type})
            loc.insert(place_name, place_type)
            return jsonify({'name': place_name, 'type': place_type})
        else:
            return jsonify({'error': f'Place "{place_name}" already exists'}), 400
    elif action == 'delete':
        places[:] = [place for place in places if place['name'] != place_name]
        loc.delete(place_name)
        return jsonify({'message': f'Place "{place_name}" deleted'})
    else:
        return jsonify({'error': 'Invalid action'}), 400

if __name__ == '__main__':
    app.run(debug=True)
