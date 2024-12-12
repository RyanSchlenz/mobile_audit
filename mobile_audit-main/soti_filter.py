import pandas as pd
from datetime import datetime, timedelta

def process_soti_data(input_file, output_file_active, output_file_inactive):
    # Load the CSV file into a DataFrame with specified encoding (handles BOM properly)
    df = pd.read_csv(input_file, encoding='utf-8-sig')

    # Clean up column names (remove leading/trailing spaces)
    df.columns = df.columns.str.strip()

    # Remove spaces from 'IMEI / MEID / ESN' and 'ICCID' (now 'SIM') columns
    df['IMEI / MEID / ESN'] = df['IMEI / MEID / ESN'].str.replace(' ', '', regex=False)
    df['ICCID'] = df['ICCID'].str.replace(' ', '', regex=False)

    # Rename columns to match the desired output format
    df = df.rename(columns={
        'ICCID': 'SIM',
        'Phone Number': 'Wireless number',
        'IMEI / MEID / ESN': 'IMEI',
        'Device Name': 'User name',
        'Device Kind': 'Device manufacturer'
    })

    # Drop rows where 'SIM' or 'Wireless number' is missing
    df = df.dropna(subset=['SIM', 'Wireless number'])

    # Ensure 'IMEI' is treated as a string to preserve all digits
    df['IMEI'] = df['IMEI'].astype(str)

    # Remove .0 from Wireless number if it exists
    df['Wireless number'] = df['Wireless number'].astype(str).str.replace('.0', '', regex=False)

    # Format the Wireless number column as xxx-xxx-xxxx
    def format_phone_number(phone):
        phone = phone.lstrip('1')  # Remove leading 1 if exists
        if len(phone) == 10:  # Ensure it has 10 digits after formatting
            return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        return phone  # Return unformatted phone if it doesn't match

    df['Wireless number'] = df['Wireless number'].apply(format_phone_number)

    # Map Device Kind values to desired values
    df['Device manufacturer'] = df['Device manufacturer'].replace({
        'Ios': 'APL',
        'AndroidForWork': 'SAM',
        'AndroidElm': 'SAM'
    })

    # Drop the 'UPN' column if it exists
    if 'UPN' in df.columns:
        df = df.drop(columns=['UPN'])

    # Ensure 'Agent Check-in Time' is in datetime format
    df['Agent Check-in Time'] = pd.to_datetime(df['Agent Check-in Time'], errors='coerce')

    # Calculate the date for 30 days ago
    thirty_days_ago = datetime.now() - timedelta(days=30)

    # Filter rows into active and inactive based on Agent Check-in Time
    active_df = df[df['Agent Check-in Time'] >= thirty_days_ago]
    inactive_df = df[df['Agent Check-in Time'] < thirty_days_ago]

    # Remove duplicates based on 'IMEI' column
    active_df = active_df.drop_duplicates(subset=['IMEI'])
    inactive_df = inactive_df.drop_duplicates(subset=['IMEI'])

    # Save the active and inactive data to respective CSV files
    active_df.to_csv(output_file_active, index=False)
    inactive_df.to_csv(output_file_inactive, index=False)

    print(f"Active devices saved to {output_file_active}")
    print(f"Inactive devices saved to {output_file_inactive}")

# If this script is being run as the main program, call the process_soti_data function
if __name__ == '__main__':
    # File paths
    input_file = 'soti_data.csv'  # Update with your actual file path
    output_file_active = 'active_soti.csv'
    output_file_inactive = 'inactive_soti.csv'

    # Call the function
    process_soti_data(input_file, output_file_active, output_file_inactive)
