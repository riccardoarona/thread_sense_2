import time
import mod_log
import mod_measure_list

class AverageManager(object):
    def __init__(self, measure_list, channel, source_channel):
        self.measure_list = measure_list
        self.source_channel = source_channel
        self.channel = channel
        
        self.log_mgr = mod_log.LogManager()
        self.log_mgr.info(self.name, "AverageManager initialized")

    # Acquire single measure from single channel
    def read_channel(self):
        
        # Calcolo la media
        val = self.measure_list.avg_by_channel(self.channel, self.source_channel)

        # Arrotondamento ad una cifra decimale
        val = round(val, 2)

        return val

    # For compliancy with abstract class
    def check_exit(self):
        return False