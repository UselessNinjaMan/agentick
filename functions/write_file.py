import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        write_target = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_file = os.path.commonpath([abs_path, write_target]) == abs_path
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(write_target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(write_target), exist_ok=True)

        with open(write_target, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: encountered unexpected error {e}'
