import os
import time

def run_analysis(script_name):
    """Runs a Python script and time its execution"""
    start_time = time.time()
    print(f"\n{'='*80}\nRunning {script_name}...\n{'='*80}")
    os.system(f"python scripts/{script_name}.py")
    print(f"\nExecution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    # Making sure we're in the project root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir('..')
    
    # Creating output directories if they don't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Run all analysis scripts
    analysis_scripts = [
        'legal_ball_analysis',
        'run_calculation_analysis',
        'wicket_analysis',
        'player_data_analysis',
        'other_issues_analysis'
    ]
    
    for script in analysis_scripts:
        run_analysis(script)
    
    print("\nAll analyses complete! Results saved to data/ directory.")