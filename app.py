from flask import Flask, request, jsonify
from flasgger import Swagger
import data

app = Flask(__name__)
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
    payload = request.json   # renamed to avoid shadowing `data`

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
# GET users by year
# -------------------------
@app.route("/users/year/<int:year>", methods=["GET"])
def users_by_year(year):
    """
    Get users by year
    ---
    parameters:
      - name: year
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Filtered list of users
    """
    filtered = [u for u in data.users if u["year"] == year]
    return jsonify(filtered)


# -------------------------
# GET age list (for charts)
# -------------------------
@app.route("/stats/age", methods=["GET"])
def age_stats():
    """
    Get ages of all users
    ---
    responses:
      200:
        description: List of ages
    """
    ages = [u["age"] for u in data.users]
    return jsonify(ages)


# -------------------------
# GET year counts (for charts)
# -------------------------
@app.route("/stats/year", methods=["GET"])
def year_stats():
    """
    Get user count by year
    ---
    responses:
      200:
        description: Count of users by year
    """
    counts = {}
    for u in data.users:
        y = u["year"]
        counts[y] = counts.get(y, 0) + 1
    return jsonify(counts)


# -------------------------
# Run the app
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
