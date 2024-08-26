import os
import subprocess
import csv

# Define variables

#local doc files :                                  Docker paths
#../Topk_doc/DB_volt_tfidf                      /tmp/TopK_Documents/DB_tfidf
#../Topk_doc/DB_volt_okapi                      /tmp/TopK_Documents/DB_okapi
#../Topk_doc/OLAP_volt_tfidf                    /tmp/TopK_Documents/OLAP_tfidf
#../Topk_doc/OLAP_volt_okapi                    /tmp/TopK_Documents/OLAP_okapi

#local keywords files :                                  Docker paths
#../Topk_Keywords/DB_volt_tfidf                      /tmp/TopK_Keywords/DB_tfidf
#../Topk_Keywords/DB_volt_okapi                      /tmp/TopK_Keywords/DB_okapi
#../Topk_Keywords/OLAP_volt_tfidf                    /tmp/TopK_Keywords/OLAP_tfidf
#../Topk_Keywords/OLAP_volt_okapi                    /tmp/TopK_Keywords/OLAP_okapi

docker_container = 'node4'

sql_folder = '../Topk_Keywords/OLAP_volt_tfidf'  # Path to the folder containing the .sql files
docker_path = '/tmp/TopK_Keywords/OLAP_tfidf'
csv_file = 'results.csv'

# List all .sql files in the folder
# extra condition : f.startswith('Q3')
sql_files = [f for f in os.listdir(sql_folder) if f.endswith('.sql')]


# Open the CSV file for writing
with open(csv_file, mode='a', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Iterate over each SQL file
    for sql_file in sql_files:
       
        file_path = os.path.join(sql_folder, sql_file)
        execution_times = []

        # Copy the file to the Docker container
        subprocess.run(['docker', 'cp', file_path, f'{docker_container}:{docker_path}'])

        # Run the SQL command 10 times and capture the "real" time
        for _ in range(10):
            cmd = f'time sqlcmd --query-timeout=30000 < {docker_path}/{sql_file}'
            
            # Execute the command in the Docker container
            exec_id = subprocess.run(['docker', 'exec', docker_container, 'bash', '-c', cmd], capture_output=True, text=True)
            
            # Check the exit code and handle any errors
            exit_code = exec_id.returncode
            output = exec_id.stderr

            if exit_code != 0:
                print(f"Error executing SQL script '{sql_file}': {output.decode('utf-8')}")
                break  # Optionally break the loop if an error occurs

            # Extract the "real" time from the output
            for line in output.splitlines():
                if 'real' in line:
                    time_str = line.split()[1]
                    execution_times.append(time_str)
                    break

        # Write the results for this SQL file to the CSV file
        if len(execution_times) == 10:
            csvwriter.writerow([sql_file] + execution_times)
        else:
            print(f"Execution for file '{sql_file}' did not complete 10 times due to an error.")

print(f'Results have been written to {csv_file}')
