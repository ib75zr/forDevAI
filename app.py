import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

USERS = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = USERS.get(id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
