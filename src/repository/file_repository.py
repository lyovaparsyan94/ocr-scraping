import json
import os
from os.path import join

from config import configs
from repository.abc_pdf_scan_repository import AbstractFileRepository


class FileRepository(AbstractFileRepository):

    def save_data(self, data: dict, filename: str) -> None:
        """
        Saves data to a specified file in JSON format.

        Args:
            data (dict): The data to be saved (as a dictionary).
            filename (str, optional): Path to the data file. Defaults to configs.dir_configs.PATH_TO_SAVE.

        Raises:
            PermissionError: If the file cannot be written due to permission issues.
        """
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def create_file(self, filename: str, text: str) -> None:
        """
        Creates a text file with the specified content.

        Args:
            filename (str): Path to the output file.
            text (str): Text content to write.

        Returns:
            None: Saves the text to the specified file.
        """

        with open(filename, 'w') as file:
            file.write(text)

    def read_json_file(self, filename: str) -> dict:
        """
        Retrieves the current data from a specified file.

        Args:
            filename (str, optional): Path to the data file. Defaults to configs.dir_configs.PATH_TO_SAVE.

        Returns:
            dict: A dictionary containing the loaded data.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If the file content cannot be decoded as JSON.
        """
        try:
            with open(filename) as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON data from '{filename}'. Check the file format.")

    def get_files_dir(self, file_dir: str = configs.DIR_CONFIG.INITIAL_DATA_DIR, abspath: bool = False) -> list[str]:
        """
        Retrieves a list of all files in the specified directory.

        Args:
            file_dir (str, optional): Directory containing files. Defaults to INITIAL_DATA_DIR.
            abspath (bool, optional): Return absolute paths. Defaults to False.

        Returns:
            List[str]: List of filenames.
        """
        files = os.listdir(file_dir)
        if abspath:
            files_abspath = [join(configs.DIR_CONFIG.INITIAL_DATA_DIR, pdf) for pdf in files]
            return files_abspath
        return files
