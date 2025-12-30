from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from api.routes import api_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "GitHub README Stats Generator API is running"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
