import os
from google.genai import types

# working_directory is the full scope of our project, it is the directory of the entire project

# directory is one of the dirs in the working_directory, if an arg is passed in here then, we only crawl on that specific dir
# otherwise the "." will be used, which means crawl only working_directory 

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory,directory))

    #If the absolute path of the directory we want to focus on doesnt start with the working directory, then we want to terminate
    #this way we can make sure the agent doesnt crawl files outside the scope of the project and compromise sensitive info
    if not abs_dir.startswith(abs_working_dir):

        #We return a string here (instead of throwing an exception) so the LLM can read the error
        return f"Error: {directory} is not in the working directory"
    
    #Iterate through each content (file or dir) inside the specified dir
    #Append file info to the response
    res = ""
    contents = os.listdir(abs_dir)
    for content in contents:
        #Join the name of the current file to the dir path we are crawling
        content_path = os.path.join(abs_dir,content)

        #Get the 3 attributes of the content that we need for the LLM
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)

        print(f"Getting info of files in {content_path} directory")

        res += f" - {content}: file_size={size} bytes, is_dir={is_dir} \n" 

    return res

#Describes the function above for the LLM to call
schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)