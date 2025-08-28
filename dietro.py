from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB (update the URI with your MongoDB URL)
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/TreasureHuntDB?retryWrites=true&w=majority")
db = client["TreasureHuntDB"]  # Database name

app = Flask(__name__)

@app.after_request
def add_csp_header(response):
    response.headers["Content-Security-Policy"] = "default-src 'self';"
    return response

# Define a route for GET requests
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

# Define a route for POST requests
@app.route("/post", methods=["POST"])
def handle_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    # Validate the expected keys
    if "station" not in data or "team" not in data:
        return jsonify({"error": "Invalid JSON payload. 'station' and 'team' are required."}), 400

    # Process the data
    station = data["station"]
    team = data["team"]

    return jsonify({
        "message": "POST request received!",
        "station": station,
        "team": team
    }), 200

# Define a route for GET requests with dynamic stationid and teamid
@app.route("/<int:stationid>/<int:teamid>", methods=["GET"])
def handle_get_station_team(stationid, teamid):
    # Save the stationid and teamid in Python variables
    station = stationid
    team = teamid

    # Get or create the collection for the station
    collection = db[station]

    # Insert the team ID and timestamp into the collection
    collection.insert_one({
        "team": team,
        "timestamp": datetime.utcnow()
    })

    # Return the extracted values
    return jsonify({
        "message": "GET request received!",
        "station": station,
        "team": team
    }), 200

# Define a route for handling 404 errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "404 Not Found"}), 404

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)