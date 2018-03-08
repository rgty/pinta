import os
from gensim import similarities

if (os.path.exists('deerwester.index'):
  index = similarities.MatrixSimilarity.load('deerwester.index')
  
