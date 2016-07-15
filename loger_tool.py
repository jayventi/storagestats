'''
loger_tool.py config and setup for python loger tool 
Created on Jun 23, 2016
@author: jayventi
'''

########     Loger tool    #####################
import logging
import logging.handlers

def loger_mang(log_path=None, stop_handler=None):
    # to init suplay a file path log_path which emits a log handler
    # to stop loging set stop_handler = emits log handler
    if not stop_handler:
        log_format = '%(asctime)s - %(name)s - %(funcName)s -' + \
                     '%(levelname)s - %(message)s' 
        dateformat = '%Y-%m-%d %I:%M:%S'
        logging.getLogger('').setLevel(logging.DEBUG)
        handler1 = logging.handlers.RotatingFileHandler( 
            log_path, 
            maxBytes=1000000, 
            backupCount=5)
        handler1.setFormatter(logging.Formatter(log_format, dateformat))
        logging.getLogger('').addHandler(handler1 )
    else:     
        logging.getLogger('').removeHandler(stop_handler )
        handler1 = None
    return handler1