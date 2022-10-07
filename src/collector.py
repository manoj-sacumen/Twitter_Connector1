"""Collector module is the main module which will get data from Twitter API."""
import json

import requests  # type: ignore

from src.api_config import API_URL, PARAMS, STORE_DIR
from src.authentications import Authentications
from src.file_writer import FileWriter
from src.log import log
from src.std_log import (ERROR_CODE_LIST, MAKING_REQUEST,
                         PREPARING_TO_GET_DATA, SET_URL_PATH,
                         STORE_FAILURE_DATA, STORE_SUCCESS_DATA,
                         SUCCESS_CODE_LIST, UN_DEFINED_CODE)


class Collector:
    """Collector module is the main module which will get data from Twitter API."""

    def __init__(self) -> None:
        """Collector will be sending requests to External resources."""
        """Request will be sent with the help of auth and config modules and received data will be stored."""
        self.auth: Authentications = Authentications()
        self.auth_token: str = self.get_auth_token()
        self.file_writer: FileWriter = FileWriter()
        self.headers: dict = {'Authorization': self.auth_token}
        self.payload: dict = {}
        self.querystring: str = ''
        self.url: str = ''
        self.response: requests.Response = requests.Response()
        self.current_key: str = ''
        self.method: str = ''
        self.url_path: str = ''
        self.data_fetch_pending: bool = True
        self.next_token: str = ''

    def generate_querystring(self, param: dict) -> None:
        """Generate query string.

        Args:
            param (dict): Contains all valid Query filed with proper value,
            All values are defined as per config
        """
        self.querystring = ''.join(
            f'{key}={val}&' for key, val in param.items()).rstrip('&')

    def create_url(self) -> None:
        """Create url by concatenating the parts of URL."""
        self.url = f"{API_URL}{self.url_path}?{self.querystring}"

    def get_auth_token(self) -> str:
        """Get Authentication token.

        Returns:
            str: Authentication token
        """
        token_type = self.auth.get_token_type()
        api_token = self.auth.get_api_token()
        return f'{token_type} {api_token}'

    def send_request(self) -> None:
        """Make a request for the defined parameters."""
        self.response = requests.request(
            self.method, self.url, headers=self.headers, data=self.payload)

    def handles_response(self) -> None:
        """Handle request responses."""
        """validate for success or failure and takes respective steps."""
        status_code = self.response.status_code
        if status_code in SUCCESS_CODE_LIST:
            log.info(SUCCESS_CODE_LIST[status_code])
            file_path = str(STORE_DIR) + "/success_" + str(self.current_key) + ".json"
            log.info(STORE_SUCCESS_DATA)
            self.file_writer.write_response_to_file(
                filepath=file_path, content_type='json', response=self.response)
            self.check_for_next_page_data()
        else:
            if status_code in ERROR_CODE_LIST:
                log.error(ERROR_CODE_LIST[status_code] + f'\nwith {self.url}')
                file_path = f'{STORE_DIR}/failure_{self.current_key}.json'
            else:
                log.error(UN_DEFINED_CODE, (str(status_code), str(self.response.text)))
                file_path = f'{STORE_DIR}/undefined_{self.current_key}.json'
            log.info(STORE_FAILURE_DATA, file_path)
            self.file_writer.write_response_to_file(
                filepath=file_path, content_type='json', response=self.response)
            self.data_fetch_pending = False
            self.next_token = ''

    def get_tweets(self, params: dict) -> None:
        """Get Tweets acts as main function which will carry out steps for each parameter set as defined in config.

        Args:
            params (dict): holds request parameters details
        """
        for key, value in params.items():
            log.info(PREPARING_TO_GET_DATA, str(key))
            self.current_key = key
            self.method = value['method']
            self.set_url_path(val=value)
            log.info(MAKING_REQUEST, str(self.current_key))
            pages_limit = 0  # temp dev purpose, to not utilize complete rate limit
            # temp settings: taking only 2 next token request
            while self.data_fetch_pending and pages_limit <= 2:
                pages_limit += 1
                if self.next_token:
                    token_key = 'pagination_token' if value['search_type'] == 'By_User_ID' else 'next_token'
                    value['query_params'][token_key] = self.next_token
                self.generate_querystring(param=value['query_params'])
                self.create_url()
                self.send_request()
                self.handles_response()
            self.data_fetch_pending = True
            self.next_token = ''

    def set_url_path(self, val: dict) -> None:
        """Set url path component as per config.

        Args:
            val (dict): holds request parameters details
        """
        search_type = val['search_type']
        path = val['path']
        if search_type in ['Recent_tweets']:  # Can be general cases
            self.url_path = path
        elif search_type == 'By_User_ID':  # specific settings
            user_id = val['user_id']
            self.url_path = '{}/{}/tweets'.format(str(path), str(user_id))
        log.info(SET_URL_PATH, str(search_type))

    def check_for_next_page_data(self) -> None:
        """Look for next_token to get next page data in success response."""
        data = json.loads(self.response.text)
        if 'meta' in data and 'next_token' in data['meta']:
            self.next_token = data['meta']['next_token']
        else:
            self.data_fetch_pending = False
            self.next_token = ''


if __name__ == '__main__':  # pragma: no cover
    # Get tweets by recent search
    col = Collector()
    col.get_tweets(PARAMS)
