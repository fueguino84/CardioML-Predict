import json
import numpy as np
import tensorflow as tf

def predict(data):
    data = json.loads(data)

    model = tf.keras.models.load_model("./../model.keras")
    param = np.array([data["colesterol"], data["presion"], data["glucosa"], data["edad"], data["sobrepeso"], data["tabaquismo"]])
    result = model.predict(np.expand_dims(param, axis=0))

    if result.item() < 1:
        response_data = {"respuesta": "El paciente no tiene riesgo cardiaco.", "valor": str(result.item())}, 200
        return response_data
    else:
        response_data = {"respuesta": "El paciente si tiene riesgo cardiaco.", "valor": str(result.item())}, 200
        return response_data
