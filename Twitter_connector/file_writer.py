# standard library's
import os
import json
# third party library's

# local library's
from log import log
from std_log import (
    JSON, DATA, JSON_DECODE_ERROR, EXCEPTION_OCCURRED, CREATEDDIR, WRITEINGFILECOMPLETED)


class File_Writer:

    def __init__(self):
        """File writer writes file
        currently writing response is main usage
        """
        self.text_content = ['html', 'json', 'yaml']
        self.bytes_content = ['jpg', 'png', 'zip', 'xls']
        self.mode = 'w'
        self.data = {}
        self.content_type = ''
        self.file_path = ''
        self.response = None

    def sett(self, filepath, content_type, response) -> None:
        """ Sets parameter variables to instance variables
        Args:
            filepath (str): path of the file
            content_type (str): type of content to be writhen
            response (response object): response object
        """
        self.file_path = filepath
        self.content_type = content_type
        self.response = response

    def reset(self) -> None:
        """Re setting the values of instance variable to initial values"""
        self.__init__()

    def path_exists(self, path) -> bool:
        """Checks for does path exists
        Args:
            path (str): path that need to be checked
        Returns:
            bool: if exists True else False
        """
        return os.path.exists(path)

    def get_parent_path(self, path) -> str:
        """Gets the parent folder path
        Args:
            path (str): path for which parent folder need to be known
        Returns:
            str: parent folder path
        """
        return os.path.dirname(path)

    def create_dirs(self, path) -> None:
        """Creates directory for given path 

        Args:
            path (str): path which need to be created
        """
        os.makedirs(path,exist_ok=True)
        log.info(CREATEDDIR + f' {path}')

    def load_json_data(self) -> dict:
        """ Loads json data from the response and 
        handles Exceptions
        Returns:
            dict: response data that need to be stored
        """

        try:
            data = json.loads(self.response.text)
        except json.decoder.JSONDecodeError:
            log.error(JSON_DECODE_ERROR + f'for response {self.response}')
        return data.get(DATA, data)

    def get_data_to_write(self) -> str | dict | bytes:
        """Selecting data from Response object
            Based on content_type required
        Returns:
            request.response: response data
        """
        try:
            if self.content_type in self.text_content:
                if self.content_type == JSON:
                    return self.load_json_data()
                else:
                    return self.response.text
            else:
                return self.response.content
        except Exception as e:
            log.error(EXCEPTION_OCCURRED + f'{e}')

    def check_for_file_dir_existence(self) -> None:
        """checking for dir exists, else create it
        """
        file_dir = self.get_parent_path(self.file_path)
        if not self.path_exists(file_dir):
            self.create_dirs(file_dir)
            log.info(CREATEDDIR + file_dir)

    def select_mode(self) -> str:
        """Selects mode of writing file based on file
        existence and type of content need to be written

        Returns:
            str: mode of file writing
        """
        path_exists = self.path_exists(self.file_path)
        if self.content_type in self.text_content:
            return 'a' if path_exists else 'w'
        elif self.content_type in self.bytes_content:
            return 'ab' if path_exists else 'wb'

    def write_json_file(self) -> None:
        """ write json file
        """
        with open(self.file_path, mode=self.mode) as w_file:
            json.dump(self.data, w_file, indent=4, sort_keys=True)

    def write_response_to_file(self, filepath, response, content_type) -> None:
        """Write received response to file
        Args:
            filepath (str): path of the file should be stored
            response (response object): https response object
            content_type (str): content type of data to be stored
        """
        try:
            self.sett(filepath=filepath, response=response,
                    content_type=content_type)
            self.data = self.get_data_to_write()
            self.mode = self.select_mode()
            self.check_for_file_dir_existence()
            self.write_json_file()
            log.info(WRITEINGFILECOMPLETED + self.file_path + '.')
        except Exception as e:
            log.error(EXCEPTION_OCCURRED,e)
        finally:
            self.reset()
