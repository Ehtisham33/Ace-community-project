import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load sports rating data from JSON file
with open("assets/file.json", "r") as file:
    SPORTS_QUESTIONS = json.load(file)

@app.route("/questions/<sport>", methods=["GET"])
def get_questions(sport):
    if sport not in SPORTS_QUESTIONS:
        return jsonify({"error": "Sport not supported"}), 400
    return jsonify(SPORTS_QUESTIONS[sport])

@app.route("/questions", methods=["GET"])
def get_multiple_questions():
    sports = request.args.get("sports")
    if not sports:
        return jsonify({"error": "No sports provided"}), 400
    
    sports_list = sports.split(",")
    questions = {}
    
    for sport in sports_list:
        if sport in SPORTS_QUESTIONS:
            questions[sport] = SPORTS_QUESTIONS[sport]
        else:
            return jsonify({"error": f"Sport '{sport}' not supported"}), 400
    
    return jsonify(questions)

@app.route("/calculate_rating", methods=["POST"])
def calculate_rating():
    data = request.get_json()
    if "sports" not in data:
        return jsonify({"error": "Missing sports data"}), 400
    
    ratings = {}
    for sport, answers in data["sports"].items():
        if sport not in SPORTS_QUESTIONS:
            return jsonify({"error": f"Sport '{sport}' not supported"}), 400
        
        questions = SPORTS_QUESTIONS[sport]
        total_score = 0
        
        for question, answer in answers.items():
            if question in questions and answer in questions[question]["options"]:
                total_score += questions[question]["options"][answer]
            else:
                return jsonify({"error": f"Invalid answer for {question} in {sport}"}), 400
        
        ratings[sport] = round(total_score, 2)
    
    return jsonify({"ratings": ratings})

if __name__ == "__main__":
    app.run(debug=True)
