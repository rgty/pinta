import configparser

config = configparser.ConfigParser()

try:
	config.read('config.ini')
except Exception as e:
	print(str(e))

def get_property(name,key):
	return config[name][key]