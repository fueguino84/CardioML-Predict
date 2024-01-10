from flask import Flask, request, jsonify
import db
from datetime import datetime
# from bson import json_util

app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    
    return app

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()

    client = db.get_db()
    log_collection = client.topicos2.log  

    end_time = datetime.now().timestamp()
    elapsed_time = end_time - data["start_time"]

    log_entry = {
        "start_time": data["start_time"],
        "params": data["params"],
        "response": data["response"],
        "elapsed_time": elapsed_time,
        "end_time": end_time,
        "user_info": data["user_info"]
    }
    
    log_collection.insert_one(log_entry)

    return jsonify({"respuesta": "Consulta logueada correctamente"}), 200

'''
@app.route('/logs', methods=['GET'])
def get_logs():
    client = db.get_db()
    log_collection = client.topicos2.log  
    logs = list(log_collection.find())
    return jsonify(json_util.dumps(logs))
'''

if __name__ == '__main__':
    app.run(port=5003, debug=True)
