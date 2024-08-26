import docker
import os
import tarfile
import io

client = docker.from_env()



container_name = "node4"
#Make sure only one is uncommented at a time:
#regular schema, Uncomment if you want to load the tables. 
#sql_schema = "../BD_SQL_scripts/regular_schema.sql"
#sql_schema_dest = "/tmp/regular_schema.sql"

#star schema, Uncomment if you want to load the tables
sql_schema = "../BD_SQL_scripts/star_schema.sql"
sql_schema_dest = "/tmp/star_schema.sql"


# Ensure the script exists
if not os.path.exists(sql_schema):
    raise FileNotFoundError(f"SQL script not found at {sql_schema}")

# Create a tarball containing the SQL script
tar_stream = io.BytesIO()
with tarfile.open(fileobj=tar_stream, mode='w') as tar:
    tar.add(sql_schema, arcname=os.path.basename(sql_schema_dest))
tar_stream.seek(0)

# Step 1: Copy the SQL script to the Docker container
container = client.containers.get(container_name)
print(f"Copying {sql_schema} to {container_name}:{sql_schema_dest}")
container.put_archive(os.path.dirname(sql_schema_dest), tar_stream)

# Step 2: Create and execute the command using exec_create and exec_start
sqlcmd_command = f"sqlcmd < {sql_schema_dest}"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{sqlcmd_command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("Process completed.")
