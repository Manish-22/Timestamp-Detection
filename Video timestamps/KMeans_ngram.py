from gensim.models import Word2Vec
import numpy as np
from nltk.cluster import KMeansClusterer
import nltk
from nltk import ngrams
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


def vectorizer_ngram(list_of_ngrams, m):
    vec = []
    num_w = 0
    for Ngram in list_of_ngrams:
        first = 1
        ng_avg = []
        for word in Ngram:
            if first == 1:
                ng_avg = m.wv[word]
            else:
                np.add(ng_avg,m.wv[word])
                first = 0
	
        ng_avg = np.asarray(ng_avg)/len(Ngram)
        #ng_avg = sum([m.wv[word] for word in Ngram])/len(Ngram)
        if num_w == 0:
            vec = ng_avg
        else:
            vec = np.add(vec, ng_avg)
        num_w += 1

    return np.asarray(vec)/num_w


docs = extract.extraction()
transpoints = transpoint()

non_empty_docs = [x for x in docs if x]
model = Word2Vec(non_empty_docs, min_count=1, sg=1)

vec_docs = []

ng_docs = [ngrams(x, 3) for x in non_empty_docs]

for doc in ng_docs:
    vec_docs.append(vectorizer_ngram(doc, model))


X = np.array(vec_docs)

n_clusters = 3
kclusterer = KMeansClusterer(
    n_clusters, distance=nltk.cluster.util.euclidean_distance, repeats=25, avoid_empty_clusters=True)
labels = kclusterer.cluster(X, assign_clusters=True)
print(labels)

for i, sentence in enumerate(docs):
	if sentence in non_empty_docs:
		print(transpoints[i].strip('\n')+':', i+1, ":", str(sentence), sep=' ')
