from flask import Flask
from flask_cors import CORS
from controllers.question_controller import QuestionController
from controllers.response_controller import ResponseController
from controllers.prediction_controller import PredictionController
from controllers.advice_controller import AdviceController 
from controllers.email_controller import EmailController 
import os  # Import os to access environment variables

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index():
  return "Hello, World!"

# Rutas para el controlador de preguntas
app.add_url_rule("/get/questions", view_func=QuestionController.get_questions, methods=["GET"])
app.add_url_rule("/get/question/<id>", view_func=QuestionController.get_question, methods=["GET"])
app.add_url_rule("/save/question", view_func=QuestionController.save_question, methods=["POST"])
app.add_url_rule("/update/question", view_func=QuestionController.update_question, methods=["PUT"])
app.add_url_rule("/delete/question", view_func=QuestionController.delete_question, methods=["DELETE"])

# Rutas para el controlador de respuestas
app.add_url_rule("/save/response", view_func=ResponseController.save_response, methods=["POST"])

# Rutas para el controlador de predicción
app.add_url_rule("/predict", view_func=PredictionController.predict, methods=["POST"])

# Rutas para el controlador de consejos (Advice)
app.add_url_rule("/get/advice", view_func=AdviceController.get_advices_by_section, methods=["POST"])  #
app.add_url_rule("/save/advice", view_func=AdviceController.save_advice, methods=["POST"])
app.add_url_rule("/update/advice", view_func=AdviceController.update_advice, methods=["PUT"])
app.add_url_rule("/delete/advice", view_func=AdviceController.delete_advice, methods=["DELETE"])

# Endpoint para enviar correos
app.add_url_rule('/send-email', view_func=EmailController.send_email, methods=['POST'])
app.add_url_rule('/advices', view_func=EmailController.send_advice, methods=['POST'])

if __name__ == "__main__":
  # Bind to the PORT environment variable or default to 5000
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
