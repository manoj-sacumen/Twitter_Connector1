# Standard library's
import os
import json
import traceback

# third party library's
import requests
# local library's
from Twitter_connector.log import log
from Twitter_connector.authentications import Authentications
from Twitter_connector.api_config import API_URL, PARAMS, STORE_DIR
from Twitter_connector.file_writer import FileWriter
from Twitter_connector.std_log import (
    MAKEINGREQUEST, STROESUCCESSDATA, ERROR_CODE_LIST, SUCCESS_CODE_LIST,
    STROEFAILUREDATA, SETURLPATH, NEXT_TOKEN, META,
    UN_DEFINED_CODE)


class Collector:

    def __init__(self) -> None:
        """
        Collector will be sending requests to External resources with the help of
        Auth and config modules and received data will be stored.
        """
        self.auth = Authentications()
        self.auth_token = self.get_auth_token()
        self.file_writer = FileWriter()
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
        self.querystring = ''.join(
            f'{key}={val}&' for key, val in param.items()).rstrip('&')

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
            self.file_writer.write_response_to_file(
                filepath=file_path, content_type='json', response=self.response)
            self.check_for_next_page_data()
        else:
            if sc in ERROR_CODE_LIST:
                log.error(ERROR_CODE_LIST[sc]+f'\nwith {self.url}')
                file_path = f'{STORE_DIR}/failure_{self.current_key}.json'
            else:
                log.error(UN_DEFINED_CODE + f'{sc, self.response.text}')
                file_path = f'{STORE_DIR}/undefined_{self.current_key}.json'
            log.info(STROEFAILUREDATA + file_path)
            self.file_writer.write_response_to_file(
                filepath=file_path, content_type='json', response=self.response)
            self.data_fetch_pending = False
            self.next_token = ''

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
            # temp settings: taking only 2 next token request
            while self.data_fetch_pending and pages_limit <= 2:
                pages_limit += 1
                if self.next_token:
                    token_key = 'pagination_token' if value['search_type']=='By_User_ID' else 'next_token'
                    value['query_params'][token_key] = self.next_token
                self.generate_querystring(param=value['query_params'])
                self.create_url()
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


if __name__ == '__main__':              # pragma: no cover
    try:
        # Get tweets by recent search
        c1 = Collector()
        c1.get_tweets(PARAMS)
    except Exception as e:
        print(e)
        log.error(e)
