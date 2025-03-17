from flask import request, jsonify
from models.advice_model import AdviceModel
import random

class AdviceController:

    @staticmethod
    def get_advices_by_section():
        try:

            data = request.get_json()

            if not data or not data.get("section"):
                return jsonify({"error": "Invalid advice data"}), 400

            advices = list(AdviceModel.get_advice_by_section(data.get("section")))

            if not advices:
                return jsonify({"error": "No advice found in the given section"}), 404

            if len(advices) > 1:
                advice = random.choice(advices)
            else:
                advice = advices[0]

            advice["_id"] = str(advice["_id"])
            return jsonify(advice), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def save_advice():
        try:
            data = request.get_json()

            if not data or not data.get("advice") or len(data["advice"]) < 5:
                return jsonify({"error": "Invalid advice data"}), 400

            if not data.get("section"):
                return jsonify({"error": "No section provided"}), 400

            advice = {
                "advice": data.get("advice"),
                "section": data.get("section")
            }

            existing_advice = AdviceModel.get_advice_by_section(data["section"])
            if any(existing["advice"] == data["advice"] for existing in existing_advice):
                return jsonify({"error": "Advice already exists in this section"}), 400

            result = AdviceModel.save(advice)

            return jsonify({"message": "Advice saved successfully", "id": str(result.inserted_id)}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_advice():
        try:
            data = request.get_json()

            advice_id = data.get("id")
            update_data = data.get("update")

            if not advice_id or not update_data:
                return jsonify({"error": "Invalid data"}), 400

            data_to_update = {key: value for key, value in update_data.items() if value is not None}

            if not data_to_update:
                return jsonify({"error": "No valid data to update"}), 400

            result = AdviceModel.update(advice_id, data_to_update)

            if result.matched_count == 0:
                return jsonify({"error": "No advice found with the given ID"}), 404

            return jsonify({"message": "Advice updated successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_advice():
        try:
            data = request.get_json()
            advice_id = data.get("id")
            if not advice_id:
                return jsonify({"error": "No ID provided"}), 400

            AdviceModel.delete(advice_id)
            return jsonify({"message": "Advice deleted successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
