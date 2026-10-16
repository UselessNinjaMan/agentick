import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes the specified Python file within the working directory, and returns a string output.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of arguments to provide to the subprocess.run() function",
                },
            },
            "required": ["file_path"]
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30)

        final_string = ""

        if completed_process.returncode != 0:
            final_string += f"Process exited with code {completed_process.returncode}"
        if not completed_process.stdout and not completed_process.stderr:
            final_string += "\nNo output produced"
        else:
            final_string += f"\nSTDOUT: {completed_process.stdout}"
            final_string += f"\nSTDERR: {completed_process.stderr}"

        return final_string

    except Exception as e:
        return f'Error: executing Python file: {e}'
