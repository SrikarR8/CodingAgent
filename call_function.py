from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

from google.genai import types

working_dir = "calculator"
def call_function(function_call_part, verbose = False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    res = "" 

    if function_call_part.name == "get_files_info":
        res = get_files_info(working_dir, **function_call_part.args)
    if function_call_part.name == "get_file_content":
        res = get_file_content(working_dir, **function_call_part.args)
    if function_call_part.name == "run_python_file":
        res = run_python_file(working_dir, **function_call_part.args)
    if function_call_part.name == "write_file":
        res = write_file(working_dir, **function_call_part.args)
    
    if res == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name = function_call_part.name,
                    response={"error":f"Unknown function: {function_call_part.name}"} 
                )
            ]
        )

    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name = function_call_part.name,
                    response={"result":res} 
                )
            ]
        )
    