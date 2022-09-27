# standard library's
import os
import sys
sys.path.append("./Twitter_connector")      # needs better solution for relative import issue.
# third party library's 
import pytest
# local library's
from authentications import Authentications
from log import log

auth=Authentications()

def test_get_api_token():
    assert auth.get_api_token()==os.environ['API_TOKEN']

def test_get_api_key():
    assert auth.get_api_key()==os.environ['API_KEY']

def test_get_api_secret_key():
    assert auth.get_api_secret_key()==os.environ['API_SECRET_KEY']

# set functionalities test cases will be written if auto key generation is possible.