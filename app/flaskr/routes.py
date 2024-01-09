from flask import (Flask,request,Response,abort,jsonify,g)  
from flaskr import app
import json
from microservices import authenticator
from microservices import db
from microservices import logger
from microservices import predictor
from datetime import datetime
from cachetools import TTLCache
import logging

# Configura el nivel de registro (DEBUG, INFO, etc.)
logging.basicConfig(level=logging.DEBUG)


CACHE_SIZE = 100
CACHE_EXPIRATION_TIME = 60  # segundos
cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_EXPIRATION_TIME)

@app.route('/predict', methods=['GET'])
def predict():
    try: 
        start_time = datetime.now().timestamp()

        authentication_result, user_info = authenticator.authenticate(request, start_time)
    
        if authentication_result:

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
                result = predictor.predict(json_data)

                cache[cache_key] = result

                logger.log(json_data, result, start_time, user_info)
                #print("Nueva caché disponible:", cache_key)
                logging.debug("Nueva caché disponible: %s", cache_key)

        else:
            result = {"respuesta": "Error de autenticación"}, 403

        return result

    except ValueError as e:
        return {"Error en la función predict al colocar un valor incorrecto": str(e)}, 400
    except Exception as e:
        return {"Error en la función predict": str(e)}, 500
