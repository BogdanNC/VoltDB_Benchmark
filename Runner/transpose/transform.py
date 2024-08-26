import os
import pandas as pd
import re

# Define the source and destination directories
csv_folder = "./distributed instance_transposed"
dest_folder = "./distributed instance_transformed"

# Create the destination folder if it doesn't exist
os.makedirs(dest_folder, exist_ok=True)

# Get the list of all CSV files in the source directory
csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

def clean_time_format(time_string):
    match = re.match(r'(\d+)m([\d.]+)s', time_string)
    if match:
        minutes = int(match.group(1))
        seconds = float(match.group(2))
        total_seconds = minutes * 60 + seconds
        return f"{total_seconds:.3f}"
    return time_string

def transform_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Get the actual number of rows and columns
    num_rows, num_cols = df.shape

    # Iterate over the specific rows and columns to clean the time format
    for row in range(0, min(11, num_rows)):  # Ensure we don't exceed the number of rows
        for col in range(min(24, num_cols)):  # Ensure we don't exceed the number of columns
            if isinstance(df.iloc[row, col], str):
                df.iloc[row, col] = clean_time_format(df.iloc[row, col])

    # Save the transformed DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

# Loop through each CSV file and transform it
for csv_file in csv_files:
    input_file = os.path.join(csv_folder, csv_file)
    output_file = os.path.join(dest_folder, csv_file)
    transform_csv(input_file, output_file)

print(f"Transformed CSV files are saved in '{dest_folder}'.")
