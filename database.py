import pymysql
import parseconfig as config
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_connection():
	try:
		connect = None

		db_host = config.get_property('db', 'host')
		db_user = config.get_property('db', 'user')
		db_pass = config.get_property('db', 'pass')
		db_name = config.get_property('db', 'name')

		logger.debug('db_host - %s', db_host)
		logger.debug('db_name - %s', db_name)
		
		connect = pymysql.connect(host=db_host, user=db_user, 
			password=db_pass, db=db_name, charset='utf8mb4', 
			cursorclass=pymysql.cursors.DictCursor)

	except Exception as e:
		print(str(e))

	logger.info('database connection..%s', (connect is not None))

	return connect