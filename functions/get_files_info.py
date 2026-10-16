import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        final_string = ""

        try:
            dir_list = os.listdir(target_dir)
        except Exception as e:
            return f'Error: directory list could not be retrieved due to error {e}'

        for item in dir_list:
            full_path = target_dir + "/" + item
            try:
                file_size = os.path.getsize(full_path)
            except Exception as e:
                return f'Error: file size could not be retrieved due to error {e}'
            try:
                is_dir = os.path.isdir(full_path)
            except Exception as e:
                return f'Error: directory status could not be found due to error {e}'
            item_string = f"- {item}: file_size={file_size}, is_dir={is_dir}\n"
            final_string += item_string

        return final_string
    except Exception as e:
        return f'Error: encountered unexpected error {e}'
