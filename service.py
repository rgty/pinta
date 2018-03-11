import dao, json, re, spacy, os
import pandas as pd
from gensim import corpora, models, similarities
import sys, subprocess, gc

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

actual_file = 'actual_content.csv'
clean_file = 'clean_content.csv'
recommend_file = 'recommend.p'
dict_file = 'dictionary.dict'
corpus_file = 'corpus.mm'
corpus_index_file = 'corpus.mm.index'
index_file = 'matrix_similarity.index'

def fetch_and_parse():
	return lemmatize(clean(dao.get_dataset()))

def clean(d_set):
	actual_set, parsed_dict = [], {}
	
	for row in d_set:
		_id, _text, _title = None, None, None
		for k in row:
			if k == 'article_id':
				_id = row[k]
			elif k == 'full_article_json':
				row_json = json.loads(row[k])
				if len(row_json['article_body']) == 1:
					_text = row_json['article_body'][0]['article_desc']
					_title = row_json['title']
				else:
					break
		if _text:
			actual_set.append({'_id':_id, '_text':_text, '_title':_title})
			parsed_dict[_id] = re.sub('[\:\n\r\t\.</>;]+','', _text)

		# save actual article content
		df = pd.DataFrame(actual_set)
		df.to_csv(actual_file)

	logger.info("cleansing..%s", (len(parsed_dict) != 0))

	return parsed_dict

def lemmatize(d_set):
	
	nlp = spacy.load('en')
	
	n_set = []
	
	for key in d_set:
		_value = ' '.join(word.lemma_ for word in nlp(d_set[key].lower()) 
			if not (word.is_punct or word.is_stop or word.is_space))
		n_set.append({'_id':key, '_text':_value})

	df = pd.DataFrame(n_set)
	df['_text'] = df['_text'].str.replace(r'.+(news)', '')
	df = df.dropna(subset=['_id','_text'], axis=0, how='any')
	df.to_csv(clean_file)

	logger.info("lemmatizing..%s", (len(df) != 0))

	return d_set

def compute_similarity(num_topics=50):

	logger.info("computing similarity with %s topics", num_topics)
	
	dictionary, corpus, index = None, None, None
	documents, texts, recommends, titles = [], [], [], []

	aframe = pd.read_csv(actual_file)
	aframe = aframe.dropna(subset=['_id','_text'], axis=0, how='any')
	af_list = aframe.reset_index(drop=True).values.tolist()
	
	for i in range(len(af_list)):
		documents.append(af_list[i][2])
		titles.append(af_list[i][3])

	cframe = pd.read_csv(clean_file)
	cframe = cframe.dropna(subset=['_id','_text'], axis=0, how='any')
	tf_list = cframe.reset_index(drop=True).values.tolist()
	
	for i in range(len(tf_list)):
		texts.append(tf_list[i][2].replace(r'[^\W]+', '').split())

	if not os.path.exists(dict_file):
		dictionary = corpora.Dictionary(texts)
		dictionary.save(dict_file)
	else:
		dictionary = corpora.Dictionary.load(dict_file)

	if not os.path.exists(corpus_file):
		corpus = [dictionary.doc2bow(text) for text in texts]
		corpora.MmCorpus.serialize(corpus_file, corpus)
	else:
		corpus = corpora.MmCorpus(corpus_file)

	tfidf = models.TfidfModel(corpus)
	c_tfidf = tfidf[corpus]
	
	if len(sys.argv) > 1:
		num_topics = int(sys.argv[1])
	lsi = models.LsiModel(c_tfidf, id2word=dictionary, num_topics=num_topics)
	c_lsi = lsi[c_tfidf]

	if not os.path.exists(index_file):
		index = similarities.MatrixSimilarity(lsi[corpus], num_features=int(num_topics))
		index.save(index_file)
	else:
		index = similarities.MatrixSimilarity.load(index_file)

	for i in range(len(documents)):
		doc = documents[i].lower().replace(r'.+(news)', '').split()
		vec_doc = dictionary.doc2bow(doc)
		lsi_doc = lsi[vec_doc]

		sims = index[lsi_doc]
		sims = sorted(enumerate(sims), key=lambda item: -item[1])
		sims = sims[1:6]

		r_dict, r_list = {'_source' : {'_id' : i, '_title' : titles[i]}}, []
		for k, v in sims:
			r_list.append({'_id': k, '_title': titles[k], '_score' : str(v)})
		r_dict['_target'] = r_list
		recommends.append(r_dict)

	df = pd.DataFrame(recommends)
	df.to_pickle(recommend_file)

def get_similar_articles(_id):
	
	logger.info("fetching similar articles..")

	resp_list, resp_dict = [], {}

	if not os.path.exists(recommend_file):
		train_model()
	else:
		df = pd.read_pickle(recommend_file)
		try:
			df = df.iloc[_id]
			
			_source, _target = {}, []
			_source['_id'] = df['_source']['_id']
			_source['_title'] = df['_source']['_title']
			
			for i in range(len(df['_target'])):
				_dict = {}
				_dict['_id'] = df['_target'][i]['_id']
				_dict['_title'] = df['_target'][i]['_title']
				_dict['_score'] = df['_target'][i]['_score']	
				_target.append(_dict)
			
			resp_dict['_source'] = _source
			resp_dict['_target'] = _target

		except Exception as e:
			print(str(e))

		logger.debug(str(resp_dict))
		logger.info('success' if len(resp_dict) != 0 else 'error')
	
	return resp_dict

def train_model():
	if not os.path.exists(clean_file):
		fetch_and_parse()
	compute_similarity(64)

def retrain_model(num_topics=64, refresh=False, force=False):
	if os.path.exists(recommend_file):
		bash_force = ['rm',recommend_file]
		if refresh:
			bash_force.extend([dict_file, corpus_file, corpus_index_file, index_file])
		if force:
			bash_force.extend([actual_file, clean_file])
		subprocess.call(bash_force)
	
	if force:
		fetch_and_parse()

	compute_similarity(num_topics)	

	return os.path.exists(recommend_file)

if __name__== '__main__':
	train_model()

