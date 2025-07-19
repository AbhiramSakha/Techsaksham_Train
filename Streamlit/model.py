from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import joblib

app = Flask(__name__)

# Load the trained model and label encoders
model = load_model('waste_model.h5')
label_encoder_location = joblib.load('label_encoder_location.pkl')
label_encoder_waste_type = joblib.load('label_encoder_waste_type.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    timestamp = pd.to_datetime(data['timestamp'])
    hour = timestamp.hour
    day_of_week = timestamp.dayofweek
    location = label_encoder_location.transform([data['location']])[0]
    waste_type = label_encoder_waste_type.transform([data['waste_type']])[0]

    input_data = np.array([[hour, day_of_week, location, waste_type]])
    prediction = model.predict(input_data)

    return jsonify({'predicted_weight': float(prediction[0][0])})

if __name__ == '__main__':
    app.run(debug=True)