import os
from google.genai import types

#This function, unlike a production-ready agent, will not be able to splice the file and such but it will rewrite the file to make its additions.
def write_file(working_dir, file_path, content):
    
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir,file_path))

    #Check if the file the agent is attempting to read is in the working directory 
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not in the working dir"
    
    #Get the parent directory, if it doesnt exist, try and create it, if unable to create return the exception
    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"could not create parent dirs: {parent_dir} = {e}"

    #Logic for writing to file
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
            retStr = f'successfully wrote "{file_path}" ({len(content)}) characters'
            print(retStr)
        return(
            retStr
        )
    except Exception as e:
        return f"Failed to write to file: {file_path}, {e}"
    
schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description="overwrites a file or writes to a new file if it does not exist (and creates required parent dirs safely), constrained to the working directory",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to write to the file as a string",
            ),
        },
    ),
)