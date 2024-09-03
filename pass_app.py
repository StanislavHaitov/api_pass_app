# Initialize the Flask application
from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample list of passwords
# This should be stored securely, preferably in a database
passwords = [
    {"id": 1, "username": "example.com", "password": "password123"},
    {"id": 2, "username": "github.com", "password": "securepass456"},
    {"id": 3, "username": "email.com", "password": "emailpass789"},
    {"id": 4, "username": "hard.work", "password": "sucsses"},
    {"id": 5, "username": "no.work", "password": "lazy"},
    {"id": 6, "username": "minikube.test", "password": "worked"},
    {"id": 7, "username": "no.go", "password": "go"}
]

# Route to get all passwords
@app.route('/password/', methods=['GET'])
def get_passwords():
    return jsonify(passwords)
    
# Route to Retrieve a specific password by its ID
@app.route('/password/<int:password_id>/', methods=['GET'])
def get_password(password_id):
    password = next((password for password in passwords if password["id"] == password_id), None)
    if password:
        return jsonify(password)
    else:
        return jsonify({"error": "Password not found"}), 404

# Run the application
if __name__ == '__main__':
    # Start the Flask application
    app.run(host='0.0.0.0', port=5000)