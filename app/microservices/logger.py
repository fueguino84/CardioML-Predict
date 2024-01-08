from microservices import db
from datetime import datetime

def log(json_data, result, start_time, user_info):
    client = db.get_db()
    log_collection = client.topicos2.log  

    end_time = datetime.now().timestamp()
    elapsed_time = end_time - start_time

    log_entry = {
        "start_time": start_time,
        "params": json_data,
        "response": result,
        "elapsed_time": elapsed_time,
        "end_time": end_time,
        "user_info": user_info
    }
    
    log_collection.insert_one(log_entry)
    client.close()
