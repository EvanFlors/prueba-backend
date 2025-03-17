from bson.objectid import ObjectId
from config.database import dbConnection

db = dbConnection()

class QuestionModel:
    @staticmethod
    def get_all():
        return db["questions"].find()

    @staticmethod
    def get_by_id(question_id):
        return db["questions"].find_one({"_id": ObjectId(question_id)})

    @staticmethod
    def get_by_question(question_text):
        return db["questions"].find_one({"question": question_text})

    @staticmethod
    def save(question):
        return db["questions"].insert_one(question)

    @staticmethod
    def update(question_id, update_data):
        return db["questions"].update_one(
            {"_id": ObjectId(question_id)},
            {"$set": update_data}
        )

    @staticmethod
    def delete(question_id):
        return db["questions"].find_one_and_delete({"_id": ObjectId(question_id)})
