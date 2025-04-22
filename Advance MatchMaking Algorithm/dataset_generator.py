import pandas as pd
import random

num_players = 10000

locations = ["Spain", "Argentina", "Mexico", "Italy", "France", "Sweden", "Portugal",
             "Belgium", "Netherlands", "United Kingdom", "United States", "United Arab Emirates",
             "Saudi Arabia", "Qatar", "Lebanon", "Brazil", "Chile", "Germany", "Denmark", "Finland"]

players_data_large = {
    "Age": [random.randint(18, 55) for _ in range(num_players)],
    "Gender": random.choices(["Male", "Female"], k=num_players),
    "Skill_Level": random.choices(["Beginner", "Intermediate", "Advanced", "Professional"], k=num_players),
    "Play_Time": random.choices(["Morning", "Afternoon", "Evening"], k=num_players),
    "Location": random.choices(locations, k=num_players),
    "Win_Rate": [random.randint(30, 90) for _ in range(num_players)], 
    "Total_Matches_Played": [random.randint(10, 500) for _ in range(num_players)],
    "Favorite_Court_Type": random.choices(["Indoor", "Outdoor", "Any"], k=num_players),
    "Average_Match_Duration": [random.randint(30, 120) for _ in range(num_players)],
    "Coach_Affiliation": random.choices(["Yes", "No"], k=num_players),
    "Rating_Score": [random.randint(1000, 2500) for _ in range(num_players)]  
}


df_large = pd.DataFrame(players_data_large)


file_path_large = "matchmaking_dataset_large.csv"
df_large.to_csv(file_path_large, index=False)

print("Dataset saved successfully:", file_path_large)
