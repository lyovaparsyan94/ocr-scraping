from abc import ABC, abstractmethod


class AbstractFileRepository(ABC):

    @abstractmethod
    def read_json_file(self, filename: str) -> dict:
        """
        Read data from a JSON file.

        Args:
            filename (str): Name of the JSON file to read.

        Returns:
            Dict: Parsed data from the JSON file.
        """
        pass

    @abstractmethod
    def create_file(self, filename: str, content: str) -> None:
        """
        Create a text file with the specified content.

        Args:
            filename (str): Name of the file to create.
            content (str): Text content to write.

        Returns:
            None: Creates the file in the specified directory.
        """
        pass

    def save_data(self, data: dict, filename: str) -> None:
        """
        Saves data to a specified file in JSON format.

        Args:
            data (dict): The data to be saved (as a dictionary).
            filename (str, optional): Path to the data file.
        """
        pass
