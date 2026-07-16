import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_contents import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function

# Max iterations for the agentic loop. These can be overridden with env vars.
MAX_ITERS = int(os.getenv("MAX_ITERS", "20"))
REQUEST_DELAY_SECONDS = float(os.getenv("REQUEST_DELAY_SECONDS", "15.0"))

#declare the 4 schemas of the 4 tools the AI can use
def build_config(system_prompt: str):
    return types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[
            types.Tool(
                function_declarations=[
                    schema_get_files_info,
                    schema_get_file_content,
                    schema_run_python_file,
                    schema_write_file,
                ]
            )
        ],
    )


def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # System prompt trumps all user prompts, the LLM follows this prompt first and prioritizes it over any user or tool prompts
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read the contents of a file
        - Write to a file (create or update)
        - Run a python file with optional arguements

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    #Check if user provided the LLM a prompt in the CLI
    if len(sys.argv) < 2:
        print("No prompt provided")
        sys.exit(1)
    verbose_flag = False

    #If verbose flag is passed in the CLI, set it to true
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True
    prompt = sys.argv[1]


    config = build_config(system_prompt)

    #Initialize chat history with the initial prompt
    history = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    #Run the agentic loop at most until max iters is reached
    for i in range(MAX_ITERS):


        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=history,
            config=config,
        )

        if response is None or response.usage_metadata is None:
            print("response is malformed")
            return
        
        model_content = response.candidates[0].content
        
        if verbose_flag:
            print(f"User Prompt: {prompt}")
            print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response Tokens: {response.usage_metadata.candidates_token_count}")

        history.append(model_content)

        function_calls = getattr(response, "function_calls", None)
        if function_calls:
            for function_call_part in function_calls:
                history.append(call_function(function_call_part, verbose_flag))

            if i < MAX_ITERS - 1:
                time.sleep(REQUEST_DELAY_SECONDS)

        else:
            #Final agent text
            print(response.text)
            break




if __name__ == "__main__":
    main()