# log format list
log_formats = {'f1': '%(asctime)s %(levelname)s - %(message)s',
               'f2': '%(asctime)s p%(process)s %(module)s :%(lineno)d %(levelname)s - %(message)s'
               }
log_format = log_formats['f2']
# date format
date_format = '%m/%d/%Y %I:%M:%S %p'
# log file name
file_name = './logs/main_log.log'
# log file size(in MB)
file_size = 1024
# log level
log_levels = {'CRITICAL': 50,
              'ERROR': 40,
              'WARNING': 30,
              'INFO': 20,
              'DEBUG': 10,
              }
log_level = log_levels['DEBUG']
