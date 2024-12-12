import pandas as pd

def convert_csv_to_excel():
    # List of CSV files to convert
    csv_files = [
        'immediate_action.csv',
        'inactive_workday_active_usage.csv',
        'inactive_usage_active_workday.csv'
    ]

    # Convert each CSV file to an Excel file
    for csv_file in csv_files:
        # Generate the output file name by replacing the CSV extension with .xlsx
        xlsx_file = csv_file.replace('.csv', '.xlsx')  # Output file path

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Ensure that IMEI columns are treated as strings to prevent Excel formatting issues
        for column in df.columns:
            if 'IMEI' in column:  # Check if the column name contains "IMEI"
                df[column] = df[column].astype(str).str.replace('.0', '', regex=False)  # Clean any .0 suffix

        # Write the DataFrame to an Excel file
        df.to_excel(xlsx_file, index=False, engine='openpyxl')

        print(f"CSV file '{csv_file}' has been successfully converted to '{xlsx_file}'")

# If this script is being run as the main program, call the convert_csv_to_excel function
if __name__ == '__main__':
    convert_csv_to_excel()
