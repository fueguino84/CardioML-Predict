from flask import (Flask,request,Response,abort,jsonify,g)  
from flaskr import app
import json
from microservices import authenticator
from microservices import db
from microservices import logger
from microservices import predictor
from datetime import datetime

@app.route('/predict', methods=['GET'])
def predict():

    start_time = datetime.now().timestamp()

    authentication_result, user_info = authenticator.authenticate(request, start_time)
    # TODO: Authenticate QUOTA (authenticator.authenticate)
    if authentication_result:
        # TODO: Implementar Cache

        params = {
            "colesterol": float(request.args.get("colesterol", 0)),
            "presion": float(request.args.get("presion", 0)),
            "glucosa": float(request.args.get("glucosa", 0)),
            "edad": float(request.args.get("edad", 0)),
            "sobrepeso": float(request.args.get("sobrepeso", 0)),
            "tabaquismo": float(request.args.get("tabaquismo", 0))
        }

        json_data = json.dumps(params)

        # Perform prediction
        result = predictor.predict(json_data)

        logger.log(json_data, result, start_time, user_info)
    else:
        result = {"respuesta": "Error de autenticación"}, 403

    return result
