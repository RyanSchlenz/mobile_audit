import pandas as pd

def process_data():
    # Load the CSV files into DataFrames
    workday_inactive_data = pd.read_csv('workday_inactive_data.csv')
    workday_active_data = pd.read_csv('workday_active_data.csv')
    inactive_usage_inactive_soti = pd.read_csv('inactive_usage_inactive_soti.csv')
    active_usage_active_soti = pd.read_csv('active_usage_active_soti.csv')

    # Normalize the data by converting the relevant columns to lowercase
    workday_inactive_data['Worker'] = workday_inactive_data['Worker'].str.lower()
    workday_active_data['Worker'] = workday_active_data['Worker'].str.lower()
    inactive_usage_inactive_soti['Verizon User name'] = inactive_usage_inactive_soti['Verizon User name'].str.lower()
    active_usage_active_soti['Verizon User name'] = active_usage_active_soti['Verizon User name'].str.lower()

    # Check for matching values in "Verizon User name" column with "Worker" in workday_inactive_data
    inactive_matches = inactive_usage_inactive_soti[inactive_usage_inactive_soti['Verizon User name'].isin(workday_inactive_data['Worker'])]

    # Check for matching values in "Verizon User name" column with "Worker" in workday_active_data
    active_matches = active_usage_active_soti[active_usage_active_soti['Verizon User name'].isin(workday_inactive_data['Worker'])]

    # Check for matching values in "Verizon User name" column with "Worker" in workday_active_data for inactive usage data
    inactive_usage_workday_matches = inactive_usage_inactive_soti[inactive_usage_inactive_soti['Verizon User name'].isin(workday_active_data['Worker'])]

    # Remove duplicates from the matches
    inactive_matches = inactive_matches.drop_duplicates()
    active_matches = active_matches.drop_duplicates()
    inactive_usage_workday_matches = inactive_usage_workday_matches.drop_duplicates()

    # Save the matched data to separate CSV files
    inactive_matches.to_csv('immediate_action.csv', index=False)
    active_matches.to_csv('inactive_workday_active_usage.csv', index=False)
    inactive_usage_workday_matches.to_csv('inactive_usage_active_workday.csv', index=False)

    # Print confirmation messages
    print("Inactive matching data saved to immediate_action.csv")
    print("Active matching data saved to inactive_workday_active_usage.csv")
    print("Inactive Usage and Workday matching data saved to inactive_usage_active_workday.csv")

# If this script is being run as the main program, call the process_data function
if __name__ == '__main__':
    process_data()
