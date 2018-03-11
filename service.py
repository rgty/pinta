import dao, json, re, spacy, os
import pandas as pd
from gensim import corpora, models, similarities
# from sklearn.feature_extraction.text import TfidfVectorizer


def fetch_and_parse():
	return lemmatize(clean(dao.get_dataset()))

def clean(d_set):
	parsed_dict = {}
	
	for row in d_set:
		_id, _text = None, None
		for k in row:
			if k == 'article_id':
				_id = row[k]
			elif k == 'full_article_json':
				row_json = json.loads(row[k])
				if len(row_json['article_body']) == 1:
					_text = row_json['article_body'][0]['article_desc']
				else:
					break
		if _text:
			parsed_dict[_id] = re.sub('[\:\n\r\t\.</>;]+','', _text)

	return parsed_dict

def lemmatize(d_set):
	
	nlp = spacy.load('en')
	
	n_set = []
	
	for key in d_set:
		_value = ' '.join(word.lemma_ for word in nlp(d_set[key].lower()) 
			if not (word.is_punct or word.is_stop or word.is_space))
		n_set.append({'_id':key, '_text':_value})
	
	df = pd.DataFrame(n_set)
	df.to_csv('clean_dataset.csv')

	df['_text'] = df['_text'].str.replace('*.(news)$', '', inplace=True, regex=True)
	df.to_csv('clean_datasets.csv')

	return d_set

def compute_similarity():
	
	dictionary, dict_file = None, 'dictionary.dict'
	corpus, corpus_file = None, 'corpus.mm'
	index, index_file = None, 'matrix_similarity.index'
	documents, texts, recommends = [], [], []

	doc_frame = pd.read_csv('clean_dataset.csv')
	doc_frame = doc_frame.dropna(subset=['_id','_text'], axis=0, how='any')
	doc_frame_list = doc_frame.reset_index(drop=True).values.tolist()

	for i in range(len(doc_frame_list)):
		documents.append(doc_frame_list[i][2])

	text_frame = pd.read_csv('clean_datasets.csv')
	text_frame = text_frame.dropna(subset=['_id','_text'], axis=0, how='any')
	text_frame['_text'] = text_frame['_text'].str.split()
	text_frame_list = text_frame.reset_index(drop=True).values.tolist()

	for i in range(len(text_frame_list)):
		texts.append(text_frame_list[i][3])

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

	lsi = models.LsiModel(c_tfidf, id2word=dictionary, num_topics=25)
	c_lsi = lsi[c_tfidf]

	if not os.path.exists(index_file):
		index = similarities.MatrixSimilarity(lsi[corpus])
		index.save(index_file)
	else:
		index = similarities.MatrixSimilarity.load(index_file)


	for i in range(len(documents)):
		vec_doc = dictionary.doc2bow(documents[i].split())
		lsi_doc = lsi[vec_doc]

		sims = index[lsi_doc]
		sims = sorted(enumerate(sims), key=lambda item: -item[1])
		sims = sims[1:6]

		recommends.append([sims])
		recommends.append([documents[i]])
		for k, v in sims:
			recommends.append(['\n'])
			recommends.append([documents[k]])
			recommends.append([texts[k]])
		break

	df = pd.DataFrame(recommends)
	df.to_csv('1_recommend.csv')

def train_model():
	if not os.path.exists('clean_datasets.csv'):
		fetch_and_parse()
	compute_similarity()

if __name__== '__main__':
	train_model()

