import sys
import logging

log_path = '/usr/src/app/log/main_log.log'

class LogManager(object):

    def __init__(self):
        global log_path
        self.log = logging.getLogger(__name__)

        try:

            self.log.setLevel(logging.INFO)

            # create a file handler
            handler = logging.FileHandler(log_path)
            handler.setLevel(logging.INFO)

            # create a logging format
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            # add the handlers to the log
            self.log.addHandler(handler)

        except:
            print "Log set-up error:", sys.exc_info()[0]
            raise

    # Aggiunge alla lista una misura dati i valori
    def info(self, caller, message):
        self.log.info(caller + " - "  + message)

    # Aggiunge alla lista una misura dati i valori
    def fatal(self, caller, message):
        self.log.fatal(caller + " - "  + message)

    # Aggiunge alla lista una misura dati i valori
    def warning(self, caller, message):
        self.log.warning(caller + " - "  + message)