import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        MAX_CHARS = 10000
        abs_path = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_file = os.path.commonpath([abs_path, target]) == abs_path
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...file "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string

    except Exception as e:
        return f'Error: encountered unexpected error {e}'
