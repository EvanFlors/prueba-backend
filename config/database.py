import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()

MONGO_URI=os.getenv("MONGO_URI")
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI)
        db = client["PracticasPyme"]
        print(client)
        print(db)
    except ConnectionError:
        print("Error de conexión con la base de datos")
    return db
