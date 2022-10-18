"""Std log module acts as placeholder for log statements which will be used though out the application."""

LOG_SETUP_DONE = 'Logging setup is done.'  # nosec
GET_API_KEY = 'Getting API key from env.'  # nosec
GET_API_SECRET_KEY = 'Getting API secret key from env.'  # nosec
GET_API_TOKEN = 'Getting API token key from env.'  # nosec
MAKING_REQUEST = 'Making request for %s'  # nosec
STORE_SUCCESS_DATA = 'Storing successful data in %s'  # nosec
WRITING_FILE_COMPLETED = 'Writing file completed, in file path: %s'  # nosec
CREATED_DIR = 'Created Directory: '  # nosec
STORE_FAILURE_DATA = 'Storing Failure data in %s'  # nosec
SET_URL_PATH = 'Setting URL path done for search type: %s'  # nosec
LOAD_ENV_FILE = 'Loading env variables from env file'  # nosec
EXCEPTION_OCCURRED = 'An Un-handled Exception occurred at %s'  # nosec
JSON_DECODE_ERROR = 'Json Decoding failed, for response %s'  # nosec
FILE_EXISTS_ERROR = 'An FileExistsError Exception raised for path: '  # nosec
PREPARING_TO_GET_DATA = 'Preparing to get data for %s parameters.'  # nosec

# Standard HTTP Response code logs
RESPONSE200 = 'Response is success with status code 200.'  # nosec
SUCCESS_CODE_LIST = {200: RESPONSE200,
                     }

RESPONSE400 = 'Invalid Request,One or more parameters to your request was invalid.'  # nosec
RESPONSE401 = 'Resource Unauthorized'  # nosec
RESPONSE404 = 'Resource Not Found'  # nosec
RESPONSE429 = 'Rate limit exceeded.'  # nosec
UN_DEFINED_CODE = 'Un defined Status code received define it,Details: %s-%s'  # nosec

ERROR_CODE_LIST = {400: RESPONSE400,
                   404: RESPONSE404,
                   429: RESPONSE429}

# Standard keywords
TEXT_CONTENT = ['text', 'html', 'json', 'yaml']
BYTES_CONTENT = ['jpg', 'png', 'zip', 'xls']
BEARER_TOKEN = "BEARER_TOKEN"  # nosec
