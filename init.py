#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
from pprint import pprint
from collections import defaultdict
import spacy, os

documents = ["Human machine interface for lab abc computer applications",
"A survey of user opinion of computer system response time",
"The EPS user interface management system",
"System and human system engineering testing of EPS",
"Relation of user perceived response time to error measurement",
"The generation of random binary unordered trees",
"The intersection graph of paths in trees",
"Graph minors IV Widths of trees and well quasi ordering",
"Graph minors A survey"]

nlp = spacy.load('en')

texts = [[word.lemma_ for word in nlp(document.lower()) if not word.is_stop] for document in documents]

frequency = defaultdict(int)

for text in texts:
  for token in text:
    frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

dictionary = corpora.Dictionary(texts)

dictionary.save('deerwester.dict')

corpus = [dictionary.doc2bow(text) for text in texts]

corpora.MmCorpus.serialize('deerwester.mm', corpus)

if (os.path.exists('deerwester.dict')):

  dictionary = corpora.Dictionary.load('deerwester.dict')
  corpus = corpora.MmCorpus('deerwester.mm')

  tfidf = models.TfidfModel(corpus)
  corpus_tfidf = tfidf[corpus]

  lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
  corpus_lsi = lsi[corpus_tfidf]

  index = similarities.MatrixSimilarity(lsi[corpus])
  index.save('deerwester.index')

  if (os.path.exists('deerwester.index')):
    index = similarities.MatrixSimilarity.load('deerwester.index')

    doc = "Human computer interaction"
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[vec_bow]

    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print('**************************************************')
    print(doc)
    print('**************************************************')
    for i, val in sims:
      print(documents[i])
