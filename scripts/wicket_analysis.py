import pandas as pd
import numpy as np
import os

# working directory to the project root
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Loading the data
print("Loading ball-by-ball data...")
ball_by_ball = pd.read_csv('data/ball_by_ball.csv')

def check_wicket_information():
    """
    Checks for incomplete dismissal details in wicket records
    """
    print("Checking for missing wicket information...")
    
    # a copy to avoid warnings
    df = ball_by_ball.copy()
    
    # Finding balls where a wicket occurred (wicket_type is not null)
    wicket_balls = df[df['wicket_type'].notna() | df['wicket_number'].notna()].copy()
    
    # Checking for missing batter or bowler information
    wicket_balls['missing_out_batter'] = wicket_balls['out_batter_id'].isna() | wicket_balls['out_batter_name'].isna()
    
    # Counting missing information
    missing_batter_info = wicket_balls[wicket_balls['missing_out_batter']].copy()
    
    if len(missing_batter_info) > 0:
        print(f"Found {len(missing_batter_info)} wickets with missing batter information")
        print("\nSample missing batter information:")
        print(missing_batter_info[['match_id', 'innings_number', 'over', 'ball_of_over', 'wicket_number','wicket_type', 'out_batter_id', 'out_batter_name']].head())
        
        # Saving to CSV
        missing_batter_info.to_csv('data/missing_wicket_information.csv', index=False)
        print("Missing wicket information saved to data/missing_wicket_information.csv")
        
    else:
        print("No missing wicket information found.")
        return None

if __name__ == "__main__":
    check_wicket_information()