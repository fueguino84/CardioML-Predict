from flask import request
from microservices import db

def check_apikey(apikey):
    # Establezco conexión con la base de datos MongoDB y selecciono la base de datos
    client = db.get_db()
    db1 = client.topicos2

    # Selecciono la colección donde almaceno los usuarios y sus API keys
    users_collection = db1.users

    # Busco el Documento de MongoDB conteniendo la API key provista
    user_data = users_collection.find_one({"apikey": apikey})

    # Cierro la conexión con la base de datos
    #client.close()

    return user_data

def check_quota():
    return True

def authenticate(request):
    api_key = request.headers.get('Authorization')
    
    #print("API KEY: ",api_key)
    
    user_info = check_apikey(api_key)
    
    if user_info:
        if check_quota():
            return True, user_info
    
    return False, user_info
