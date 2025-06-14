import pandas as pd
import numpy as np
import os

# working directory to the project root
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Loading data
print("Loading data...")
ball_by_ball = pd.read_csv('data/ball_by_ball.csv')
innings = pd.read_csv('data/innings.csv')

def check_innings_endings():
    """
    Checks for unexplained innings endings
    """
    print("Checking for unexplained innings endings...")
    
    # Getting the maximum over for each innings from ball-by-ball data
    max_overs = ball_by_ball.groupby(['match_id', 'innings_number'])['over'].max().reset_index()
    max_overs.columns = ['match_id', 'innings_number', 'max_over_played']
    
    # Merge with innings data
    merged = innings.merge(max_overs, on=['match_id', 'innings_number'])
    
    # Calculating wickets for each innings from ball-by-ball data
    final_balls = ball_by_ball.loc[ball_by_ball.groupby(['match_id', 'innings_number'])['total_balls_so_far'].idxmax()]
    wickets_df = final_balls[['match_id', 'innings_number', 'total_wickets_so_far']].copy()
    merged = merged.merge(wickets_df, on=['match_id', 'innings_number'])
    
    # Find innings that ended early
    early_endings = merged[
        (merged['max_over_played'] < merged['final_over_limit']) & 
        (merged['total_wickets_so_far'] < 10)
    ].copy()
    
    # For second innings, checking if they reached the target
    second_innings = early_endings[early_endings['innings_number'] == 2].copy()
    if len(second_innings) > 0:
        # Check if target was reached
        second_innings['target_reached'] = second_innings['runs'] >= second_innings['target']
        early_second_innings = second_innings[~second_innings['target_reached']].copy()
    else:
        early_second_innings = pd.DataFrame()
    
    # Combining early first innings and early second innings that didn't reach target
    early_first_innings = early_endings[early_endings['innings_number'] == 1].copy()
    unexplained_endings = pd.concat([early_first_innings, early_second_innings])
    
    if len(unexplained_endings) > 0:
        print(f"Found {len(unexplained_endings)} innings that ended prematurely without explanation")
        print("\nUnexplained innings endings:")
        print(unexplained_endings[['match_id', 'innings_number', 'max_over_played', 'final_over_limit', 'total_wickets_so_far', 'runs', 'target']])
        
        # Saving to CSV
        unexplained_endings.to_csv('data/unexplained_innings_endings.csv', index=False)
        print("Unexplained innings endings saved to data/unexplained_innings_endings.csv")
        
        return unexplained_endings
    else:
        print("No unexplained innings endings found.")
        return None

def check_null_values():
    """
    Checks for null values in critical fields
    """
    print("\nChecking for null values in critical fields...")
    
    # List of critical fields to check
    critical_fields = ['no_ball_penalty_runs', 'runs_bye', 'runs_leg_bye', 'runs_wide', 'wicket_type']
    
    # Calculating null percentages
    null_stats = []
    for field in critical_fields:
        null_count = ball_by_ball[field].isna().sum()
        null_percent = null_count / len(ball_by_ball) * 100
        null_stats.append({
            'field': field,
            'null_count': null_count,
            'total_count': len(ball_by_ball),
            'null_percent': null_percent
        })
    
    null_stats_df = pd.DataFrame(null_stats)
    print("\nNull value statistics:")
    print(null_stats_df)
    
    # Saving to CSV
    null_stats_df.to_csv('data/null_value_statistics.csv', index=False)
    print("Null value statistics saved to data/null_value_statistics.csv")
    
    return null_stats_df

