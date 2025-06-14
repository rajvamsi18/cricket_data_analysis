import pandas as pd
import numpy as np
import os

# working directory to the project root
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Loading the data
print("Loading data...")
ball_by_ball = pd.read_csv('data/ball_by_ball.csv')
innings = pd.read_csv('data/innings.csv')

def check_run_calculations():
    """
    Checks for inconsistencies in run calculations:
    1. To verify total_runs_so_far matches the sum of individual run components
    2. To compare final ball-by-ball totals with innings totals
    """
    print("Checking run calculation issues...")
    
    # Create a copy to avoid warnings
    df = ball_by_ball.copy()
    
    # Fill NA values with 0 for run components
    run_columns = ['runs_off_bat', 'runs_wide', 'no_ball_penalty_runs', 'runs_bye', 'runs_leg_bye']
    for col in run_columns:
        df[col] = df[col].fillna(0)
    
    # Calculate expected total runs
    df['calculated_runs'] = df[run_columns].sum(axis=1)
    
    # Checking if there are differences between calculated and recorded runs
    df['run_difference'] = df['total_runs_so_far'] - df.groupby(['match_id', 'innings_number'])['calculated_runs'].cumsum()
    
    # Finding rows where the runs don't match
    run_issues = df[df['run_difference'] != 0].copy()
    
    if len(run_issues) > 0:
        print(f"Found {len(run_issues)} instances where calculated runs don't match total_runs_so_far")
        print("\nSample issues:")
        print(run_issues[['match_id', 'innings_number', 'over', 'ball_of_over', 'calculated_runs', 'total_runs_so_far', 'run_difference']].head())
        
        # Saving issues to CSV
        run_issues.to_csv('data/run_calculation_issues.csv', index=False)
        print("Run calculation issues saved to data/run_calculation_issues.csv")
    else:
        print("No run calculation issues found within ball-by-ball data.")
    
    # checking mismatches between ball-by-ball and innings data
    print("\nChecking mismatches between ball-by-ball and innings data...")
    
    # Get the final ball for each innings to compare with innings totals
    final_balls = df.loc[df.groupby(['match_id', 'innings_number'])['total_balls_so_far'].idxmax()]
    
    # Prepare for comparison
    comparison = []
    for _, final_ball in final_balls.iterrows():
        match_id = final_ball['match_id']
        innings_number = final_ball['innings_number']
        
        # Finding corresponding innings data
        innings_data = innings[(innings['match_id'] == match_id) & (innings['innings_number'] == innings_number)]
        
        if len(innings_data) > 0:
            innings_total = innings_data.iloc[0]['runs']
            ball_by_ball_total = final_ball['total_runs_so_far']
            
            if innings_total != ball_by_ball_total:
                comparison.append({
                    'match_id': match_id,
                    'innings_number': innings_number,
                    'ball_by_ball_total': ball_by_ball_total,
                    'innings_total': innings_total,
                    'difference': innings_total - ball_by_ball_total
                })
    
    comparison_df = pd.DataFrame(comparison)
    if len(comparison_df) > 0:
        print(f"Found {len(comparison_df)} innings with mismatched totals between datasets")
        print("\nMismatches:")
        print(comparison_df)
        
        # Saving to CSV
        comparison_df.to_csv('data/innings_total_mismatches.csv', index=False)
        print("Innings total mismatches saved to data/innings_total_mismatches.csv")
        
        return run_issues, comparison_df
    else:
        print("No mismatches found between ball-by-ball and innings totals.")
        return run_issues, None

if __name__ == "__main__":
    check_run_calculations()