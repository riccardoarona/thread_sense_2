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
        self.cfg_mgr = mod_config.ConfigManager(self.log_mgr)
        self.cfg_mgr.load_config()
        self.channel_list = self.cfg_mgr.get_channel_list()

        self.thread_timeout = float(self.cfg_mgr.get_exit_params()[0].get("thread_timeout_ms", 10000)) / 1000
        self.thread_stop_timeout = float(self.cfg_mgr.get_exit_params()[0].get("thread_stop_timeout_ms", 10000)) / 1000
        self.log_mgr.info(self.__class__.__name__, \
                        "Thread params - thread_timeout:<" + str(self.thread_timeout) + ">; " + \
                        "thread_stop_timeout:<" + str(self.thread_stop_timeout) + ">")


    def setup_threads(self):

        source = None
        thd_mgr = None

        self.log_mgr.info(self.__class__.__name__, "Setting-up threads")

        for ch in self.channel_list:

            thread_id = ch.get("id")
            channel_nr = int(ch.get("channel"))
            source_channel_nr = int(ch.get("source_channel"))
            samp_time = float(ch.get("samp_time_ms")) / 1000

            self.log_mgr.info(self.__class__.__name__, \
                              "Source definition - ID:<" + thread_id + ">; " + \
                              "samp_time:<" + str(samp_time) + ">; " + \
                              "channel:<" + str(channel_nr) + ">; " + \
                              "source_channel:<" + str(source_channel_nr) + ">")

            # Create an instance of the acquisition manager
            if (ch.get("type") == "analogue"):
                source = mod_sense_hat.SenseManager(self.log_mgr, int(channel_nr))
            if (ch.get("type") == "average"):
                source = mod_average.AverageManager(self.log_mgr, self.measure_list, channel_nr, source_channel_nr)

            # Create an instance of the acquisition management thread
            thd_mgr = mod_thread.ThreadManager(self.log_mgr, channel_nr, samp_time, source, self.measure_list)
            self.thread_list.append(thd_mgr)

    def start_threads(self):

        # Logging existing threads
        for th in self.thread_list:
            self.log_mgr.info(self.__class__.__name__, "Listing channel:<" + str(th.get_channel()) + ">")

        # Start threads
        for th in self.thread_list:
            self.log_mgr.info(self.__class__.__name__, "Activating channel:<" + str(th.get_channel()) + ">")
            th.start_acquisition
            th.start()

        self.log_mgr.info(self.__class__.__name__, "Starting exit mgr")

        # Instantiate and activate the exit manager
        self.exit_mgr = mod_exit.ExitManager(self.log_mgr, self.thread_timeout, self.thread_stop_timeout, self.thread_list)
        self.exit_mgr.start_exit_mgr()
        self.exit_mgr.start()

        # Wait for exit manager to complete its job
        self.exit_mgr.join()

main = MainClass()
main.setup_threads()
main.start_threads()

# sns_mgr.show_green_sign()
print("Termine programma")
