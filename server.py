import json
import os
import random

from payos import PaymentData, PayOS
from flask import Flask, render_template, jsonify, request, send_from_directory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize PayOS with environment variables
payOS = PayOS(
    client_id=os.environ.get('PAYOS_CLIENT_ID'),
    api_key=os.environ.get('PAYOS_API_KEY'),
    checksum_key=os.environ.get('PAYOS_CHECKSUM_KEY')
)

app = Flask(__name__, static_folder='public', static_url_path='', template_folder='public')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/create_payment_link', methods=['POST'])
def create_payment():
    domain = "http://127.0.0.1:4242"  # Update the domain to use port 4242
    try:
        paymentData = PaymentData(
            orderCode=random.randint(1000, 99999),
            amount=10000,
            description="demo",
            cancelUrl=f"{domain}/detail.html",
            returnUrl=f"{domain}/successful_payment.html"
        )
        payosCreatePayment = payOS.createPaymentLink(paymentData)
        return jsonify(payosCreatePayment.to_json())
    except Exception as e:
        return jsonify(error=str(e)), 403
    
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('public/files', filename)

if __name__ == "__main__":
    app.run(port=4242)
