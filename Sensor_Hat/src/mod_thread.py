import threading
import time
import mod_log
import mod_measure_list
import mod_sense_hat

# Threads management class
class ThreadManager(object):

    def __init__(self, log_mgr, channel, delay, source, measure_list):
        self.log_mgr = log_mgr              # Logger module
        self.channel = channel              # Canale di acquisizione
        self.delay = delay                  # Tempo di acquisizione in ms.
        self.source = source                # Modalita' di acquisizione
        self.measure_list = measure_list    # Riferimento alla lista misure
        self.exit_flag = False              # Flag per la terminazione del thread

        self.log_mgr.info(self.__class__.__name__, "Initialized for channel <" + str(self.channel) + ">")

    # Start acquisition thread
    def start_acquisition(self):
        self.acq_thread = threading.Thread(target = self.acquisition_thread)
        self.acq_thread.start()

    # Acquisition thread definition
    def acquisition_thread(self):
        self.log_mgr.info(self.__class__.__name__, "Started for channel <" + str(self.channel) + ">")

        while (self.exit_flag == False):

            # Get timestamp
            ts = time.time()

            # Add to measure list
            self.measure_list.add_details(self.channel, self.source.read_channel(), ts)

            time.sleep(self.delay)

    # Stop acquisition thread
    def stop_acquisition (self):
        self.log_mgr.info(self.__class__.__name__, "Stopped for channel <" + str(self.channel) + ">")
        self.exit_flag = True

    def stopped_acquisition(self):
        return not(self.acq_thread.isAlive)

    def get_channel(self):
        return self.channel

    # # Thread per il processamento delle misure
    # def parse_measures(self, exit_flag, measure_list):

    #     while self.counter:

    #         # Se ho premuto il pulsante, esco e visualizzo
    #         # il segno verde
    #         if (self.exit_flag == 1):
    #             counter = 0

    #         # Genero le medie per le grandezze rilevate
    #         for ch in channels:
    #             meas = self.measure_list.avg_by_channel(ch)

    #             # Stampo il valore della media
    #             print("TS:<" + str(meas.timestamp) + ">; NUM:<" + str(meas.count)+ ">; AVG:<" + str(meas.value)+ ">")

    #             # Aggiorno il codice canale e aggiungo la media alla lista misure
    #             meas.channel = meas.channel + 10
    #             self.measure_list.add_measure(meas)

    #             # Per la temperatura, coloro il display in funzione della media rilevata
    #             if (meas.channel == 11):
    #                 self.show_temperature(meas.value)

    #         # Genero il JSON
    #         main_dic = {}
    #         main_dic[mkc.key_timestamp] = time.time()
    #         main_dic[mkc.key_qos] = "good"
    #         main_dic[mkc.key_values] = self.measure_list.json_dictionary()

    #         self.measure_list.clear_list()

    #         print("")
    #         print("************************")
    #         print(str(json.dumps(main_dic,
    #                   indent=4, sort_keys=True,
    #                   separators=(',', ': '), ensure_ascii=False)))

    #         time.sleep(self.delay)

    #         counter -= 1
