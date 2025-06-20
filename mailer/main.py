import resend
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

RESEND_EMAIL = os.getenv("RESEND_EMAIL", "")

app = Flask(__name__)

@app.post("/send-welcome")
def index():
  
  body = request.get_json()
  if not body or not body.get("email"):
    return jsonify({"error": "Email is required"}), 400
  params = {
    "from": RESEND_EMAIL,
    "to": [body["email"]],
    "subject": "Bienvenido a nuestra aplicación",
    "html": "<strong>Hola</strong>",
  }

  r = resend.Emails.send(params)
  return jsonify(r)

if __name__ == "__main__":
  
  environment = os.getenv('ENVIRONMENT', 'development')
  app.run(
        host = '0.0.0.0', 
        port = 8091, 
        debug = (environment == 'development'),
  )
