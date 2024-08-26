import docker
import os
import tarfile
import io

client = docker.from_env()

container_name = "node4"  # Name of your Docker container

file_loc = "/mnt/output_csv_1000k/"

authors = "authors.csv"
documents = "documents.csv"
documents_authors = "documents_authors.csv"
genders = "genders.csv"
geo_location = "geo_location.csv"
vocabulary = "vocabulary.csv"
words = "words.csv"

# Step 1: Copy the SQL script to the Docker container
container = client.containers.get(container_name)

# Step 2: Create and execute the command using exec_create and exec_start
command = f"csvloader  --file={file_loc}{authors} --skip 1 --separator=, AUTHORS"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("authors completed.")

command = f"csvloader  --file={file_loc}{documents} --skip 1 --separator=, DOCUMENTS"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("Documents completed.")

command = f"csvloader  --file={file_loc}{documents_authors} --skip 1 --separator=, DOCUMENTS_AUTHORS"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("Documents_authors completed.")


command = f"csvloader  --file={file_loc}{genders} --skip 1 --separator=, GENDERS"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("genders completed.")


command = f"csvloader  --file={file_loc}{geo_location} --skip 1 --separator=, GEO_LOCATION"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("geo_location completed.")

command = f"csvloader  --file={file_loc}{vocabulary} --skip 1 --separator=, VOCABULARY"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("vocabulary completed.")

command = f"csvloader  --file={file_loc}{words} --skip 1 --separator=, WORDS"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("words completed.")