def check_bowler_statistics():
    """
    Checks for inconsistent bowler statistics by examining the unique values
    of bowler_balls_bowled in each over
    """
    print("\nChecking for bowler statistics issues...")
    
    # Creating a copy of the dataframe
    df = ball_by_ball.copy()
    
    issues = []

    # Group by match, innings, and bowler
    for (match_id, innings_number, bowler_id), bowler_data in df.groupby(['match_id', 'innings_number', 'bowler_id']):
        bowler_name = bowler_data['bowler_name'].iloc[0]
        
        # Determine which overs this bowler bowled
        bowler_overs = bowler_data['over'].unique()
        bowler_overs.sort()
        
        # Calculating which over number this is for the bowler (1st, 2nd, 3rd, 4th)
        for i, over_num in enumerate(bowler_overs):
            # This is the bowler's (i+1)th over (0-indexed -> 1-indexed)
            bowler_over_number = i + 1
            
            # data for this specific over
            over_data = bowler_data[bowler_data['over'] == over_num].copy()
            
            # unique legal_ball_of_over values (should be 1-6)
            legal_balls = over_data['legal_ball_of_over'].dropna().unique()
            legal_balls.sort()
            
            # unique bowler_balls_bowled values
            bowler_balls = over_data['bowler_balls_bowled'].dropna().unique()
            bowler_balls.sort()
            
            # Expected values based on which over this is for the bowler
            expected_start = (bowler_over_number - 1) * 6 + 1
            expected_end = bowler_over_number * 6
            expected_balls = list(range(expected_start, expected_end + 1))
            
            # Checking if the values match the expected pattern
            if not np.array_equal(bowler_balls, expected_balls):
                # Only report if this isn't just due to missing data (incomplete over)
                if len(legal_balls) == len(expected_balls) or any(ball not in expected_balls for ball in bowler_balls):
                    issues.append({
                        'match_id': match_id,
                        'innings_number': innings_number,
                        'over_num': over_num,
                        'bowler_id': bowler_id,
                        'bowler_name': bowler_name,
                        'bowler_over_number': bowler_over_number,
                        'actual_balls': ', '.join(map(str, bowler_balls)),
                        'expected_balls': ', '.join(map(str, expected_balls)),
                        'legal_balls_count': len(legal_balls),
                        'expected_balls_count': len(expected_balls)
                    })
    
    if issues:
        issues_df = pd.DataFrame(issues)
        
        print(f"Found {len(issues_df)} overs with inconsistent bowler ball counts")
        print("\nSample bowler ball count issues:")
        print(issues_df.head())
        
        # Looking for the specific example (Shaheen Shah Afridi in match 1459548)
        shaheen_issues = issues_df[(issues_df['bowler_name'] == 'Shaheen Shah Afridi') & 
                                  (issues_df['match_id'] == 1459548)]
        if len(shaheen_issues) > 0:
            print("\nShaheen Shah Afridi issues in match 1459548:")
            print(shaheen_issues)
            
            # Get all Shaheen's balls in this match/innings to analyze pattern
            shaheen_balls = df[(df['match_id'] == 1459548) & 
                              (df['innings_number'] == 1) & 
                              (df['bowler_name'] == 'Shaheen Shah Afridi')]
            
            # Group by over to see the pattern clearly
            for over_num, over_group in shaheen_balls.groupby('over'):
                print(f"\nOver {over_num} (sorted by ball_of_over):")
                over_data = over_group.sort_values('ball_of_over')
                print(over_data[['ball_of_over', 'legal_ball_of_over', 'bowler_balls_bowled']])

        # Looking for the specific example (Tristan Luus in match 1449663)
        tristan_issues = issues_df[(issues_df['bowler_name'] == 'Tristan Luus') & 
                                  (issues_df['match_id'] == 1449663)]
        if len(tristan_issues) > 0:
            print("\nTristan Luus issues in match 1449663:")
            print(tristan_issues)
            
            # Get all Tristan's balls in this match/innings to analyze pattern
            tristan_balls = df[(df['match_id'] == 1449663) & 
                              (df['innings_number'] == 2) & 
                              (df['bowler_name'] == 'Tristan Luus')]
            
            # Group by over to see the pattern clearly
            for over_num, over_group in tristan_balls.groupby('over'):
                print(f"\nOver {over_num} (sorted by ball_of_over):")
                over_data = over_group.sort_values('ball_of_over')
                print(over_data[['ball_of_over', 'legal_ball_of_over', 'bowler_balls_bowled']])
        
        # Saving to CSV
        issues_df.to_csv('data/bowler_statistics_issues.csv', index=False)
        print("Bowler statistics issues saved to data/bowler_statistics_issues.csv")
        
        return issues_df
    else:
        print("No bowler statistics issues found.")
        return None
    

