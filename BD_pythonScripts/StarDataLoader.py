import docker
import os
import tarfile
import io

client = docker.from_env()

container_name = "node4"  # Name of your Docker container

file_loc = "/mnt/output_csv_star_1000k/"

author_dimension = "author_dimension.csv"
document_dimension = "document_dimension.csv"
document_facts = "document_facts.csv"
location_dimension = "location_dimension.csv"
time_dimension = "time_dimension.csv"
word_dimension = "word_dimension.csv"

# Step 1: Copy the SQL script to the Docker container
container = client.containers.get(container_name)

# Step 2: Create and execute the command using exec_create and exec_start
command = f"csvloader  --file={file_loc}{author_dimension} --skip 1 --separator=, author_dimension"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("author_dimension completed.")

command = f"csvloader  --file={file_loc}{document_dimension} --skip 1 --separator=, document_dimension"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("document_dimension completed.")

command = f"csvloader  --file={file_loc}{document_facts} --skip 1 --separator=, document_facts"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("document_facts completed.")


command = f"csvloader  --file={file_loc}{location_dimension} --skip 1 --separator=, location_dimension"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("location_dimension completed.")

command = f"csvloader  --file={file_loc}{time_dimension} --skip 1 --separator=, time_dimension"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("time_dimension completed.")

command = f"csvloader  --file={file_loc}{word_dimension} --skip 1 --separator=, word_dimension"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("word_dimension completed.")