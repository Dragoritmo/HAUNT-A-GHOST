from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})

@app.route('/check-url', methods=['POST'])
def check_url():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
        
    try:
        base_url = "http://archive.org/wayback/available"
        params = {'url': url}
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            # Si no hay snapshot disponible, probablemente es 404
            if not data.get('archived_snapshots'):
                return jsonify({
                    'is_broken': True,
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({
                    'is_broken': False,
                    'timestamp': datetime.now().isoformat()
                })
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        print("API running at http://localhost:5000/")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error starting API: {e}")