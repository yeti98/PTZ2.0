import json

from src.TrackingModel import TrackingModel

CONFIG_FILE_PATH = '../config/config.json'


def read_config(path):
    with open(CONFIG_FILE_PATH, 'r') as handle:
        cfg = json.load(handle)
    handle.close()
    return cfg


cfg = read_config(CONFIG_FILE_PATH)
tracking_agent = TrackingModel(cfg)
tracking_agent.track()
