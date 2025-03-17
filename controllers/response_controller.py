from flask import request, jsonify
from models.response_model import ResponseModel

class ResponseController:
    @staticmethod
    def save_response():
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "No JSON data provided"}), 400

            # Save the response
            result = ResponseModel.save(data)

            return jsonify({"message": "Data saved successfully", "id": str(result.inserted_id)}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
