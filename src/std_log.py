"""Std log module acts as placeholder for log statements which will be used though out the application."""

LOG_SETUP_DONE = 'Logging setup is done.'
GET_API_KEY = 'Getting API key from env.'
GET_API_SECRET_KEY = 'Getting API secret key from env.'
GET_API_TOKEN = 'Getting API token key from env.'
MAKING_REQUEST = 'Making request for '
STORE_SUCCESS_DATA = 'Storing successful data in %s'
WRITING_FILE_COMPLETED = 'Writing file completed, in file path: %s'
CREATED_DIR = 'Created Directory: %s'
STORE_FAILURE_DATA = 'Storing Failure data in %s'
SET_URL_PATH = 'Setting URL path done for search type: %s'
LOAD_ENV_FILE = 'Loading env variables from env file'
EXCEPTION_OCCURRED = 'An Un-handled Exception occurred at %s'
JSON_DECODE_ERROR = 'Json Decoding failed '
FILE_EXISTS_ERROR = 'An FileExistsError Exception raised for path: '
PREPARING_TO_GET_DATA = 'Preparing to get data for %s parameters.'

# Standard HTTP Response code logs
RESPONSE200 = 'Response is success with status code 200.'
RESPONSE201 = ''
RESPONSE203 = ''
SUCCESS_CODE_LIST = {200: RESPONSE200,
                     201: RESPONSE201,
                     203: RESPONSE203}

RESPONSE500 = ''
RESPONSE400 = 'Invalid Request,One or more parameters to your request was invalid.'
RESPONSE401 = 'Resource Unauthorized'
RESPONSE404 = 'Resource Not Found'
RESPONSE429 = 'Rate limit exceeded.'
UN_DEFINED_CODE = 'Un defined Status code received define it,Details: %s-%s'

ERROR_CODE_LIST = {500: RESPONSE500,
                   400: RESPONSE400,
                   404: RESPONSE404,
                   429: RESPONSE429}

# Standard keywords
TEXT_CONTENT = ['text', 'html', 'json', 'yaml']
BYTES_CONTENT = ['jpg', 'png', 'zip', 'xls']
