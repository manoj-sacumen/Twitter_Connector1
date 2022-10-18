"""Collector module is the main module which will get data from Twitter API."""
import datetime
import json

from sac_requests.context.request import Response

from src.api_config import API_URL, QUERY_TEMPLATE, STORE_DIR
from src.authentications import Authentications
from src.file_writer import FileWriter
from src.log import log
from src.request_handler import RequestHandler
from src.std_log import (BEARER_TOKEN, ERROR_CODE_LIST, MAKING_REQUEST,
                         PREPARING_TO_GET_DATA, SET_URL_PATH,
                         STORE_FAILURE_DATA, STORE_SUCCESS_DATA,
                         SUCCESS_CODE_LIST, UN_DEFINED_CODE)


class Collector:
    """Collector module is the main module which will get data from Twitter API."""

    def __init__(self) -> None:
        """Collector will be sending requests to External resources."""
        """Request will be sent with the help of auth and config modules and received data will be stored."""
        self.auth: Authentications = Authentications()
        self.token_type = self.auth.get_token_type()
        self.auth_token: str = self.get_auth_token()
        self.file_writer: FileWriter = FileWriter()
        self.headers: dict = {'Authorization': self.auth_token}
        self.querystring: str = ''
        self.end_point: str = ''
        self.response: Response = Response()
        self.current_key: str = ''
        self.method: str = ''
        self.url_path: str = ''
        self.data_fetch_pending: bool = True
        self.next_token: str = ''
        self.params: dict = {}
        self.request_handel = RequestHandler(headers=self.headers, host=API_URL, auth_type=BEARER_TOKEN)

    def generate_querystring(self, param: dict) -> None:
        """Generate query string.

        Args:
            param (dict): Contains all valid Query filed with proper value,
            All values are defined as per config
        """
        self.querystring = ''.join(
            f'{key}={val}&' for key, val in param.items()).rstrip('&')

    def get_end_point(self) -> None:
        """Get end point by combining url path and query string."""
        self.end_point = f"{self.url_path}?{self.querystring}"

    def get_auth_token(self) -> str:
        """Get Authentication token.

        Returns:
            str: Authentication token
        """
        api_token = self.auth.get_api_token()
        return f'{self.token_type} {api_token}'

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
                log.error(ERROR_CODE_LIST[status_code] + f'\nwith {self.end_point}')
                file_path = f'{STORE_DIR}/failure_{self.current_key}.json'
            else:
                log.error(UN_DEFINED_CODE, str(status_code), str(self.response.text))
                file_path = f'{STORE_DIR}/undefined_{self.current_key}.json'
            log.info(STORE_FAILURE_DATA, file_path)
            self.file_writer.write_response_to_file(
                filepath=file_path, content_type='json', response=self.response)
            self.data_fetch_pending = False
            self.next_token = ''

    def get_tweets(self) -> None:
        """Get Tweets acts as main function which will carry out steps for each parameter set as defined in config.

        Args:
            params (dict): holds request parameters details
        """
        for key, value in self.params.items():
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
                self.get_end_point()
                self.response = self.request_handel.send_get_request(endpoint=self.end_point)
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

    def create_query_params(self, params, name):
        """Create new parameters dict by filling user input in predefined template."""
        temp_param, query_params, name_of_query = {}, {}, 'Data_on_'
        now = datetime.datetime.now
        today = now().strftime("%Y-%m-%dT00:00:00Z")
        tomorrow = (now() + datetime.timedelta(1)).strftime("%Y-%m-%dT00:00:00Z")
        if "user_id" in params:
            temp_param = QUERY_TEMPLATE['tweets_by_user_id']
            query_params = temp_param['query_params']
            temp_param["user_id"] = params.get("user_id")
        else:
            temp_param = QUERY_TEMPLATE['recent_tweets_query']
            query_params = temp_param['query_params']
            query_params["query"] = params.get("query")

        query_params["start_time"] = params.get("start_time", today)
        query_params["end_time"] = params.get("end_time", tomorrow)
        query_params["max_results"] = params.get("max_results", 10)
        name_of_query += name
        self.params.update({name_of_query: temp_param})


if __name__ == '__main__':  # pragma: no cover
    # Get tweets by recent search and user id
    """
    Note on parameters:
    1. start_time should not be older than 7 days.
    2. end_time should not be older than start_time.
    3. time format should be in 'YYYY-MM-DDTHH:MM:SSZ'
    4. max_results should be between 10 and 100.
    5. user.fields should be in coma separated format.
    """
    today_tweets = {"query": "India", "max_results": 1}
    tweets_by_datetime = {"query": "India",
                          "start_time": "2022-10-09T00:00:00Z",
                          "end_time": "2022-10-09T02:00:00Z",
                          "max_results": 100}

    user_tweets = {"user_id": 54829997, "start_time": "2022-10-07T00:00:00Z", "end_time": "2022-10-11T00:00:00Z",
                   "user.fields": "created_at"}
    col = Collector()
    col.create_query_params(today_tweets, name='today_tweets')
    # col.create_query_params(tweets_by_datetime, name='9th_Oct_2022_tweets')
    # col.create_query_params(user_tweets, name='user_54829997_tweets')
    col.get_tweets()
