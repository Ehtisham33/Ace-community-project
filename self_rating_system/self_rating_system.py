import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

# Load sports rating data from JSON file
with open("assets/file.json", "r") as file:
    SPORTS_QUESTIONS = json.load(file)

class RatingRequest(BaseModel):
    sports: Dict[str, Dict[str, str]]  # Dictionary of sports with their answers

@app.get("/questions/{sport}")
def get_questions(sport: str):
    if sport not in SPORTS_QUESTIONS:
        raise HTTPException(status_code=400, detail="Sport not supported")
    return SPORTS_QUESTIONS[sport]

@app.get("/questions")
def get_multiple_questions(sports: str):
    sports_list = sports.split(",")
    questions = {}
    
    for sport in sports_list:
        if sport in SPORTS_QUESTIONS:
            questions[sport] = SPORTS_QUESTIONS[sport]
        else:
            raise HTTPException(status_code=400, detail=f"Sport '{sport}' not supported")
    
    return questions

@app.post("/calculate_rating")
def calculate_rating(request: RatingRequest):
    ratings = {}
    
    for sport, answers in request.sports.items():
        if sport not in SPORTS_QUESTIONS:
            raise HTTPException(status_code=400, detail=f"Sport '{sport}' not supported")
        
        questions = SPORTS_QUESTIONS[sport]
        total_score = 0
        
        for question, answer in answers.items():
            if question in questions and answer in questions[question]["options"]:
                total_score += questions[question]["options"][answer]
            else:
                raise HTTPException(status_code=400, detail=f"Invalid answer for {question} in {sport}")
        
        ratings[sport] = round(total_score, 2)
    
    return {"ratings": ratings}

# Run using: uvicorn script_name:app --reload
