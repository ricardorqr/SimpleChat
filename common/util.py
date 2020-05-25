import os


class Util:

    @staticmethod
    def find_file(file_name):
        for directory_path, directory_names, files in os.walk('.'):
            for file_name_in_directory in files:
                if file_name_in_directory == file_name:
                    return os.path.join(directory_path, file_name_in_directory)
