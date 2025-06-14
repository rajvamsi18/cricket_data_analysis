import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# working directory to the project root
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Loading the data
print("Loading ball-by-ball data...")
ball_by_ball = pd.read_csv('data/ball_by_ball.csv')

def check_legal_ball_counting():
    """
    Checks for issues where legal_ball_of_over incorrectly increments for 
    wide balls and no-balls within each over.
    """
    print("Checking legal ball counting issues...")
    
    # copy to avoid warnings
    df = ball_by_ball.copy()
    
    # Identifying extras (wides and no-balls)
    df['is_wide'] = df['runs_wide'].notna() & (df['runs_wide'] > 0)
    df['is_noball'] = df['no_ball_penalty_runs'].notna() & (df['no_ball_penalty_runs'] > 0)
    df['is_extra'] = df['is_wide'] | df['is_noball']
    
    # Finding issues where legal_ball_of_over increments from previous ball for extras
    issues = []
    
    for (match_id, innings_number, over), group in df.groupby(['match_id', 'innings_number', 'over']):
        # Sort by ball_of_over to ensure correct sequence
        group = group.sort_values('ball_of_over').reset_index()
        
        # Track the previous legal_ball_of_over value
        prev_legal_ball = None
        
        for i, row in group.iterrows():
            # Checking if this is an extra (wide or no-ball)
            if row['is_extra']:
                # If we have a previous legal ball value to compare
                if prev_legal_ball is not None and pd.notna(row['legal_ball_of_over']):
                    # Check if legal_ball_of_over incremented for this extra
                    if row['legal_ball_of_over'] > prev_legal_ball:
                        issues.append({
                            'match_id': match_id,
                            'innings_number': innings_number,
                            'over': over,
                            'ball_of_over': row['ball_of_over'],
                            'legal_ball_of_over': row['legal_ball_of_over'],
                            'previous_legal_ball': prev_legal_ball,
                            'extra_type': 'Wide' if row['is_wide'] else 'No ball',
                            'runs_wide': row['runs_wide'] if pd.notna(row['runs_wide']) else 0,
                            'no_ball_penalty_runs': row['no_ball_penalty_runs'] if pd.notna(row['no_ball_penalty_runs']) else 0
                        })
            
            # Updating previous legal ball value if this ball has one
            if pd.notna(row['legal_ball_of_over']):
                prev_legal_ball = row['legal_ball_of_over']
    
    if issues:
        issues_df = pd.DataFrame(issues)
        print(f"Found {len(issues_df)} instances where legal_ball_of_over incorrectly increments for extras")
        print("\nSample issues:")
        print(issues_df.head())
        
        # Grouping by match and over to see pattern
        issue_counts = issues_df.groupby(['match_id', 'innings_number', 'over']).size().reset_index(name='issue_count')
        print("\nIssues per over:")
        print(issue_counts.sort_values('issue_count', ascending=False).head(10))
        
        # example for the report
        example = issues_df[issues_df['match_id'] == 1443098]
        if len(example) > 0:
            print("\nExample for report (Match 1443098):")
            print(example.head())
            
            # Showing the full sequence of balls in this over
            for (match, innings, over) in example[['match_id', 'innings_number', 'over']].values[:1]:
                full_over = df[(df['match_id'] == match) & (df['innings_number'] == innings) & (df['over'] == over)]
                full_over_sorted = full_over.sort_values('ball_of_over')
                print(f"\nFull sequence for match {match}, innings {innings}, over {over}:")
                print(full_over_sorted[['ball_of_over', 'legal_ball_of_over', 'is_wide', 'is_noball', 'runs_wide', 'no_ball_penalty_runs']])
        
        # Saving the issues to a CSV file
        issues_df.to_csv('data/legal_ball_increment_issues.csv', index=False)
        print("All issues saved to data/legal_ball_increment_issues.csv")
        
        return issues_df
    else:
        print("No legal ball increment issues found for extras.")
        return None

if __name__ == "__main__":
    check_legal_ball_counting()