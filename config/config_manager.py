import configparser
import os

config_file = 'config.ini'

def save_config(selected_image_path):
    config = configparser.ConfigParser()
    config['SETTINGS'] = {'background_image': selected_image_path}
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
        return config.get('SETTINGS', 'background_image', fallback=None)
    return None