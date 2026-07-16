# Autonomous Coding Agent

An autonomous coding assistant built from scratch using the Gemini API. 

Unlike a standard LLM chatbot that simply waits for prompts, this project implements an autonomous **stateful reasoning loop**. It enables the agent to plan tasks, execute local file system tools, observe the results, and iterate on its code until the goal is achieved.

## Agent vs LLM:

This project explores the transition from static code generation to autonomous software engineering. The agent follows a continuous cycle:

1. **Thinking:** Evaluates the user's request and decides if it needs more information or if it can take action.
2. **Acting (Tool-Calling):** Outputs structured function calls (e.g., `write_file`, `run_python`, `get_files_info`) rather than just text.
3. **Observing:** The local environment executes the requested tool and feeds the raw output (or error traceback) back to the model.
4. **Adapting:** The agent reads the execution result, self-corrects if there are bugs, and plans its next move.

## Features

* **Custom Tool-Calling:** Directly interacts with the local file system.
* **State Management:** Maintains full interaction history, preserving the model's reasoning traces across turns.
* **Autonomous Error Recovery:** Capable of reading Python tracebacks and rewriting code until it executes successfully.

## Disclaimer
   - To ensure safe execution, the agent is restricted to working within a provided demo calculator application. The working directory is hardcoded into the agent's logic to act as a security boundary, preventing it from reading or modifying unrelated personal files on your local machine.
   - Run this at your own risk. This project is not production-ready. While basic guardrails like directory sandboxing are implemented, this is fundamentally an educational proof-of-concept. Autonomous agents can be unpredictable; do not run this in a sensitive environment or grant it access to critical file systems.

## Installation

### Prerequisites
* Python 3.10+
* A Google Gemini API Key

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/SrikarR8/CodingAgent.git](https://github.com/SrikarR8/CodingAgent.git)
   cd CodingAgent
   ```
2. **Setup Virtual Enviorment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. **Add API KEY**
   Create a .env file and add your Gemini API Key
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the Agent
 * The agent can be run with the following command:
  ```bash
   python main.py "Enter your prompt here"
  ```
  For best results specify to the agent that its tools are already in the calculator directory

### Acknowledgements
* This project was heavily inspired by [this freecodecamp](https://youtu.be/YtHdaXuOAks?si=CtFcfx6u3QJRxDAV) tutorial. Significant parts of this tutorial are outdated, consult the [Gemini API Docs](https://ai.google.dev/gemini-api/docs) as well
