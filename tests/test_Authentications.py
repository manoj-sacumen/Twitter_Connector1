# standard library's
import os
import sys
# needs better solution for relative import issue.
# third party library's
# local library's
from Twitter_connector.authentications import Authentications

sys.path.append("./Twitter_connector")
auth = Authentications()


def test_get_api_token():
    assert auth.get_api_token() == os.environ['API_TOKEN']


def test_get_api_key():
    assert auth.get_api_key() == os.environ['API_KEY']


def test_get_api_secret_key():
    assert auth.get_api_secret_key() == os.environ['API_SECRET_KEY']


def test_get_token_type():
    assert auth.get_token_type() == os.environ['TOKEN_TYPE']


def test_load_env_file():
    # https://adamj.eu/tech/2020/10/13/how-to-mock-environment-variables-with-pytest/
    # print(os.environ['TOKEN_TYPE'])
    auth.load_env_file()
    # still need to figure which method to test


# set functionalities test cases will be written if auto key generation is possible.
