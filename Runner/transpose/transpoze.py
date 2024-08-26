import os
import pandas as pd

# Define the source and destination directories
csv_folder = "../Distributed instance"
dest_folder = "./distributed instance_transposed"

# Create the destination folder if it doesn't exist
os.makedirs(dest_folder, exist_ok=True)

# Get the list of all CSV files in the source directory
csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

def transpose_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file, header=None)

    # Transpose the DataFrame
    df_transposed = df.transpose()

    # Optional: Reset the index if you want a clean header
    df_transposed.reset_index(drop=True, inplace=True)

    # Save the transposed DataFrame to a new CSV file
    df_transposed.to_csv(output_file, index=False, header=False)

# Loop through each CSV file and transpose it
for csv_file in csv_files:
    input_file = os.path.join(csv_folder, csv_file)
    output_file = os.path.join(dest_folder, csv_file)
    transpose_csv(input_file, output_file)

print(f"Transposed CSV files are saved in '{dest_folder}'.")
