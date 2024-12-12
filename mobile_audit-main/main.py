import os
import subprocess
import time
from project_config import config

# Load configuration from project_config
scripts = config['scripts']
csv_files = config['csv_files']

# List to track created files
created_files = []

# Function to get the full path of a file in the same directory as the script
def get_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# Function to run a script
def run_script(script):
    script_path = get_file_path(script)
    try:
        print(f"Running {script_path}...")
        subprocess.check_call(['python', script_path])
        print(f"Successfully ran {script_path}")
        # Track the files created by the script
        track_created_files()
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to run {script_path}: {e}")
        return False

# Function to delete all created CSV and XLSX files except specified ones
def delete_files(success=True):
    # Specify the files to exclude from deletion (only exclude specified ones)
    files_to_exclude = {
        'zendesk_ticket_analysis.xlsx', 
        'immediate_action.xlsx',
        'inactive_workday_active_usage.xlsx', 
        'inactive_usage_active_workday.xlsx',
        'immediate_action.csv',
        'inactive_workday_active_usage.csv', 
        'inactive_usage_active_workday.csv',
        'workday_data.csv',
        'verizon_data.csv',
        'soti_data.csv'
    }

    # Delete only .csv and .xlsx files that were created by the script
    for file in os.listdir(os.path.dirname(__file__)):
        file_path = get_file_path(file)
        # Only delete if the file is not in the exclusion list and is a .csv or .xlsx file
        if os.path.isfile(file_path) and os.path.basename(file_path) not in files_to_exclude and (file_path.endswith('.csv') or file_path.endswith('.xlsx')):
            os.remove(file_path)
            print(f"Deleted {file_path}")
    
    # If it fails, clean up immediately
    if not success:
        print("Cleaned up files after failure.")

# Function to track created files during script execution
def track_created_files():
    # List of all files in the current directory
    dir_path = os.path.dirname(__file__)
    for file in os.listdir(dir_path):
        # Track only newly created .csv and .xlsx files
        if (file.endswith('.csv') or file.endswith('.xlsx')) and file not in created_files:
            created_files.append(file)
            print(f"Created file: {file}")

# Function to run all scripts and check CSV and XLSX file existence
def run_all_scripts():
    # Run each main script in order
    for script in scripts:
        if not run_script(script):
            print(f"Script {script} failed. Stopping execution.")
            delete_files(success=False)  # Clean up files if failure occurs
            break
    else:
        # Check if all required CSV files exist after scripts have run
        time.sleep(2)  # Short delay before checking files
        if check_csv_files(csv_files):
            print("All scripts ran successfully and all required CSV files are present.")
        else:
            print("One or more required files are missing after script execution.")
            delete_files(success=False)  # Clean up files if failure occurs

    # List all created files at the end
    print("\nList of all created files:")
    for file in created_files:
        print(file)

# Function to check if required CSV files exist
def check_csv_files(files):
    missing_files = [get_file_path(file) for file in files if not os.path.isfile(get_file_path(file))]
    if not missing_files:
        return True
    print(f"Missing files: {', '.join(missing_files)}")
    return False

if __name__ == "__main__":
    # Track the files that are created during script execution
    created_files.extend(csv_files)  # Add the initial CSV files that are expected to be created

    run_all_scripts()
