import pandas as pd
import random

num_players = 10000

locations = ["Spain", "Argentina", "Mexico", "Italy", "France", "Sweden", "Portugal","Belgium", "Netherlands", "United Kingdom", "United States", "United Arab Emirates","Saudi Arabia", "Qatar", "Lebanon", "Brazil", "Chile", "Germany", "Denmark", "Finland"]


players_data_large = {
    "Age": random.sample(range(18, 55), num_players), 
    "Gender": [random.choice(["Male", "Female"]) for _ in range(num_players)],
    "Skill_Level": [random.choice(["Beginner", "Intermediate", "Advanced", "Professional"]) for _ in range(num_players)],
    "Play_Time": [random.choice(["Morning", "Afternoon", "Evening"]) for _ in range(num_players)],
    "Location": random.choices(locations, k=num_players),
    "Win_Rate": random.sample(range(30, 91), num_players),  
    "Total_Matches_Played": random.sample(range(10, 501), num_players),
    "Favorite_Court_Type": [random.choice(["Indoor", "Outdoor", "Any"]) for _ in range(num_players)],
    "Average_Match_Duration": random.sample(range(30, 121), num_players),
    "Coach_Affiliation": [random.choice(["Yes", "No"]) for _ in range(num_players)],
    "Rating_Score": random.sample(range(1000, 2501), num_players)  
}


df_large = pd.DataFrame(players_data_large)


file_path_large = "matchmaking_dataset_large.csv"
df_large.to_csv(file_path_large, index=False)

file_path_large
