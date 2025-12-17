import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app) # STEVE: This stops the "Failed to connect" bar in the app

# Logic to load the key from Render or PC memory
creds_json = os.environ.get('FIREBASE_CONFIG')
if creds_json:
    cred = credentials.Certificate(json.loads(creds_json))
    firebase_admin.initialize_app(cred)
    db = firestore.client()

@app.route('/')
def home():
    return "API is Online", 200

@app.route('/specials/list', methods=['GET'])
def get_specials():
    try:
        docs = db.collection('specials').stream()
        return jsonify([doc.to_dict() for doc in docs]), 200
    except:
        return jsonify([]), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)