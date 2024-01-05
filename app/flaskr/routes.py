from flask import (Flask,request,Response,abort,jsonify)  
from flaskr import app
import json
from microservices import predictor

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/predict', methods=['GET'])
def predict():

    # TODO: Authenticate (authenticator.authenticate)
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

    # TODO: Log (logger.log)
    return predictor.predict(json_data)
    