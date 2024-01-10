from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import joblib
import json

app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    
    return app

@app.route('/predict', methods=['POST'])
def predict():
    try: 
        data = request.get_json()
        data = json.loads(data)

        model = tf.keras.models.load_model("./../../model.keras")
        params = np.array([data["colesterol"], data["presion"], data["glucosa"], data["edad"], data["sobrepeso"], data["tabaquismo"]])

        params = params.reshape(1, -1)
    
        # Cargo el scaler del modelo y lo aplico a los valores actuales
        scaler = joblib.load("./../../scaler.joblib")
        
        scaled_params = scaler.transform(params)
        
        result = model.predict(scaled_params)

        if result.item() < 1:
            return {"respuesta": "El paciente no tiene riesgo cardiaco.", "valor": str(result.item())}, 200
        else:
            return {"respuesta": "El paciente si tiene riesgo cardiaco.", "valor": str(result.item())}, 200
            
    except Exception as e:
        return {"Error en la función predict": str(e)}, 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)
