import pandas as pd

def match_inactive_verizon_workday():
    # Load the CSV files
    verizon_data_file = 'verizon_data_cleaned.csv'  # Path to the Verizon data
    workday_data_file = 'workday_data.csv'  # Path to the Workday data
    output_file = 'inactive_verizon_workday_match.csv'  # Output file name

    # Read the CSV files
    verizon_df = pd.read_csv(verizon_data_file)
    workday_df = pd.read_csv(workday_data_file, header=4, encoding='latin1')

    # Check the column names to ensure we're using the correct ones
    print("Verizon Data Columns:", verizon_df.columns)
    print("Workday Data Columns:", workday_df.columns)

    # Convert both 'Verizon User name' and 'Worker' columns to lowercase to make comparison case-insensitive
    verizon_df['User name'] = verizon_df['User name'].str.lower()
    workday_df['Worker'] = workday_df['Worker'].str.lower()

    # Filter rows where 'Data usage' and 'Used minutes' are both 0
    inactive_verizon_df = verizon_df[(verizon_df['Data usage'] == 0) & (verizon_df['Used minutes'] == 0)]

    # Merge the inactive verizon data with the workday data based on matching 'User name' and 'Worker'
    merged_df = pd.merge(inactive_verizon_df, workday_df, 
                         left_on='User name', right_on='Worker', 
                         how='inner')

    # Select only the columns from verizon_data_cleaned.csv that you need
    final_df = merged_df[['Cost center', 'IMEI_x', 'SIM_x', 'User name', 'Used minutes', 'Data usage', 'Wireless number', 'Device manufacturer_x']]

    # Save the final DataFrame to a new CSV file
    final_df.to_csv(output_file, index=False)

    print(f"Matching inactive data has been saved to {output_file}")

# If this script is being run as the main program, call the match_inactive_verizon_workday function
if __name__ == '__main__':
    match_inactive_verizon_workday()
