import os
from google.genai import types

MAX_CHARS = 10000

# working_directory is the full scope of our project, it is the directory of the entire project.
#  We keep track of it to make sure the agent does not access files outside of context

# File path is the path to the file that we are interested in getting the contents of

def get_file_content(working_dir, file_path):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir,file_path))

    #Check if the file the agent is attempting to read is in the working directory 
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not in the working dir"
    
    #Return an error message if the file does not exist
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"
    
    #Read the contents of the file as a string
    file_content_string = ""
    try:
        print(f"Getting contents of {abs_file_path}")
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += (
                    f'[... File "{file_path}" truncated at 10000 characters]'
                )
    except Exception as e:
        return f"Excpetion reading file: {e}"
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description="Gets the contents of the given file as a string, constrained to the working directory",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file from the working directory",
            ),
        },
    ),
)