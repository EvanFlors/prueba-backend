from config.database import dbConnection

db = dbConnection()

class ResponseModel:
    @staticmethod
    def save(response):
        db = dbConnection()
        return db["responses"].insert_one(response)