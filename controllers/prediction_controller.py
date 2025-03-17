from flask import request, jsonify
from chat import get_response

class PredictionController:
    @staticmethod
    def predict():
        text = request.get_json().get("message")
        if not text:
            return jsonify({"error": "No message provided"}), 400

        response = get_response(text)
        message = {"answer": response}
        return jsonify(message)