def check_incomplete_overs():
    """
    Checks for overs with fewer than 6 balls, which may indicate missing data
    """
    print("\nChecking for incomplete overs (missing balls)...")
    
    # Creating a copy of the dataframe
    df = ball_by_ball.copy()
    
    # Count balls in each over
    over_counts = df.groupby(['match_id', 'innings_number', 'over']).size().reset_index(name='ball_count')
    
    # In cricket, an over should have 6 legal deliveries to get completed
    incomplete_overs = over_counts[over_counts['ball_count'] < 6].copy()
    
    if len(incomplete_overs) > 0:
        print(f"Found {len(incomplete_overs)} potentially incomplete overs")
        print("\nSample incomplete overs:")
        print(incomplete_overs.head())
        
        # Checking for the specific example in match 1459548, over 13
        specific_example = incomplete_overs[(incomplete_overs['match_id'] == 1459548) & (incomplete_overs['over'] == 13)]
        if len(specific_example) > 0:
            print("\nSpecific example from report (match 1459548, over 13):")
            print(specific_example)
            
            # Show the actual balls in this over
            example_balls = df[(df['match_id'] == 1459548) & (df['innings_number'] == 1) & (df['over'] == 13)]
            print("\nBalls in this over:")
            print(example_balls[['match_id', 'innings_number', 'over', 'ball_of_over', 'legal_ball_of_over', 'facing_batter_name', 'bowler_name']])
        
        # Find the most extreme cases (fewest balls)
        extreme_cases = incomplete_overs.sort_values('ball_count').head(5)
        print("\nMost extreme cases (fewest balls):")
        print(extreme_cases)
        
        # additional analysis to look for patterns in incomplete overs
        incomplete_by_match = incomplete_overs.groupby('match_id').size().reset_index(name='incomplete_over_count')
        incomplete_by_match = incomplete_by_match.sort_values('incomplete_over_count', ascending=False)
        print("\nMatches with the most incomplete overs:")
        print(incomplete_by_match.head())
        
        # matches where sequential overs are missing
        sequential_missing = []
        for match_id in incomplete_overs['match_id'].unique():
            match_overs = incomplete_overs[incomplete_overs['match_id'] == match_id]['over'].values
            match_overs.sort()
            
            for i in range(len(match_overs) - 1):
                if match_overs[i] + 1 == match_overs[i + 1]:
                    sequential_missing.append({
                        'match_id': match_id,
                        'first_over': match_overs[i],
                        'second_over': match_overs[i + 1]
                    })
        
        if sequential_missing:
            sequential_df = pd.DataFrame(sequential_missing)
            print("\nMatches with sequential missing overs (possible data gap patterns):")
            print(sequential_df)
        
        # Saving to CSV
        incomplete_overs.to_csv('data/incomplete_overs.csv', index=False)
        print("Incomplete overs saved to data/incomplete_overs.csv")
        
        return incomplete_overs
    else:
        print("No incomplete overs found.")
        return None
    

# Validate run totals
def validate_run_totals():
    # Group by match and innings
    innings_totals = ball_by_ball.groupby(['match_id', 'innings_number']).agg({
        'runs_off_bat': 'sum',
        'runs_wide': 'sum',
        'runs_bye': 'sum',
        'runs_leg_bye': 'sum',
        'no_ball_penalty_runs': 'sum'
    })
    
    # Calculate total runs
    innings_totals['calculated_total'] = innings_totals.sum(axis=1)
    
    # Compare with recorded totals from innings data
    # (assuming you have innings_df with total runs)
    merged = innings_totals.merge(
        innings[['match_id', 'innings_number', 'runs']], 
        on=['match_id', 'innings_number']
    )
    
    # Find discrepancies
    discrepancies = merged[merged['calculated_total'] != merged['runs']]
    print("\ndiscrepancies\n", discrepancies)
    return discrepancies

if __name__ == "__main__":
    check_innings_endings()
    check_null_values()
    check_bowler_statistics()
    check_incomplete_overs()
    validate_run_totals()