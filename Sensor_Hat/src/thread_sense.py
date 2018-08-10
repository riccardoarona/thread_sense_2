# coding=utf-8
import json
import mod_config
import mod_log
import mod_measure_list
import mod_thread
import mod_sense_hat
import mod_average

thread_list = []

class MainClass(object):
    def __init__(self):

        global log_mgr
        self.cfg_mgr = cfg_mgr

        self.channel_list = []
        log_mgr.info(self.name, "initialization")

        self.cfg_mgr.load_config()
        self.channel_list = self.cfg_mgr.get_channel_list()

    def setup_threads(self):
        global log_mgr
        global thread_list
        global measure_list

        source = None
        thd_mgr = None

        log_mgr.info(self.name, "startup")

        for ch in self.channel_list:

            # Istanzio l'oggetto che gestisce il canale di acquisizione (fisico o calcolato)
            log_mgr.info(self.name, "Source definition: <" + str(ch.get("channel")) + ">; <" + str(ch.get("channel")) + ">")
            if (ch.get("type") == "analogue"):
                source = mod_sense_hat.SenseManager(ch.get("channel"))
            if (ch.get("type") == "average"):
                source = mod_average.AverageManager(measure_list, ch.get("channel"), ch.get("source_channel"))

            # Istanzio il thread, fornendogli il riferimento del canale di acquisizione
            samp_time = int(ch.get("samp_time_ms")) / 1000
            log_mgr.info(self.name, "Thread start: <" + str(ch.get("id")) + ">")
            thd_mgr = mod_thread.ThreadManager(ch.get("channel"), samp_time, source, measure_list)
            thread_list.append(thd_mgr)

    def start_threads(self):
        for th in thread_list:
            th.start()
            th.join()
            th.start_acquisition()

# Istanzio la classe del log
log_mgr = mod_log.LogManager()

# Leggo la configurazione
cfg_mgr = mod_config.ConfigManager()

# Istanzio la lista misure
measure_list = mod_measure_list.MeasureList()

# Avvio il programma
main = MainClass()
main.setup_threads()
main.start_threads()

# sns_mgr.show_green_sign()
print("Termine programma")
