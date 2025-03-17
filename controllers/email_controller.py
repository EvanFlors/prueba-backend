import os
import re
import requests
from dotenv import load_dotenv
from flask import request, jsonify
import google.generativeai as genai

# Configurar la API de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def fetchAdvices(results):
    try:
        # Crear un único prompt para cada sección
        prompt = ""
        
        for section in results:
            prompt += f"Proporciona consejos para mejorar la sección '{section['section']}'.\n"
            prompt += "Enfócate en las siguientes preguntas:\n"
            
            for response in section['responses']:
                if response['answer'] == '0' or response['answer'] == '1':
                    prompt += f"- {response['question']}\n"
            
            prompt += "\n"  # Separador entre secciones para claridad

        prompt += "Para cada seccion da un consejo general sobre la seccion en un parrafo y posteriormente da consejos especificos."
        prompt += "El formato debe ser: Nombre de seccion, consejo general, consejos especificos."
        
        # Solicitud a Gemini para generar los consejos
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        raise Exception(f"Error al generar consejos con Gemini: {str(e)}")

class EmailController:
  
  @staticmethod
  def send_advice():
    try:
      # Obtener datos de la solicitud
      data = request.json
      advice = fetchAdvices(data.get('results'))

      advice = advice.replace("*", "")

      return jsonify(advice), 200

    except Exception as e:
      # Manejo de errores
      return jsonify({
        "error": "Error interno del servidor",
        "details": str(e)
      }), 500

  
  @staticmethod
  def send_email():
    try:
        data = request.json
        from_email = data.get('from')
        to_email = data.get('to')
        subject = data.get('subject')
        results = data.get('results')

        # Obtener los consejos para cada sección
        advice = fetchAdvices(results)

        # Generar el HTML del correo con los consejos
        html = "<h1>Consultoría personalizada</h1>"

        # Procesar los consejos generados
        advice = advice.split("\n")  # Separar el texto por saltos de línea
        
        # Crear el HTML con formato
        formatted_advice = ""
        section_title = ""
        for line in advice:
            if line.startswith("## "):  # Detecta el inicio de una sección
                section_title = line[3:].strip()
            elif line.startswith("**Consejo general:"):  # Detecta el consejo general
                formatted_advice += f"<strong>{line[18:].strip()}</strong><br><br>"
            elif line.startswith("**") and "Consejo específicos" not in line:  # Detecta una pregunta problemática
                formatted_advice += f"<strong>{line[2:].strip()}</strong><br>"  # Pregunta en negrita
            elif line.startswith("*"):  # Detecta un consejo específico
                formatted_advice += f"<ul><li>{line[2:].strip()}</li></ul>"  # Consejos en lista numerada
            elif line.strip():  # Si es una línea de texto normal
                formatted_advice += f"<p>{line.strip()}</p>"

        # Agregar la última sección si existe
        if section_title:
            formatted_advice += f"<h2>{section_title}</h2>"

        # Generar el HTML completo con los consejos
        html += formatted_advice.replace("**", "")

        # Enviar el correo
        response = requests.post(
            'https://api.resend.com/emails',
            json={
                "from": from_email,
                "to": to_email,
                "subject": subject,
                "html": html
            },
            headers={
                "Authorization": f"Bearer {os.getenv('RESEND_API_KEY')}",
                "Content-Type": "application/json"
            }
        )

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                "error": "Error al enviar el correo",
                "details": response.text
            }), response.status_code
    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500