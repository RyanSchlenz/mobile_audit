import pandas as pd

def process_verizon_data(input_file, output_file_inactive, output_file_active):
    # Define the columns you want in the output
    output_columns = [
        "Cost center",
        "Wireless number",
        "Current device ID - 4G only",  # Assuming this is the IMEI
        "SIM",
        "User name",
        "Minutes",
        "Data usage",
        "Used minutes",
        "Wireless number status",
        "Device manufacturer"
    ]

    # Read the input Verizon data CSV
    df = pd.read_csv(input_file, encoding="latin1")

    # Ensure the required columns exist in the input data
    required_columns = ["Data usage", "Minutes", "Used minutes", "Wireless number status"] + output_columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following required columns are missing from the input file: {', '.join(missing_columns)}")

    # Filter rows where "Wireless number status" is "Active"
    df = df[df["Wireless number status"].str.strip().eq("Active")]

    # Convert 'Data usage', 'Minutes', and 'Used minutes' to numeric, replacing non-numeric values with 0
    df["Data usage"] = pd.to_numeric(df["Data usage"], errors="coerce").fillna(0)
    df["Minutes"] = pd.to_numeric(df["Minutes"], errors="coerce").fillna(0)
    df["Used minutes"] = pd.to_numeric(df["Used minutes"], errors="coerce").fillna(0)

    # Filter rows for inactive usage: 'Data usage', 'Minutes', and 'Used minutes' are all 0
    inactive_df = df[(df["Data usage"] == 0) & (df["Minutes"] == 0) & (df["Used minutes"] == 0)]

    # Filter rows for active usage: Any of 'Data usage', 'Minutes', or 'Used minutes' is greater than 0
    active_df = df[(df["Data usage"] > 0) | (df["Minutes"] > 0) | (df["Used minutes"] > 0)]

    # Select only the desired columns for output
    inactive_df = inactive_df[output_columns]
    active_df = active_df[output_columns]

    # Save the filtered data to respective CSV files
    inactive_df.to_csv(output_file_inactive, index=False)
    active_df.to_csv(output_file_active, index=False)

    print(f"Inactive Verizon data saved to {output_file_inactive}")
    print(f"Active Verizon data saved to {output_file_active}")


# The main script execution block
if __name__ == "__main__":
    # Define the file paths for input and output
    input_file = "verizon_data.csv"  # Path to your input CSV file
    output_file_inactive = "inactive_verizon.csv"  # Path to the output file for inactive data
    output_file_active = "active_verizon.csv"  # Path to the output file for active data

    # Call the function to process the data
    process_verizon_data(input_file, output_file_inactive, output_file_active)
