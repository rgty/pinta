import configparser
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

config = configparser.ConfigParser()

try:
	config.read('config.ini')
except Exception as e:
	print(str(e))

def get_property(name,key):
	return config[name][key]