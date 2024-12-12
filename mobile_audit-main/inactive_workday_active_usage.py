import pandas as pd

def match_inactive_workday_active_usage():
    # File paths
    active_usage_file = 'active_usage_active_soti.csv'
    workday_inactive_file = 'workday_inactive_data.csv'
    output_file = 'inactive_workday_active_usage.csv'

    # Load the CSV files
    active_usage_df = pd.read_csv(active_usage_file, encoding='utf-8-sig')
    workday_inactive_df = pd.read_csv(workday_inactive_file, encoding='utf-8-sig')

    # Clean up column names (remove leading/trailing spaces)
    active_usage_df.columns = active_usage_df.columns.str.strip()
    workday_inactive_df.columns = workday_inactive_df.columns.str.strip()

    # Print columns to verify their names
    print("Columns in active_usage_df:", active_usage_df.columns)
    print("Columns in workday_inactive_df:", workday_inactive_df.columns)

    # Ensure the comparison is case-insensitive by converting both columns to lowercase
    active_usage_df['Verizon User name'] = active_usage_df['Verizon User name'].str.lower()
    workday_inactive_df['Worker'] = workday_inactive_df['Worker'].str.lower()

    # Merge the dataframes on the case-insensitive 'Verizon User name' and 'Worker'
    merged_df = pd.merge(
        active_usage_df,
        workday_inactive_df,
        left_on='Verizon User name',
        right_on='Worker',
        how='inner'
    )

    # Debugging step: Print the column names of the merged dataframe
    print("Columns in merged_df:", merged_df.columns)

    # Check if the required columns exist in the merged dataframe
    if 'SOTI Device manufacturer' in merged_df.columns and 'Verizon Device manufacturer' in merged_df.columns:
        # Select the relevant columns and rename them to match the desired format
        output_df = merged_df[[
            'Cost center',
            'SIM_x',
            'Verizon User name',
            'Minutes',
            'Data usage',
            'Wireless number',
            'SOTI Device manufacturer',  # SOTI Device manufacturer
            'Verizon Device manufacturer'   # Verizon Device manufacturer
        ]]

        # Save the result to the output CSV file
        output_df.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f"Matched inactive workday active usage data saved to {output_file}")
    else:
        print("Required columns are missing in the merged dataframe.")

# If this script is being run as the main program, call the match_inactive_workday_active_usage function
if __name__ == '__main__':
    match_inactive_workday_active_usage()
