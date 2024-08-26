import os

# Define the file name patterns
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
weeks = ['1w', '2w', '3w']
genders = ['male', 'female']

# Directory to save the files (optional, you can set it to your desired path)
output_directory = '.'

# Loop through quarters and genders to create the files
for quarter in quarters:
    for week in weeks:
        for gender in genders:
            # Construct the file name
            file_name = f"{quarter}_{week}_{gender}.sql"
            
            # Full path to the file
            file_path = os.path.join(output_directory, file_name)
            
            # Create the file and write a sample comment inside
            with open(file_path, 'w') as file:
                file.write(f"-- SQL file for {quarter} {week} {gender}\n")
            
            print(f"Created file: {file_path}")