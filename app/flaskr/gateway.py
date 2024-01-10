from flask import (Flask,request,Response,abort,jsonify,g)  
import json
from datetime import datetime
from cachetools import TTLCache
import logging
import requests

app = Flask(__name__)

# Configuro rutas de microservicios
AUTH_SERVICE_URL = 'http://localhost:5001/authenticate'
LOG_SERVICE_URL = 'http://localhost:5003/log'
PREDICT_SERVICE_URL = 'http://localhost:5002/predict'

# Configura el nivel de registro (DEBUG, INFO, etc.)
logging.basicConfig(level=logging.DEBUG)


CACHE_SIZE = 100
CACHE_EXPIRATION_TIME = 60  # segundos
cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_EXPIRATION_TIME)

@app.route('/predict', methods=['GET'])
def predict():
    try: 
        start_time = datetime.now().timestamp()

        # Procedo a autenticar con el microservicio
        api_key = request.headers.get('Authorization')
        authentication_result = requests.post(AUTH_SERVICE_URL, headers={'Authorization': api_key}, json={"start_time": start_time})
        if authentication_result.status_code != 200:
            return jsonify({"respuesta": "Error de autenticación"}), 403
        # Autenticación correcta
        else:
            params = {
                "colesterol": float(request.args.get("colesterol", 0)),
                "presion": float(request.args.get("presion", 0)),
                "glucosa": float(request.args.get("glucosa", 0)),
                "edad": float(request.args.get("edad", 0)),
                "sobrepeso": float(request.args.get("sobrepeso", 0)),
                "tabaquismo": float(request.args.get("tabaquismo", 0))
             }
        
            cache_key = json.dumps(params)
            
            if cache_key in cache:
                result = cache[cache_key]
                #print("Usando la caché disponible:", cache_key)
                logging.debug("Usando la caché disponible: %s", cache_key)
            else:
                json_data = json.dumps(params)
                result = requests.post(PREDICT_SERVICE_URL, json=json_data)
                result = result.json()
                
                cache[cache_key] = result

                log_json = {
                    "params": json_data,
                    "response": result,
                    "start_time": start_time,
                    "user_info": authentication_result.json()["user_info"]
                }
                log_result = requests.post(LOG_SERVICE_URL, json=log_json)
            
                #print("Nueva caché disponible:", cache_key)
                logging.debug("Nueva caché disponible: %s", cache_key)

        return result

    except ValueError as e:
        return {"Error en la función predict al colocar un valor incorrecto": str(e)}, 400
    except Exception as e:
        return {"Error en la función predict": str(e)}, 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
