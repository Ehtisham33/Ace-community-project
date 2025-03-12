from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_criteria():
    with open(r"D:\Glaxit Projects\padel_project\assets\file.json", "r") as file:
        return json.load(file)

score_criteria = load_criteria()

@app.route("/questions", methods=["GET"])
def get_questions():
    questions = [{"question": q["question"], "options": list(q["options"].keys())} for q in score_criteria["questions"]]
    return jsonify({"questions": questions})

@app.route("/calculate-rating", methods=["POST"])
def calculate_rating():
    data = request.json  
    total_score = 0
    
    for question in score_criteria["questions"]:
        answer = data.get(question["question"], "")
        total_score += question["options"].get(answer, 0)
    
    rating = 1
    for scale in score_criteria["rating_scale"]:
        if scale["min"] <= total_score <= scale["max"]:
            rating = scale["rating"]
            break
    
    return jsonify({"total_score": total_score, "rating": rating})

if __name__ == "__main__":
    app.run(debug=True)
