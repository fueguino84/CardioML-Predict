from flask import (Flask,request,Response,abort,jsonify,g)  
from flaskr import app
import json
from microservices import authenticator
from microservices import db
from microservices import predictor
from datetime import datetime


@app.route('/predict', methods=['GET'])
def predict():

    start_time = datetime.now().timestamp()

    authentication_result, user_info = authenticator.authenticate(request)
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

        # Record the end time
        end_time = datetime.now().timestamp()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        log_to_mongodb(json_data, result, start_time, elapsed_time,end_time,user_info)
    else:
        result = {"respuesta": "Error de autenticación"}, 403

    return result

def log_to_mongodb(json_data, result, start_time, elapsed_time,end_time,user_info):
    db1 = db.get_db()
    log_collection = db1.topicos2.log  
    
    log_entry = {
        "start_time": start_time,
        "params": json_data,
        "response": result,
        "elapsed_time": elapsed_time,
        "end_time":end_time,
        "user_info":user_info
    }
    
    log_collection.insert_one(log_entry)
    db1.close()
