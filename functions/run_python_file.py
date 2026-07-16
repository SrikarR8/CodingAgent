import os
import subprocess
from google.genai import types


def run_python_file(working_dir, file_path :str, args = [] ):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir,file_path))

    #Check if the file the agent is attempting to read is in the working directory 
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not in the working dir"
    
    #Return an error message if the file does not exist
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"
    
    #Return an error if the agent is accessing a non python file
    if not file_path.endswith(".py"):
        return f"Error: {file_path} is not a python file"

    try:
        final_args = ["python3", file_path]
        final_args.extend(args)

        output = subprocess.run(
            final_args, cwd = abs_working_dir, timeout=30, capture_output=True, text=True
            )
        print(f"Executing {file_path}")
        finalStr =  f"""
        STDOUT: {output.stdout}
        STDERR: {output.stderr}
        """
        if output.returncode != 0:
            finalStr+= f"Process exited with exit code: {output.returncode}"
        if output.stdout == "" and output.stderr == "":
            finalStr = "No output produced \n"
        
        return finalStr
    except Exception as e:
        return f"Error executing python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description="Runs a python file with python3 interpreter. Accepts additional CLI args as an optional array.",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to be used as the CLI args for the python file",
                items=types.Schema(
                    type=types.Type.STRING
                )
            ),
        },
    ),
)



