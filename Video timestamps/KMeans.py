from gensim.models import Word2Vec
import numpy as np
from nltk.cluster import KMeansClusterer
import nltk
import extract
from filter_time import transpoint

def vectorizer(sentence, m):
	vec = []
	num_w = 0
	for word in sentence:
		if num_w == 0:
				vec = m.wv[word]
		else:
			vec = np.add(vec, m.wv[word])
		num_w += 1

	return np.asarray(vec)/num_w

docs=extract.extraction()
transpoints=transpoint()

non_empty_docs = [x for x in docs if x]
model = Word2Vec(non_empty_docs, min_count = 1,sg=1)

vec_docs = []

for doc in non_empty_docs:
	vec_docs.append(vectorizer(doc, model))

X = np.array(vec_docs)

n_clusters = 3
kclusterer = KMeansClusterer(
	n_clusters, distance=nltk.cluster.util.euclidean_distance, repeats=25,avoid_empty_clusters=True)
labels = kclusterer.cluster(X, assign_clusters=True)
print(labels)

for i,sentence in enumerate(docs):
	if sentence in non_empty_docs:
		print(transpoints[i].strip('\n')+':',i+1,":",str(sentence),sep=' ')
