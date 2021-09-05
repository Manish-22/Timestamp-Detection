from gensim.models import Word2Vec
import numpy as np
from nltk.cluster import KMeansClusterer
import nltk
import extract

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
non_empty_docs = [x for x in docs if x]
model = Word2Vec(non_empty_docs, min_count = 1,sg=1)

vec_docs = []

for doc in non_empty_docs:
	vec_docs.append(vectorizer(doc, model))

X = np.array(vec_docs)

n_clusters = 3
kclusterer = KMeansClusterer(
	n_clusters, distance=nltk.cluster.util.euclidean_distance, repeats=25)
labels = kclusterer.cluster(X, assign_clusters=True)
print(labels)

for index, sentence in enumerate(non_empty_docs):
	print(str(labels[index])+":"+str(sentence))
