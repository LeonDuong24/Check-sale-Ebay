import logging
import traceback
import logging.handlers
import datetime
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
def config_log():
    log_file= f'log/app.log'
    log_level = logging.ERROR 
    logging.basicConfig(filename=log_file,level=log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    logger:logging
    logger = logging.getLogger('my_logger')
    logger.addHandler(file_handler)
    return logger
