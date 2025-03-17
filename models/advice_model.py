from bson.objectid import ObjectId
from config.database import dbConnection

db = dbConnection()

class AdviceModel:

    @staticmethod
    def get_all():
        return db["advices"].find()

    @staticmethod
    def get_advice_by_section(section):
        return db["advices"].find({"section": section})

    @staticmethod
    def save(advice):
        return db["advices"].insert_one(advice)

    @staticmethod
    def update(advice_id, update_data):
        return db["advices"].update_one(
            {"_id": ObjectId(advice_id)},
            {"$set": update_data}
        )

    @staticmethod
    def delete(advice_id):
        return db["advices"].find_one_and_delete({"_id": ObjectId(advice_id)})
