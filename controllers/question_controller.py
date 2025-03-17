from flask import request, jsonify
from models.question_model import QuestionModel

class QuestionController:

    @staticmethod
    def get_questions():
        try:
            result = QuestionModel.get_all()
            grouped_questions = []

            for question in result:
                question["id"] = str(question["_id"])
                category = question.get("category")

                order = question.get("order")

                category_group = next((item for item in grouped_questions if item["title"] == category), None)

                if not category_group:
                    category_group = {
                        "title": category,
                        "order": order,
                        "questions": []
                    }
                    grouped_questions.append(category_group)

                category_group["questions"].append({
                    "id": question["id"],
                    "text": question["question"],
                })

            grouped_questions.sort(key=lambda x: x["order"])

            return jsonify(grouped_questions), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_question(id):
        try:
            question = QuestionModel.get_by_id(id)

            if not question:
                return jsonify({"error": "No question found with the given ID"}), 404

            question["_id"] = str(question["_id"])

            return jsonify(question), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def save_question():
        try:
            data = request.get_json()

            if not data or not data.get("question") or len(data["question"]) < 10:
                return jsonify({"error": "Invalid question data"}), 400

            if not data.get("category"):
                return jsonify({"error": "No question category provided"}), 400

            if not data.get("order"):
                return jsonify({"error": "No order category provided"}), 400

            if not data.get("type"):
                return jsonify({"error": "No question type provided"}), 400

            question = {
                "question": data.get("question"),
                "category": data.get("category"),
                "order": data.get("order"),
                "type": data.get("type")
            }

            existing_question = QuestionModel.get_by_question(question["question"])

            if existing_question:
                return jsonify({"error": "Question already exists"})

            result = QuestionModel.save(question)

            return jsonify({"message": "Data saved successfully", "id": str(result.inserted_id)}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_question():
        try:
            data = request.get_json()

            question_id = data.get("id")
            update_data = data.get("update")

            if not question_id or not update_data:
                return jsonify({"error": "Invalid data"}), 400

            data_to_update = {
                "question": update_data.get("question"),
                "order": update_data.get("order"),
                "type": update_data.get("type"),
                "category": update_data.get("category"),
            }

            data_to_update = {key: value for key, value in data_to_update.items() if value is not None}

            if not data_to_update:
                return jsonify({"error": "No valid data to update"}), 400

            result = QuestionModel.update(question_id, data_to_update)

            if result.matched_count == 0:
                return jsonify({"error": "No question found with the given ID"}), 404

            return jsonify({"message": "Question updated successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_question():
        try:
            data = request.get_json()
            question_id = data.get("id")
            if not question_id:
                return jsonify({"error": "No ID provided"}), 400
            QuestionModel.delete(question_id)
            return jsonify({"message": "Question deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
