import pymysql
import parseconfig as config
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def get_connection():
	try:
		db_host = config.get_property('db', 'host')
		db_user = config.get_property('db', 'user')
		db_pass = config.get_property('db', 'pass')
		db_name = config.get_property('db', 'name')
		
		return pymysql.connect(host=db_host, user=db_user, 
			password=db_pass, db=db_name, charset='utf8mb4', 
			cursorclass=pymysql.cursors.DictCursor)

	except Exception as e:
		print(str(e))