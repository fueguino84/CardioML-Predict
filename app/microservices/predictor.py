import json
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import joblib


def predict(data):
    data = json.loads(data)

    model = tf.keras.models.load_model("./../model.keras")
    params = np.array([data["colesterol"], data["presion"], data["glucosa"], data["edad"], data["sobrepeso"], data["tabaquismo"]])

    params = params.reshape(1, -1)

    # Cargo el scaler del modelo y lo aplico a los valores actuales
    scaler = joblib.load("./../scaler.joblib")
    
    scaled_params = scaler.transform(params)
    
    result = model.predict(scaled_params)

    if result.item() < 1:
        response_data = {"respuesta": "El paciente no tiene riesgo cardiaco.", "valor": str(result.item())}, 200
        return response_data
    else:
        response_data = {"respuesta": "El paciente si tiene riesgo cardiaco.", "valor": str(result.item())}, 200
        return response_data
