from flask import request
from microservices import db
from datetime import datetime

def check_apikey(apikey):
    client = db.get_db()
    users_collection = client.topicos2.users

    # Busco el Documento de MongoDB conteniendo la API key provista
    user_data = users_collection.find_one({"apikey": apikey})

    #client.close()

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

        #client.close()

        return True

def authenticate(request, start_time):
    api_key = request.headers.get('Authorization')
    
    user_info = check_apikey(api_key)
    
    if user_info:
        if check_quota(api_key, start_time, user_info["group"]):
            return True, user_info
    
    return False, user_info
