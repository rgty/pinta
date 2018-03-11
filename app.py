from flask import Flask, request, jsonify
import service

app = Flask(__name__)

@app.route('/recommend/article', methods=['POST'])
def handle_recommend():
	req_data = request.get_json(force=True)
	resp_data = service.get_similar_articles(req_data.get('_id'))
	return jsonify(resp_data)

app.run()