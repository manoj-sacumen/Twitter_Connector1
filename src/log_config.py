"""Log config module acts as placeholder for configuration related to logging functionality."""
# log format list
LOG_FORMATS = {'f1': '%(asctime)s %(levelname)s - %(message)s',
               'f2': '%(asctime)s p%(process)s %(module).15s.py at line %(lineno)d  %(levelname)s - %(message)s'
               }
LOG_FORMAT = LOG_FORMATS['f2']
# date format
DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'
# log file name
FILE_NAME = './logs/main_log.log'
# log file size(in MB)
FILE_SIZE = 1024
# log level
LOG_LEVELS = {'CRITICAL': 50,
              'ERROR': 40,
              'WARNING': 30,
              'INFO': 20,
              'DEBUG': 10,
              }
LOG_LEVEL = LOG_LEVELS['INFO']
