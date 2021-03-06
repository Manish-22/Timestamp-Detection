from gensim.models import Word2Vec
import numpy as np
import extract
from nltk.util import ngrams
from os import listdir


def cos_sim_word(x, y):
    X_set = set(x)
    Y_set = set(y)
    l1 = []
    l2 = []
    rvector = X_set.union(Y_set)
    for w in rvector:
        if (w in X_set):
            l1.append(1)
        else:
            l1.append(0)
        if (w in Y_set):
            l2.append(1)
        else:
            l2.append(0)
        c = 0
    for i in range(len(rvector)):
        c += l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine


def cosine_sim(vA, vB):
    # print(vA.shape,vB.shape)
    return np.dot(vA, vB) / (np.sqrt(np.dot(vA, vA)) * np.sqrt(np.dot(vB, vB)))


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
    # print(list_of_ngrams[1])
    vec = []
    num_w = 0
    for Ngram in list_of_ngrams:
        first = 1
        ng_avg = []
        for word in Ngram:
            if first == 1:
                ng_avg = m.wv[word]
            else:
                np.add(ng_avg, m.wv[word])
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
non_empty_docs = [x for x in docs if x]
model = Word2Vec(non_empty_docs, min_count=1, sg=1)

ng_docs = [list(ngrams(x, 3)) for x in non_empty_docs]

vecs = []

# print(vectorizer_ngram(ng_docs[0],model))
for doc in ng_docs:
    vecs.append(vectorizer_ngram(doc, model))

#print("Shape of vec_ng[0] ",vecs[0])

left_sim = []
right_sim = []
l_sim_w = []
r_sim_w = []

l1 = 0
r1 = len(vecs)

no_of_images = len(listdir('Images'))
group_size = no_of_images/3

for i in range(len(vecs)):
    l_vec_sum1 = 0
    r_vec_sum1 = 0
    l_vec_sum2 = 0
    r_vec_sum2 = 0

    if(i-group_size <= 1):
        l1 = 0
    else:
        l1 = i-group_size

    if(i+group_size > (len(vecs)-1)):
        r1 = len(vecs)-1
    else:
        r1 = i+group_size

    for j in range(i, int(l1)-1, -1):
        if(np.asarray(vecs[i]).shape == np.asarray(vecs[j]).shape):
            l_vec_sum1 += cosine_sim(np.asarray(vecs[i]), np.asarray(vecs[j]))
        l_vec_sum2 += cos_sim_word(non_empty_docs[i], non_empty_docs[j])
    for k in range(i+1, int(r1)+1):
        if(np.asarray(vecs[i]).shape == np.asarray(vecs[k]).shape):
            r_vec_sum1 += cosine_sim(np.asarray(vecs[i]), np.asarray(vecs[k]))
        r_vec_sum2 += cos_sim_word(non_empty_docs[i], non_empty_docs[k])

    left_sim.append(l_vec_sum1/group_size)
    l_sim_w.append(l_vec_sum2/group_size)

    right_sim.append(r_vec_sum1/group_size)
    r_sim_w.append(r_vec_sum2/group_size)

topic_changes_V = []
topic_changes_W = []

for i in range(len(vecs)):
    if(right_sim[i] > left_sim[i]):
        topic_changes_V.append(1)
    else:
        topic_changes_V.append(0)

    if(r_sim_w[i] > l_sim_w[i]):
        topic_changes_W.append(1)
    else:
        topic_changes_W.append(0)

print("Vector based topic changes")
print(topic_changes_V)
for i in range(len(vecs)):
    print(topic_changes_V[i], non_empty_docs[i], sep=':')

print("\nWord based topic changes")
print(topic_changes_W)
for i in range(len(vecs)):
    print(topic_changes_W[i], non_empty_docs[i], sep=':')
