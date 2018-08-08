import sys
import os
import json
import mod_log
import time
from pprint import pprint

config_file = "/usr/src/app/cfg/config.json"
config_check = "/usr/src/app/log/dict_%Y%m%d-%H%M%S.json"
log_mgr = mod_log.LogManager()

class ConfigManager(object):
    def __init__(self):
        self.config = None

    def load_config(self):

        global config_file
        config_new = None
        config_old_sorted = None
        config_new_sorted = None


        log_mgr.info("Loading Config file <" + str(config_file) + ">")
        if not os.path.isfile(config_file):
            log_mgr.fatal("Config file <" + str(config_file) + "> does not exist!")
            return False

        # Open configuration JSON
        try:
            with open(config_file, 'r') as f:
                if self.config is None:
                    log_mgr.info("Config initialization")
                    self.config = json.load(f)
                    pprint(self.config)
                    self.to_json(self.config, "inner")
                    return True
                else:
                    config_new = json.load(f)

        except:
            print "Configuration load error:", sys.exc_info()[0]
            raise

        # Sort existing config and updated one
        config_old_sorted = self.ordered(self.config)
        self.to_json(config_old_sorted, "config_old_sorted")
        config_new_sorted = self.ordered(config_new)
        self.to_json(config_new_sorted, "config_new_sorted")

        # If nothing change, ok
        if (config_old_sorted == config_new_sorted):
            log_mgr.info("Config unchanged")
            return True

        # Log configuration changes
        log_mgr.info("Config update")
        self.check_diffs(config_old_sorted, config_new_sorted)
        self.config = config_new

        return True

    # Save configurtion dictionary to a new file
    def to_json(self, cfg=None, cfg_name=None):
        global config_check
        if (cfg == None):
            cfg = self.config
        if (cfg_name == None):
            cfg_name = "inner"
        config_check_f = time.strftime(config_check)
        log_mgr.info("Saving config:<" + str(cfg_name) + "> to JSON:<" + str(config_check_f) + ">")
        with open(config_check_f, 'w') as f:
            json.dumps(cfg, f)

    # Sorting configurtion dictionary elements
    # https://stackoverflow.com/questions/25851183/how-to-compare-two-json-objects-with-the-same-elements-in-a-different-order-equa
    def ordered(self, obj):
        if isinstance(obj, dict):
            return sorted((k, self.ordered(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(self.ordered(x) for x in obj)
        else:
            return obj

    # Compare old and new configuration dictionaries and log differences
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
        channels = self.config.get("channels", [])
        if (channels is None):
            log_mgr.warning("Configured channel list is empty!")
            return []
        return channels

    def get_MQTT_keys_dict(self):
        MQTT_keys = self.config.get("MQTT_keys", None)
        if (MQTT_keys is None):
            log_mgr.warning("Configured MQTT_keys list is empty!")
        return MQTT_keys