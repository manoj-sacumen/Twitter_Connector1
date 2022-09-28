# Standard library's
import os
import json
import traceback

# third party library's
import requests
# local library's
from log import log
from authentications import Authentications
from api_config import API_URL, PARAMS, STORE_DIR
from std_log import (
    MAKEINGREQUEST, WRITEINGFILECOMPLETED, STROESUCCESSDATA, ERROR_CODE_LIST, SUCCESS_CODE_LIST,
    CREATEDDIR, STROEFAILUREDATA, SETURLPATH, NEXT_TOKEN, META, JSON, DATA,
    UN_DEFINED_CODE, JSON_DECODE_ERROR, EXCEPTION_OCCURRED)


class Collector:

    def __init__(self) -> None:
        """
        Collector will be sending requests to External resources with the help of
        Auth and config modules and received data will be stored.
        """
        self.auth = Authentications()
        self.auth_token = self.get_auth_token()
        self.headers = {'Authorization': self.auth_token}
        self.payload = {}
        self.querystring = ''
        self.url = ''
        self.response = None
        self.current_key = ''
        self.method = ''
        self.url_path = ''
        self.data_fetch_pending = True
        self.next_token = ''

    def generate_querystring(self, param: dict) -> None:
        """Generate query string
        Args:
            param (dict): Contains all valid Query filed with proper value,
            All values are defined as per config
        """
        self.querystring = ''.join(f'{key}={val}&' for key, val in param.items()).rstrip('&')

    def create_url(self) -> None:
        """ Creates url by concatenating the parts of URL"""
        self.url = f"{API_URL}{self.url_path}?{self.querystring}"

    def get_auth_token(self) -> str:
        """ Gets Authentication token

        Returns:
            str: Authentication token
        """
        token_type = self.auth.get_token_type()
        api_token = self.auth.get_api_token()
        return f'{token_type} {api_token}'

    def make_request(self) -> None:
        """makes a request for the defined parameters
        """
        self.response = requests.request(
            self.method, self.url, headers=self.headers, data=self.payload)

    def handles_response(self) -> None:
        """ handles request response,
        validates for success or failure
        and takes respective steps
        """

        sc = self.response.status_code
        if sc in SUCCESS_CODE_LIST:
            log.info(SUCCESS_CODE_LIST[sc])
            file_path = f'{STORE_DIR}/success_{self.current_key}.json'
            log.info(STROESUCCESSDATA + file_path)
            self.write_response_to_file(file_path=file_path)
            self.check_for_next_page_data()
        else:
            if sc in ERROR_CODE_LIST:
                log.error(ERROR_CODE_LIST[sc]+f'\nwith {self.url}')
                file_path = f'{STORE_DIR}/failure_{self.current_key}.json'
            else:
                log.error(UN_DEFINED_CODE + f'{sc, self.response.text}')
                file_path = f'{STORE_DIR}/undefined_{self.current_key}.json'
            log.info(STROEFAILUREDATA + file_path)
            self.write_response_to_file(file_path=file_path)
            self.data_fetch_pending = False
            self.next_token = ''

    def write_response_to_file(self, file_path: str, mode='W', content_type=JSON) -> None:
        """ Write received response to file
        Args:
            file_path (str): file path
            mode (str, optional): _description_. Defaults to 'w'.
            content_type (str, optional): _description_. Defaults to 'text'.
        """
        text_content = ['html', 'json', 'yaml']
        bytes_content = ['jpg', 'png', 'zip', 'xls']

        def load_json_file() -> dict:
            """ Loads json data from the response and 
            handles Exceptions

            Returns:
                dict: response data that need to be stored
            """
            _data = {}
            try:
                _data = json.loads(self.response.text)
            except json.decoder.JSONDecodeError:
                log.error(JSON_DECODE_ERROR + f'for response {self.response}')
            if DATA in _data:
                return _data[DATA]
            else:
                return _data

        def get_data_to_write() -> str | dict | bytes:
            """Selecting data from Response object
               Based on content_type required
            Returns:
                request.response: response data
            """
            try:
                if content_type in text_content:
                    if content_type == JSON:
                        return load_json_file()
                    else:
                        return self.response.text
                else:
                    return self.response.content
            except Exception as e:
                log.error(EXCEPTION_OCCURRED + f'{traceback.print_tb()}')

        def check_for_file_dir_existence() -> None:
            """checking for dir exists, else create it
            """
            file_dir = os.path.dirname(file_path)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
                log.info(CREATEDDIR + file_dir)

        def select_mode() -> str:
            """Selects mode of writing file based on file
            existence and type of content need to be written

            Returns:
                str: mode of file writing
            """
            path_exists = os.path.exists(file_path)
            if content_type in text_content:
                return 'a' if path_exists else 'w'
            elif content_type in bytes_content:
                return 'ab' if path_exists else 'wb'

        def write_json_file(filepath: str, _mode: str, _data: dict) -> None:
            """ write json file

            Args:
                filepath (str): file path of file
                _data (dict): Json data received from response
                _mode (str): mode of file opening
            """
            with open(filepath, mode=_mode) as w_file:
                json.dump(_data, w_file, indent=4, sort_keys=True)

        data = get_data_to_write()
        mode = select_mode()
        check_for_file_dir_existence()
        write_json_file(file_path, mode, data)
        log.info(WRITEINGFILECOMPLETED + file_path + '.')

    def get_tweets(self, params: dict) -> None:
        """Get Tweets acts as main function,
        which will carry out steps for each parameter set as defined in config.

        Args:
            params (dict): holds request parameters details
        """
        for key, value in params.items():
            log.info(f'Preparing to get data for {key} parameters.')
            self.current_key = key
            self.method = value['method']
            self.set_url_path(val=value)
            log.info(MAKEINGREQUEST + self.current_key)
            pages_limit = 0   # temp dev purpose, to not utilize complete rate limit
            while self.data_fetch_pending and pages_limit <= 2:     # temp settings: taking only 2 next token request
                pages_limit += 1
                if self.next_token:
                    value['query_params'][NEXT_TOKEN] = self.next_token
                self.generate_querystring(param=value['query_params'])
                self.create_url()
                print(self.url)
                self.make_request()
                self.handles_response()
            self.data_fetch_pending = True
            self.next_token = ''

    def set_url_path(self, val: dict) -> None:
        """ Sets url path component as per config
        Args:
            val (dict): holds request parameters details
        """
        search_type = val['search_type']
        path = val['path']
        if search_type in ['Recent_tweets']:  # Can be general cases
            self.url_path = path
        elif search_type == 'By_User_ID':  # specific settings
            user_id = val['user_id']
            self.url_path = f'{path}/{user_id}/tweets'
        log.info(SETURLPATH + f' {search_type}')

    def check_for_next_page_data(self) -> None:
        """
        Looking for next_token to get next page
         data in success response data
        """
        data = json.loads(self.response.text)
        if META in data and NEXT_TOKEN in data[META]:
            self.next_token = data[META][NEXT_TOKEN]
        else:
            self.data_fetch_pending = False
            self.next_token = ''


if __name__ == '__main__':
    # Get tweets by recent search
    c1 = Collector()
    c1.get_tweets(PARAMS)
