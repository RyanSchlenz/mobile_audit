import pandas as pd

def process_workday_data(input_file, output_file_inactive, output_file_active):
    # Read the CSV file, skipping the first 4 rows (index 0-3) and using the 5th row (index 4) as the header
    df = pd.read_csv(input_file, header=4, encoding='latin1')

    # Print the column names to check if the header is correctly assigned
    print("Column names:", df.columns)

    # Filter rows where 'Active Status' is NOT 'Yes'
    inactive_df = df[df['Active Status'] != 'Yes']
    inactive_df.to_csv(output_file_inactive, index=False)
    print(f"Inactive data has been saved to {output_file_inactive}")

    # Filter rows where 'Active Status' is 'Yes'
    active_df = df[df['Active Status'] == 'Yes']
    active_df.to_csv(output_file_active, index=False)
    print(f"Active data has been saved to {output_file_active}")


# The main script execution block
if __name__ == "__main__":
    # Define the file paths for input and output
    input_file = "workday_data.csv"  # Path to your input CSV file
    output_file_inactive = "workday_inactive_data.csv"  # Path to the output file for inactive data
    output_file_active = "workday_active_data.csv"  # Path to the output file for active data

    # Call the function to process the data
    process_workday_data(input_file, output_file_inactive, output_file_active)
