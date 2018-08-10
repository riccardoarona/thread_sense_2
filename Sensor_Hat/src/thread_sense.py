# coding=utf-8
import json
import mod_config
import mod_log
import mod_exit
import mod_measure_list
import mod_thread
import mod_sense_hat
import mod_average

thread_list = []

class MainClass(object):
    def __init__(self):

        self.log_mgr = mod_log.LogManager()
        self.cfg_mgr = cfg_mgr

        self.channel_list = []
        self.log_mgr.info(self.__class__.__name__, "initialization")

        self.cfg_mgr.load_config()
        self.channel_list = self.cfg_mgr.get_channel_list()

        self.thread_timeout = int(self.cfg_mgr.get_exit_params()[0].get("thread_timeout_ms", 10000)) / 1000
        self.thread_stop_timeout = int(self.cfg_mgr.get_exit_params()[0].get("thread_stop_timeout_ms", 10000)) / 1000


    def setup_threads(self):

        global thread_list
        global measure_list

        source = None
        thd_mgr = None

        self.log_mgr.info(self.__class__.__name__, "startup")

        for ch in self.channel_list:

            # Istanzio l'oggetto che gestisce il canale di acquisizione (fisico o calcolato)
            self.log_mgr.info(self.__class__.__name__, "Source definition: <" + str(ch.get("channel")) + ">; <" + str(ch.get("channel")) + ">")
            if (ch.get("type") == "analogue"):
                source = mod_sense_hat.SenseManager(ch.get("channel"))
            if (ch.get("type") == "average"):
                source = mod_average.AverageManager(measure_list, ch.get("channel"), ch.get("source_channel"))

            # Istanzio il thread, fornendogli il riferimento del canale di acquisizione
            samp_time = int(ch.get("samp_time_ms")) / 1000
            self.log_mgr.info(self.__class__.__name__, "Thread start: <" + str(ch.get("id")) + ">")
            thd_mgr = mod_thread.ThreadManager(ch.get("channel"), samp_time, source, measure_list)
            thread_list.append(thd_mgr)

    def start_threads(self):
        # Start threads
        for th in thread_list:
            th.start()
            th.join()
            th.start_acquisition()

        # Instantiate and activate the exit manager
        self.exit_mgr = mod_exit.ExitManager(self.thread_timeout, self.thread_stop_timeout, thread_list)
        self.exit_mgr.start()
        self.exit_mgr.join()
        self.exit_mgr.start_exit_mgr()

# Leggo la configurazione
cfg_mgr = mod_config.ConfigManager()

# Istanzio la lista misure
measure_list = mod_measure_list.MeasureList()

# sns_mgr.show_green_sign()
print("Termine programma")
