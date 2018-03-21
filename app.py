from flask import Flask, request, jsonify
import service

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/v1/recommend/article', methods=['POST'])
def handle_v1():
	resp_data = {}
	try:
		req_data = request.get_json(force=True)
		resp_data = service.get_similar_articles(req_data.get('_id'))
		resp_data['status'] = 'success'
	except Exception as e:
		logging.error(str(e))
		resp_data['status'] = 'error'

	return jsonify(resp_data)


@app.route('/v2/recommend/article', methods=['POST'])
def handle_v2():
	resp_data = {}
	try:
		req_data = request.get_json(force=True)
		resp_data = service.get_similar_articles(req_data.get('_id'))
		resp_data['status'] = 'success'
	except Exception as e:
		logging.error(str(e))
		resp_data['status'] = 'error'

	return jsonify(resp_data)

@app.route('/recommend/retrain', methods=['GET'])
def handle_retrain():
	resp_data = {}
	try:	
		num_topics = request.args.get('num_topics')
		refresh, force = False, False

		if request.args.get('refresh_dataset'):
			refresh = bool(request.args.get('refresh_dataset'))

		if request.args.get('force'):
			force = bool(request.args.get('force'))

		#retrain model
		is_retrain = service.retrain_model(num_topics, refresh, force)

		resp_data['status'] = 'success' if is_retrain else 'error'
		resp_data['num_topics'] = num_topics
		resp_data['refresh_dataset'] = refresh
		resp_data['force'] = force
	
	except Exception as e:
		logging.error(str(e))
		resp_data['status'] = 'error'

	return jsonify(resp_data)

if __name__ == '__main__':
	app.run()