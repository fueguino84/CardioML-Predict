from flask import Flask, request, jsonify
import db
from datetime import datetime
from bson import json_util

app = Flask(__name__)

def check_apikey(apikey):
    client = db.get_db()
    users_collection = client.topicos2.users

    # Busco el Documento de MongoDB conteniendo la API key provista
    user_data = users_collection.find_one({"apikey": apikey})

    return user_data

def check_quota(api_key, start_time, group):

    if (group == "FREEMIUM"):
        quota = 5
    elif (group == "PREMIUM"):
        quota = 50
    else:
        return {"respuesta": "Grupo de usuario inválido"}, 403
    
    client = db.get_db()
    querys_collection = client.topicos2.querys

    time_threshold = start_time - 60
    count_documents = querys_collection.count_documents({"start_time": {"$gte": time_threshold}})
    print(f"Numeros de consultas realizadas por esta api_key en el último minuto: {count_documents}")

    if (count_documents >= quota):
        print(f"No se procesa la petición porque se excedió la cuota disponible: {quota} consultas por minuto")
        return {"error": "Quota excedida"}, 403
    else:
        query_entry = {
            "api_key": api_key,
            "start_time": start_time
        }
        
        querys_collection.insert_one(query_entry)

        return True

@app.route('/authenticate', methods=['POST'])
def authenticate():
    api_key = request.headers.get('Authorization')
    data = request.get_json()
    
    user_info = check_apikey(api_key)

    if user_info:
        if check_quota(api_key, data["start_time"], user_info["group"]):
            return jsonify({"respuesta": "Authentication correcta", "user_info": json_util.dumps(user_info)})
    
    return jsonify({"respuesta": "Error de autenticación"}), 401

if __name__ == '__main__':
    app.run(port=5001, debug=True)
