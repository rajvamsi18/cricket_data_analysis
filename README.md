# Cricket Data Quality Analysis

## Project Overview

This repository contains Python scripts for analyzing cricket match data quality. The scripts identify various 
data quality issues as documented in the accompanying report `Cricket Data Quality Analysis Report.pdf`.


## Project Structure

```

├── data
│   ├── ball_by_ball.csv
│   ├── field_descriptions.csv
│   ├── innings.csv
│   ├── players.csv
├── README.md
├── scripts
│   ├── legal_ball_analysis.py
│   ├── other_issues_analysis.py
│   ├── player_data_analysis.py
│   ├── run_all_analyses.py
│   ├── run_calculation_analysis.py
│   └── wicket_analysis.py

```

## Required Python Packages

To run the analysis scripts, you need the following Python packages:
- pandas (2.0.0 or newer)
- numpy (1.24.0 or newer)

Install with pip:

    pip install pandas numpy

## How to Run the Scripts

### Option 1: Run All Analyses at Once

1. Place the CSV data files in the `data/` directory
2. Open a terminal or command prompt
3. Navigate to the project root directory
4. Run the main script:

    python scripts/run_all_analyses.py

5. Analysis results will be saved as CSV files in the `data/` directory

### Option 2: Run Individual Analysis Scripts

You can also run each analysis script individually:

    python scripts/legal_ball_analysis.py      # Check legal ball counting issues
    python scripts/run_calculation_analysis.py # Check run calculation inconsistencies
    python scripts/wicket_analysis.py          # Analyze wicket information issues
    python scripts/player_data_analysis.py     # Check player data completeness
    python scripts/other_issues_analysis.py    # Analyze other data quality issues

## What Each Script Does

1. **legal_ball_analysis.py**: Identifies instances where the `legal_ball_of_over` counter incorrectly 
   increments for wide balls and no-balls.

2. **run_calculation_analysis.py**: Detects inconsistencies in run totals by:
   - Comparing calculated running totals with recorded `total_runs_so_far` values
   - Identifying mismatches between ball-by-ball and innings data

3. **wicket_analysis.py**: Finds issues with wicket information such as:
   - Missing dismissal details (batter who got out, bowler who took wicket)
   - Specific analysis of rows 555-610 where wicket counts are inconsistent

4. **player_data_analysis.py**: Analyzes player data issues including:
   - Missing batting and bowling attributes in players.csv
   - Missing non-facing batter details in ball-by-ball data

5. **other_issues_analysis.py**: Examines various other quality issues:
   - Unexplained innings endings
   - Null values in critical fields
   - Inconsistent bowler statistics
   - Missing overs and balls

6. **run_all_analyses.py**: Main script that runs all the above analyses in sequence and consolidates 
   the results.

## Data Quality Issues Identified

The scripts identify several key data quality issues including:

1. Legal ball counting errors for extras
2. Run calculation inconsistencies
3. Missing wicket information
4. Incomplete player data
5. Unexplained innings endings
6. Inefficient use of null values
7. Missing overs and inconsistent bowler statistics
8. Metadata and schema errors

For a detailed explanation of these issues and recommendations for addressing them, please refer to 
the full report in `Cricket Data Quality Analysis Report.pdf`.