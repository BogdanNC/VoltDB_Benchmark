import docker
import os
import tarfile
import io

client = docker.from_env()

container_name = "node1"
#Make sure only one is uncommented at a time:

#regular schema, Uncomment if you want to load the tables. 

#sql_clear = "../BD_SQL_scripts/clear_regular_script.sql"
#sql_clear_dest = "/tmp/clear_script.sql"

#star schema, Uncomment if you want to load the tables

sql_clear = "../BD_SQL_scripts/clear_star_script.sql"
sql_clear_dest = "/tmp/clear_script.sql"


if not os.path.exists(sql_clear):
    raise FileNotFoundError(f"SQL script not found at {sql_clear}")

tar_stream = io.BytesIO()
with tarfile.open(fileobj=tar_stream, mode='w') as tar:
    tar.add(sql_clear, arcname=os.path.basename(sql_clear_dest))
tar_stream.seek(0)

container = client.containers.get(container_name)

print(f"Copying {sql_clear} to {container_name}:{sql_clear_dest}")
container.put_archive(os.path.dirname(sql_clear_dest), tar_stream)

# Step 2: Create and execute the command using exec_create and exec_start
sqlcmd_command = f"sqlcmd < {sql_clear_dest}"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{sqlcmd_command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

remove_script = f"rm {sql_clear_dest}"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c"{remove_script}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("Process completed.")
