import os
from flask import (Flask,request,Response,abort,jsonify)  
import numpy as np
import pickle
import pandas as pd
import tensorflow as tf
#from flaskr.db import get_db
#from datetime import datetime
#from bson.json_util import dumps


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

    @app.route('/predict',methods=['GET', 'POST'])
    def predict():
       
        colesterol = request.args.get("colesterol")
        presion = request.args.get("presion")
        glucosa = request.args.get("glucosa")
        edad = request.args.get("edad")
        sobrepeso = request.args.get("sobrepeso")
        tabaquismo = request.args.get("tabaquismo")
        error = None
    
        model = pickle.load("../../model.pkl")
        model = tf.keras.models.load_model("../../model.keras")
        

        if not colesterol:
            error = 'colesterol is required.'
        elif not presion:
            error = 'presion is required.'
        elif not glucosa:
            error = 'glucosa is required.'
        elif not edad:
            error = 'edad is required.'
        elif not sobrepeso:
            error = 'sobrepeso is required.'
        elif not tabaquismo:
            error = 'tabaquismo is required.'

        if error:
            abort(404, description=error) 
        
        param=np.array([colesterol,presion,glucosa,edad,sobrepeso,tabaquismo])

        result = model.predict(param)

    return jsonify(result.tolist())
    
    #URL para probar
    #http://127.0.0.1:5000/predict?colesterol=0.1,presion=0.71,glucosa=0.85,edad=0.45,sobrepeso=1,tabaquismo=0& 

    @app.route('/requests',methods=['GET', 'POST'])
    def requests():
        result=get_db().request_log.find()
        # se convierte el cursor a una lista
        list_cur = list(result)         
        # se serializan los objetos
        json_data = dumps(list_cur, indent = 2)  
        #retornamos la rista con los metadatos adecuados
        return Response(json_data,mimetype='application/json')

    return app