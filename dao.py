import database
import parseconfig as config

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dataset():

	try:
		connect = database.get_connection()
		query = str(config.get_property('query','article.sql'))
		rows = []
		with connect.cursor() as cursor:
			cursor.execute(query)
			rows = cursor.fetchall()
			cursor.close()
			
	except Exception as e:
		print(str(e))

	logger.info('fetching dataset..%s', (len(rows) != 0))

	return rows