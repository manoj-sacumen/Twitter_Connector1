LOGSETUPDONE = 'Logging setup is done.'
GETAPIKEY = 'Getting API key from env.'
GETAPISECRETKEY = 'Getting API secret key from env.'
GETAPITOKEN = 'Getting API token key from env.'
SETAPIKEY = 'Setting API key to env done.'
SETAPISECRETKEY = 'Setting API secret key to env done.'
SETAPITOKEN = 'Setting API token key to env done.'
MAKEINGREQUEST = 'Making request for '
STROESUCCESSDATA = 'Storing successful data in'
WRITEINGFILECOMPLETED = 'Writing file completed, in file path: '
CREATEDDIR = 'Created Directory:'
STROEFAILUREDATA = 'Storing Failure data in'
SETURLPATH = 'Setting URL path done for search type:'
LOADENVFILE = 'Loading env variables from env file'
# Debug logs
# Info logs
# Error logs
EXCEPTION_OCCURRED = 'An Un-handled Exception occurred at'
JSON_DECODE_ERROR = 'Json Decoding failed '
# Critical logs



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
UN_DEFINED_CODE = 'Un defined Status code received define it'

ERROR_CODE_LIST = {500: RESPONSE500,
                   400: RESPONSE400,
                   404: RESPONSE404,
                   429: RESPONSE429}


# Standard keywords
NEXT_TOKEN = 'next_token'
META = 'meta'
DATA = 'data'

# file types
JSON = 'json'
