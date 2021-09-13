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
        ng_avg = sum([m.wv[word] for word in Ngram])/len(Ngram)
        if num_w == 0:
            vec = ng_avg
        else:
            vec = np.add(vec, ng_avg)
        num_w += 1

    return np.asarray(vec)/num_w


docs = extract.extraction()
transpoints = transpoint()

docs_index = {}
for i in range(len(docs)):
    docs_index[i] = docs[i]

res = dict((frozenset(v), k+1) for k, v in docs_index.items())

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

for i, sentence in enumerate(non_empty_docs):
    print(transpoints[i].strip('\n')+':',
          res[frozenset(sentence)], ":", str(sentence), sep=' ')
