from flask import request
from microservices import db

def check_apikey(apikey):
    client = db.get_db()
    users_collection = client.topicos2.users

    # Busco el Documento de MongoDB conteniendo la API key provista
    user_data = users_collection.find_one({"apikey": apikey})

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
