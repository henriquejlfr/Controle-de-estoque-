from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'data.json'

# ---------------- Utils ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "items": []}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ---------------- Auth ----------------
@app.route('/api/login', methods=['POST'])
def login():
    data = load_data()
    body = request.json
    for user in data['users']:
        if user['username'] == body['username'] and user['password'] == body['password']:
            return jsonify(user)
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/users', methods=['POST'])
def create_user():
    data = load_data()
    body = request.json
    data['users'].append(body)
    save_data(data)
    return jsonify({"msg": "User created"})

# ---------------- Items ----------------
@app.route('/api/items', methods=['GET'])
def get_items():
    data = load_data()
    return jsonify(data['items'])

@app.route('/api/items', methods=['POST'])
def add_item():
    data = load_data()
    body = request.json
    data['items'].append(body)
    save_data(data)
    return jsonify({"msg": "Item added"})

@app.route('/api/items/<name>', methods=['DELETE'])
def delete_item(name):
    data = load_data()
    data['items'] = [i for i in data['items'] if i['name'] != name]
    save_data(data)
    return jsonify({"msg": "Item removed"})

# ---------------- Run ----------------
if __name__ == '__main__':
    app.run(debug=True)