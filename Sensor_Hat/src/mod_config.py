import sys
import os
import json
import mod_log

config_file = '/usr/src/app/cfg/config.json'
dict_old = '/usr/src/app/log/dict_old.json'
dict_new = '/usr/src/app/log/dict_new.json'
log_mgr = mod_log.LogManager()

class ConfigManager(object):
    def __init__(self):
        self.config = []
        pass

    def load_config(self):
        global config_file
        log_mgr.info("Loading Config file <" + str(config_file) + ">")
        if not os.path.isfile(config_file):
            log_mgr.fatal("Config file <" + str(config_file) + "> does not exist!")
            return False

        # Apro la lista dei parametri di configurazione
        try:
            with open(config_file, 'r') as f:
                if self.config is None:
                    log_mgr.info("Config initialization")
                    self.config = self.ordered(json.load(f))
                    json.dumps(self.config, )
                    return True

                config_new = self.ordered(json.load(f))

        except:
            print "Configuration load error:", sys.exc_info()[0]
            raise

        if (self.config == config_new):
            log_mgr.info("Config unchanged")
            return True
        
        log_mgr.info("Config update")
        self.check_diffs(self.config, config_new)
        self.config = config_new

        return True

    # Stampa gli elementi della lista
    def print_config(self):
        for item in self.config:
            lvINDEX=0
            for params in self.config[item]:
                for key, value in params.iteritems():
                    print item +'/'+str(lvINDEX)+'/'+key, value
                lvINDEX+=1

    # Ordinamento degli elementi della lista
    def ordered(self, obj):
        if isinstance(obj, dict):
            log_mgr.info("Sorting - found dict")
            return sorted((k, self.ordered(v)) for k, v in obj.items())
        if isinstance(obj, list):
            log_mgr.info("Sorting - found list")
            return sorted(self.ordered(x) for x in obj)
        else:
            return obj

    # Confronto dei valori della configurazione nuova con quella vecchia
    def check_diffs(self, old, new):
        diff = False
        for old_key in old:
            if old_key not in new:
                diff = True
                log_mgr.warning("key:<%s> missing" %old_key)
            elif old[old_key] != new[old_key]:
                diff = True
                log_mgr.warning("key:<" + old_key + "> value updated: old:<" + old[old_key] + ">; new:<" + new[old_key] + ">")
        return diff

    def get_channel_list(self):
        return self.config.get('channels', {})

    def get_MQTT_keys_dict(self):
        return self.config.get('MQTT_keys', {})