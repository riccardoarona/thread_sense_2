import threading
import time
import mod_log
import mod_sense_hat
import mod_thread
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

sense = None

# Threads management class
class ExitManager(threading.Thread):

    def __init__(self, delay, close_timeout, thread_list):
        global sense
        threading.Thread.__init__(self)
        self.thread_list = thread_list      # Data acquisition thread list
        self.close_timeout = close_timeout  # Timeout for threads closeup
        self.delay = delay                  # Tempo di acquisizione in ms.
        self.exit_flag = False              # Threads termination flag
        sense = SenseHat()

        self.log_mgr = mod_log.LogManager()
        self.log_mgr.info(self.__class__.__name__, "initialized")

    # Sensors reading thread
    def start_exit_mgr(self):
        self.log_mgr.info(self.__class__.__name__, "started")

        while (self.exit_flag == False):

            # Add to measure list
            self.exit_flag = self.pushed_middle

            time.sleep(self.delay)

        self.stop_acquisition()

    def stop_acquisition (self):
        self.log_mgr.info(self.__class__.__name__, "stopping threads")

        for th in self.thread_list:
            th.stop_acquisition()
            while (th.stopped_acquisition & self.close_timeout <= 10):
                c_timeout = self.close_timeout - 1
                time.sleep(1)

# ------------------------------------------------------------------------------------------------
#  METODI DEDICATI PER IL SENSE-HAT
# ------------------------------------------------------------------------------------------------

    # Alla pressione del pulsante del sense-hat il programma termina
    def pushed_middle(self, event):
        if event.action == ACTION_PRESSED:
            self.log_mgr.info(self.__class__.__name__, "Exit button pressed")
            self.exit_flag = True