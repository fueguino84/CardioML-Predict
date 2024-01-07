from flask import (Flask,request,Response,abort,jsonify,g)  
from flaskr import app
import json
from microservices import db
from microservices import predictor
from datetime import datetime


@app.route('/predict', methods=['GET'])
def predict():

    start_time = datetime.now().timestamp()

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

     # Perform prediction
    result = predictor.predict(json_data)

    # Record the end time
    end_time = datetime.now().timestamp()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    log_to_mongodb(json_data, result, start_time, elapsed_time,end_time)
 

    return result

def log_to_mongodb(json_data, result, start_time, elapsed_time,end_time):
    db1 = db.get_db()
    log_collection = db1.topicos2.log  
    
    log_entry = {
        "start_time": start_time,
        "params": json_data,
        "response": result,
        "elapsed_time": elapsed_time,
        "end_time":end_time
    }
    
    log_collection.insert_one(log_entry)
    db1.close()



@app.route('/testdb')
def test_db():
    db1 = db.get_db()

    if db1 is not None:

        # Select the "users" collection
        users_collection = db1.topicos2.users  # Replace "your_database" with your actual database name

        # Retrieve the first document from the "users" collection
        first_user = users_collection.find_one()

        if first_user:
            # Do something with the first user document
            return str(first_user)
        else:
            return "No users found in the 'users' collection."

    else:
        return "Error: Database connection is not valid."
