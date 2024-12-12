import pandas as pd

def process_usage_data(soti_file, verizon_file, output_file):
    # Read data from both files
    verizon_df = pd.read_csv(verizon_file)
    soti_df = pd.read_csv(soti_file)

    # Print column names to check for discrepancies
    print(f"{soti_file} columns:", soti_df.columns)
    print(f"{verizon_file} columns:", verizon_df.columns)

    # Strip whitespace from Wireless number columns
    verizon_df['Wireless number'] = verizon_df['Wireless number'].str.strip()
    soti_df['Wireless number'] = soti_df['Wireless number'].str.strip()

    # Ensure IMEI columns are strings to handle any formatting issues (like `.0` suffix)
    verizon_df['Current device ID - 4G only'] = verizon_df['Current device ID - 4G only'].astype(str).str.replace('.0', '', regex=False)
    soti_df['IMEI'] = soti_df['IMEI'].astype(str).str.replace('.0', '', regex=False)

    # Check for duplicates
    print("Duplicates in verizon_df:", verizon_df['Wireless number'].duplicated().sum())
    print("Duplicates in soti_df:", soti_df['Wireless number'].duplicated().sum())

    # Merge the DataFrames on Wireless number
    merged_df = pd.merge(
        verizon_df,
        soti_df,
        left_on='Wireless number',
        right_on='Wireless number',
        indicator=True  # Adds a column '_merge' to indicate merge status
    )

    # Output match statistics
    matched_count = merged_df[merged_df['_merge'] == 'both'].shape[0]
    print("Matched rows count:", matched_count)

    # Output the counts for clarity
    total_verizon = verizon_df.shape[0]
    total_soti = soti_df.shape[0]
    print(f"Total in verizon_df: {total_verizon}")
    print(f"Total in soti_df: {total_soti}")

    # Print merged DataFrame shape and counts of merge types
    print("Merged DataFrame shape:", merged_df.shape)
    print("Counts of merge types:\n", merged_df['_merge'].value_counts())

    # Ensure that the 'User name' from verizon_df is included
    merged_df['Verizon User name'] = merged_df['User name_x']  # Explicitly take from verizon_df

    # Select the correct columns for output
    output_columns = [
        'Cost center', 'IMEI_x', 'SIM_x', 'Verizon User name', 'Minutes', 'Data usage', 'Wireless number', 
        'Device manufacturer_x', 'Device manufacturer_y'  # Device manufacturer from both files
    ]

    # Filter the DataFrame to include only the matching rows (where merge indicator is 'both')
    final_columns = [col for col in output_columns if col in merged_df.columns]
    final_df = merged_df[merged_df['_merge'] == 'both'][final_columns]

    # Fill blank 'Data usage' with 0
    final_df['Data usage'] = final_df['Data usage'].fillna(0)

    # Rename columns for clarity
    final_df = final_df.rename(columns={
        'Device manufacturer_x': 'SOTI Device manufacturer',  # From SOTI data
        'Device manufacturer_y': 'Verizon Device manufacturer'  # From Verizon data
    })

    # Check if 'Verizon User name' is present in final_df columns
    print("Final DataFrame columns:", final_df.columns)

    # Save the resulting DataFrame to a new CSV file
    final_df.to_csv(output_file, index=False)

    # Print final counts
    print("Matched rows count:", final_df.shape[0])
    print(f"Matching data has been combined and saved to '{output_file}'!")

# Main function to call process_usage_data for both Active and Inactive usage
def main():
    # File paths (you can change these as needed)
    active_soti_file = 'active_soti.csv'
    active_verizon_file = 'active_verizon.csv'
    inactive_soti_file = 'inactive_soti.csv'
    inactive_verizon_file = 'inactive_verizon.csv'

    # Output files
    output_active_file = 'active_usage_active_soti.csv'
    output_inactive_file = 'inactive_usage_inactive_soti.csv'

    # Process Active Usage
    print("Processing Active Usage Data...")
    process_usage_data(active_soti_file, active_verizon_file, output_active_file)

    # Process Inactive Usage
    print("Processing Inactive Usage Data...")
    process_usage_data(inactive_soti_file, inactive_verizon_file, output_inactive_file)

# If this script is being run as the main program, call the main function
if __name__ == '__main__':
    main()
