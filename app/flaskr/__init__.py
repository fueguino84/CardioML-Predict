# import os
from flask import (Flask,request,Response,abort,jsonify)  
# import numpy as np
# import pickle
# import pandas as pd
# import tensorflow as tf
# import json

app = Flask(__name__)

from flaskr import routes

#from flaskr.db import get_db
#from datetime import datetime
#from bson.json_util import dumps

'''
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/predict', methods=['GET', 'POST'])
    def predict():
        if request.method == 'GET':
            colesterol = float(request.args.get("colesterol", 0))
            presion = float(request.args.get("presion", 0))
            glucosa = float(request.args.get("glucosa", 0))
            edad = float(request.args.get("edad", 0))
            sobrepeso = float(request.args.get("sobrepeso", 0))
            tabaquismo = float(request.args.get("tabaquismo", 0))
        elif request.method == 'POST':
            data = request.get_json()
            colesterol = float(data.get("colesterol", 0))
            presion = float(data.get("presion", 0))
            glucosa = float(data.get("glucosa", 0))
            edad = float(data.get("edad", 0))
            sobrepeso = float(data.get("sobrepeso", 0))
            tabaquismo = float(data.get("tabaquismo", 0))
        else:
            abort(400, description='Invalid request method.')

        model = tf.keras.models.load_model("./../model.keras")
        param = np.array([colesterol, presion, glucosa, edad, sobrepeso, tabaquismo])
        result = model.predict(np.expand_dims(param, axis=0))

        if result.item()<1:
            return "El paciente no tiene riesgo cardiaco.Valor obtenido: " + str(result.item())
        
        else:
            return "El paciente si tiene riesgo cardiaco.Valor obtenido: " + str(result.item())
        

        
    @app.route('/requests', methods=['GET', 'POST'])
    def requests():
        result = get_db().request_log.find()
        # se convierte el cursor a una lista
        list_cur = list(result)
        # se serializan los objetos
        json_data = dumps(list_cur, indent=2)
        # retornamos la rista con los metadatos adecuados
        return Response(json_data, mimetype='application/json')

    return app
    '''