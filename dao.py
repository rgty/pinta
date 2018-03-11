import database
import parseconfig as config
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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

	return rows