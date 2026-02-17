from flask import Flask, request, jsonify
from flasgger import Swagger
from flask_cors import CORS
import data

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)


# -------------------------
# Root
# -------------------------
@app.route("/")
def home():
    return "API Playground is running. Visit /apidocs for Swagger UI."


# -------------------------
# GET all users
# -------------------------
@app.route("/users", methods=["GET"])
def get_users():
    """
    Get all users
    ---
    responses:
      200:
        description: A list of users
    """
    return jsonify(data.users)


# -------------------------
# POST a new user
# -------------------------
@app.route("/users", methods=["POST"])
def add_user():
    """
    Add a new user
    ---
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - age
            - year
          properties:
            name:
              type: string
            email:
              type: string
            age:
              type: integer
            year:
              type: integer
    responses:
      201:
        description: User created successfully
    """

    payload = request.json

    user = {
        "id": data.next_id,
        "name": payload["name"],
        "email": payload["email"],
        "age": payload["age"],
        "year": payload["year"]
    }

    data.users.append(user)
    data.next_id += 1

    return jsonify(user), 201


# -------------------------
# POST batch users
# -------------------------
@app.route("/users/batch", methods=["POST"])
def batch_add_users():
    """
    Batch add users
    ---
    parameters:
      - in: body
        name: users
        required: true
        schema:
          type: array
          items:
            type: object
            required:
              - name
              - email
              - age
              - year
            properties:
              name:
                type: string
              email:
                type: string
              age:
                type: integer
              year:
                type: integer
    responses:
      201:
        description: Users created successfully
    """

    payload = request.json

    new_users = []

    for item in payload:

        user = {
            "id": data.next_id,
            "name": item["name"],
            "email": item["email"],
            "age": item["age"],
            "year": item["year"]
        }

        data.users.append(user)
        new_users.append(user)

        data.next_id += 1

    return jsonify(new_users), 201


# -------------------------
# PATCH update user
# -------------------------
@app.route("/users/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    """
    Update user partially
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true

      - in: body
        name: user
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            age:
              type: integer
            year:
              type: integer

    responses:
      200:
        description: Updated user
      404:
        description: User not found
    """

    payload = request.json

    for user in data.users:

        if user["id"] == user_id:

            user.update(payload)

            return jsonify(user)

    return jsonify({"error": "User not found"}), 404


# -------------------------
# DELETE user
# -------------------------
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete user
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true

    responses:
      200:
        description: User deleted
      404:
        description: User not found
    """

    for i, user in enumerate(data.users):

        if user["id"] == user_id:

            deleted = data.users.pop(i)

            return jsonify(deleted)

    return jsonify({"error": "User not found"}), 404


# -------------------------
# GET users by year
# -------------------------
@app.route("/users/year/<int:year>", methods=["GET"])
def users_by_year(year):

    filtered = [u for u in data.users if u["year"] == year]

    return jsonify(filtered)


# -------------------------
# GET age stats
# -------------------------
@app.route("/stats/age", methods=["GET"])
def age_stats():

    ages = [u["age"] for u in data.users]

    return jsonify(ages)


# -------------------------
# GET year stats
# -------------------------
@app.route("/stats/year", methods=["GET"])
def year_stats():

    counts = {}

    for u in data.users:

        y = u["year"]

        counts[y] = counts.get(y, 0) + 1

    return jsonify(counts)


# -------------------------
# Health check
# -------------------------
@app.route("/healthz")
def health():

    return {"status": "ok"}


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
