from gensim import corpora, models, similarities
import os
from pprint import pprint

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
    pprint(sims)
    
  
  
