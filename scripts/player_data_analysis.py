import pandas as pd
import numpy as np
import os

# working directory to the project root
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Loading the data
print("Loading data...")
ball_by_ball = pd.read_csv('data/ball_by_ball.csv')
players = pd.read_csv('data/players.csv')

def check_player_data():
    """
    Checks for missing player information and non-facing batter details
    """
    print("Checking for player data issues...")
    
    # 1. Check for missing player attributes in players.csv
    print("\n1. Checking for missing player attributes...")
    
    # Count missing attributes
    missing_attributes = players[
        (players['batting_hand'].isna()) | 
        (players['bowling_type'].isna())
    ].copy()
    
    if len(missing_attributes) > 0:
        print(f"Found {len(missing_attributes)} players with missing attributes")
        print("\nSample players with missing attributes:")
        print(missing_attributes.head())
        
        # Saving to CSV
        missing_attributes.to_csv('data/missing_player_attributes.csv', index=False)
        print("Missing player attributes saved to data/missing_player_attributes.csv")
        

    else:
        print("No players with missing attributes found.")


    # 2. Checks for missing non-facing batter details
    print("\n2. Checking for missing non-facing batter details...")

    # balls with missing non-facing batter info
    missing_non_facing = ball_by_ball[
        (ball_by_ball['non_facing_batter_id'].isna()) | 
        (ball_by_ball['non_facing_batter_name'].isna())
    ].copy()

    if len(missing_non_facing) > 0:
        print(f"Found {len(missing_non_facing)} balls with missing non-facing batter details ({len(missing_non_facing)/len(ball_by_ball)*100:.2f}% of all balls)")
        
        # Group by match and innings to see the pattern
        missing_by_match = missing_non_facing.groupby(['match_id', 'innings_number']).size().reset_index(name='count')
        print("\nDistribution of missing non-facing batter details by match and innings:")
        print(missing_by_match)
        
        print("\nSample balls with missing non-facing batter details:")
        print(missing_non_facing[['match_id', 'innings_number', 'over', 'ball_of_over', 'facing_batter_name', 'non_facing_batter_id', 'non_facing_batter_name']].head())
        
        # Saving to CSV
        missing_non_facing.to_csv('data/missing_non_facing_batter.csv', index=False)
        print("Missing non-facing batter details saved to data/missing_non_facing_batter.csv")
        
        return missing_attributes, missing_non_facing
    else:
        print("No balls with missing non-facing batter details found.")
        return missing_attributes, None

if __name__ == "__main__":
    check_player_data()