from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
import os
from ascii_art import generate_tombstone

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})

# Determinar si estamos en modo local o en la nube
IS_LOCAL = os.environ.get('IS_LOCAL', 'false').lower() == 'true'

if IS_LOCAL:
    import serial
    import time
    ARDUINO_PORT = '/dev/ttyUSB0'
    BAUD_RATE = 9600

def print_certificate(url, message, timestamp):
    try:
        if not IS_LOCAL:
            return False
            
        # Conectar con Arduino (solo en modo local)
        arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        tombstone = generate_tombstone(url, message, timestamp)
        arduino.write(tombstone.encode())
        arduino.close()
        return True
    except Exception as e:
        print(f"Error de impresión: {str(e)}")
        return False

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "API está funcionando",
        "endpoints": {
            "/check-url": "POST - Verifica si una URL está rota"
        }
    })

@app.route('/check-url', methods=['POST'])
def check_url():
    data = request.json
    url = data.get('url')
    message = data.get('message', 'Rest In Peace')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
        
    try:
        base_url = "http://archive.org/wayback/available"
        params = {'url': url}
        response = requests.get(base_url, params=params)
        
        timestamp = datetime.now().isoformat()
        
        if response.status_code == 200:
            data = response.json()
            is_broken = not data.get('archived_snapshots')
            
            if is_broken:
                # Generar el arte ASCII siempre
                tombstone = generate_tombstone(url, message, timestamp)
                
                # Intentar imprimir solo si estamos en modo local
                printed = print_certificate(url, message, timestamp) if IS_LOCAL else False
                
                return jsonify({
                    'is_broken': True,
                    'timestamp': timestamp,
                    'certificate_printed': printed,
                    'message': message,
                    'ascii_art': tombstone  # Incluimos el arte ASCII en la respuesta
                })
            else:
                return jsonify({
                    'is_broken': False,
                    'timestamp': timestamp
                })
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)