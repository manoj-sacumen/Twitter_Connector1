"""File writer module will provide capability to write the response to desired file in defined way."""
import json
import os
from typing import Union

from src.log import log
from src.std_log import (BYTES_CONTENT, CREATED_DIR, EXCEPTION_OCCURRED,
                         FILE_EXISTS_ERROR, JSON_DECODE_ERROR, TEXT_CONTENT,
                         WRITING_FILE_COMPLETED)


class FileWriter:
    """File Writer class  writes file."""

    def __init__(self):
        """File writer class writes file, currently writing response is main usage."""
        self.text_content: list = TEXT_CONTENT
        self.bytes_content: list = BYTES_CONTENT
        self.mode: str = 'w'
        self.data: dict = {}
        self.content_type: str = ''
        self.file_path: str = ''
        self.response: object = None

    def sett(self, filepath, content_type, response) -> None:
        """Set parameter variables to instance variables.

        Args:
            filepath (str): path of the file
            content_type (str): type of content to be written
            response (response object): response object
        """
        self.file_path = filepath
        self.content_type = content_type
        self.response = response

    def reset(self) -> None:
        """Re setting the values of instance variable to initial values."""
        self.__init__()

    @staticmethod
    def path_exists(path) -> bool:
        """Check for does path exist.

        Args:
            path (str): path that need to be checked
        Returns:
            bool: if exists True else False
        """
        return bool(os.path.exists(path))

    @staticmethod
    def get_parent_path(path) -> str:
        """Get the parent folder path.

        Args:
            path (str): path for which parent folder need to be known
        Returns:
            str: parent folder path
        """
        return str(os.path.dirname(path))

    @staticmethod
    def create_dirs(path) -> None:
        """Create directory for given path.

        Args:
            path (str): path which need to be created
        """
        try:
            os.makedirs(path, exist_ok=True)
            log.info(CREATED_DIR + f' {path}')
        except FileExistsError as exception:
            log.error(FILE_EXISTS_ERROR + path + exception)

    def load_response_text_in_json(self) -> dict:
        """Load json data from the response and handles Exceptions.

        Returns:
            dict: response data that need to be stored
        """
        data = {}
        try:
            data = json.loads(self.response.text)
        except json.decoder.JSONDecodeError:
            log.error(JSON_DECODE_ERROR + f'for response {self.response}')
        return data.get('data', data)

    def get_data_to_write(self) -> Union[str, dict, bytes]:
        """Select data from Response object Based on content_type required.

        Returns:
            request.response: response data
        """
        try:
            if self.content_type in self.text_content:
                if self.content_type == 'json':
                    return self.load_response_text_in_json()
                return self.response.text
            return bytes(self.response.content)
        except Exception as exception:
            log.error(EXCEPTION_OCCURRED % (exception))
            return {}

    def check_for_file_dir_existence(self) -> None:
        """Check for dir exists, else create it."""
        file_dir = self.get_parent_path(self.file_path)
        if not self.path_exists(file_dir):
            self.create_dirs(file_dir)
            log.info(CREATED_DIR % (file_dir))

    def select_mode(self) -> str:
        """Select mode of writing file based on file existence and type of content need to be written.

        Returns:
            str: mode of file writing.
        """
        path_exists = self.path_exists(self.file_path)
        if self.content_type in self.text_content:
            return 'a' if path_exists else 'w'
        return 'ab' if path_exists else 'wb'

    def write_json_file(self) -> None:
        """Write json file."""
        with open(self.file_path, mode=self.mode) as w_file:
            json.dump(self.data, w_file, indent=4, sort_keys=True)

    def write_response_to_file(self, filepath: str, response: object, content_type: str) -> None:
        """Write received response to file.

        Args:
            filepath (str): path of the file should be stored.
            response (response object): https response object.
            content_type (str): content type of data to be stored.
        """
        try:
            self.sett(filepath=filepath, response=response,
                      content_type=content_type)
            self.data = self.get_data_to_write()
            self.mode = self.select_mode()
            self.check_for_file_dir_existence()
            self.write_json_file()
            log.info(WRITING_FILE_COMPLETED % (self.file_path))
        except Exception as exception:
            log.error(EXCEPTION_OCCURRED % str(exception))
        finally:
            self.reset()
