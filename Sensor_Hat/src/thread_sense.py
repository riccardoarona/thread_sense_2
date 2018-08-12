# coding=utf-8
import json
import mod_config
import mod_log
import mod_exit
import mod_measure_list
import mod_thread
import mod_sense_hat
import mod_average

class MainClass(object):
    def __init__(self):
        self.thread_list = []
        self.channel_list = []

        # Istanzio il log manager
        self.log_mgr = mod_log.LogManager()
        self.log_mgr.info(self.__class__.__name__, "Initialization")

        # Istanzio la lista misure
        self.measure_list = mod_measure_list.MeasureList()

        # Leggo la configurazione
        self.cfg_mgr = mod_config.ConfigManager()
        self.cfg_mgr.load_config()
        self.channel_list = self.cfg_mgr.get_channel_list()

        self.thread_timeout = int(self.cfg_mgr.get_exit_params()[0].get("thread_timeout_ms", 10000)) / 1000
        self.thread_stop_timeout = int(self.cfg_mgr.get_exit_params()[0].get("thread_stop_timeout_ms", 10000)) / 1000
        self.log_mgr.info(self.__class__.__name__, "Thread params - thread_timeout:<" + str(self.thread_timeout) + ">; thread_stop_timeout:<" + str(self.thread_stop_timeout) + ">")


    def setup_threads(self):

        source = None
        thd_mgr = None

        self.log_mgr.info(self.__class__.__name__, "Startup")

        for ch in self.channel_list:

            # Istanzio l'oggetto che gestisce il canale di acquisizione (fisico o calcolato)
            self.log_mgr.info(self.__class__.__name__, "Source definition - ID:<" + str(ch.get("id")) + ">; channel:<" + str(ch.get("channel")) + ">; source_channel:<" + str(ch.get("source_channel")) + ">")
            if (ch.get("type") == "analogue"):
                source = mod_sense_hat.SenseManager(int(ch.get("channel")))
            if (ch.get("type") == "average"):
                source = mod_average.AverageManager(self.measure_list, int(ch.get("channel")), int(ch.get("source_channel")))

            # Istanzio il thread, fornendogli il riferimento del canale di acquisizione
            samp_time = int(ch.get("samp_time_ms")) / 1000
            self.log_mgr.info(self.__class__.__name__, "Thread start - ID:<" + str(ch.get("id")) + ">")
            thd_mgr = mod_thread.ThreadManager(int(ch.get("channel")), samp_time, source, self.measure_list)
            self.thread_list.append(thd_mgr)

    def start_threads(self):

        self.log_mgr.info(self.__class__.__name__, "Starting threads")

        # Start threads
        for th in self.thread_list:
            th.start()
            th.join()
            th.start_acquisition()

        self.log_mgr.info(self.__class__.__name__, "Starting exit mgr")

        # Instantiate and activate the exit manager
        self.exit_mgr = mod_exit.ExitManager(self.thread_timeout, self.thread_stop_timeout, self.thread_list)
        self.exit_mgr.start()
        self.exit_mgr.join()
        self.exit_mgr.start_exit_mgr()

main = MainClass()
main.setup_threads
main.start_threads

# sns_mgr.show_green_sign()
print("Termine programma")
