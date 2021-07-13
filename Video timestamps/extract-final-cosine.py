import cv2
import PIL
import pytesseract
import clean
import os
from gensim.models import Word2Vec
import nltk
import numpy as np
from sklearn.cluster import KMeans
from sklearn import cluster
from sklearn import metrics
from sklearn.decomposition import PCA
from scipy.cluster import hierarchy
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt


def cos_sim_word(x, y):
    X_set = set(x)
    Y_set = set(x)
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
    return np.dot(vA, vB) / (np.sqrt(np.dot(vA, vA)) * np.sqrt(np.dot(vB, vB)))


def vectorizer(sentence, m):
    vec = []
    num_w = 0
    for word in sentence:
        try:
            if num_w == 0:
                vec = m.wv[word]
            else:
                vec = np.add(vec, m[word])
            num_w += 1
        except:
            pass

    return np.asarray(vec)/num_w


if os.path.isfile("eng.txt"):
    os.remove("eng.txt")
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
# file=open("eng.txt", "a")

docs = []
no_of_images = 11
for k in range(1, no_of_images):
    if(k < 10):
        imgpth = "img-000"+str(k)+".png"
    else:
        imgpth = "img-00"+str(k)+".png"
    # imgpth="test3.webp"
    # for imgpth in os.listdir("."):
    #     if imgpth.endswith(".png"):
    image = cv2.imread(imgpth)
    img = PIL.Image.open(imgpth)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=13)
    contours, hierarchy = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    l = []
    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)

        if h > 300 and w > 300:
            continue
        if h < 40 or w < 40:
            continue

        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        img1 = img.crop((x, y, x+w, y+h))
        l.append(pytesseract.image_to_string(img1))

    # if k in [2,4,5,7,9,12,14,18,24,25,27]:
        # cv2.imshow("show",image)
        # cv2.waitKey()

    doc_text = []
    l.reverse()
    # file.write(imgpth)
    # file.write("\n")
    for i in l:
        doc_text.extend(clean.text_preprocessing(i))
        # file.write(i)
    # file.close()
    docs.append(doc_text)
    print(k)

non_empty_docs = [x for x in docs if x]
model = Word2Vec(non_empty_docs, min_count=1, sg=1)

vecs = []

for doc in non_empty_docs:
    vecs.append(vectorizer(doc, model))

left_sim = []
right_sim = []
l_sim_w = []
r_sim_w = []

l1 = 0
r1 = len(vecs)

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
        l_vec_sum1 += cosine_sim(vecs[i], vecs[j])
        l_vec_sum2 += cos_sim_word(non_empty_docs[i], non_empty_docs[j])
    for k in range(i+1, int(r1)+1):
        r_vec_sum1 += cosine_sim(vecs[i], vecs[k])
        r_vec_sum2 += cos_sim_word(non_empty_docs[i], non_empty_docs[k])
    # if(i == 0):
        # left_sim.append(0)
        # l_sim_w.append(0)
    # else:
        # left_sim.append(l_vec_sum1/i)
        # l_sim_w.append(l_vec_sum2/i)
    # right_sim.append(r_vec_sum1/(len(vecs)-i))
    # r_sim_w.append(r_vec_sum2/(len(vecs)-i))

    left_sim.append(l_vec_sum1/group_size)
    l_sim_w.append(l_vec_sum2/group_size)

    right_sim.append(r_vec_sum1/group_size)
    r_sim_w.append(r_vec_sum2/group_size)

topic_changes_V=[]
topic_changes_W=[]

for i in range(len(vecs)):
    if(right_sim[i] > left_sim[i]):
        topic_changes_V.append(1)
    else:
        topic_changes_V.append(0)

    if(r_sim_w[i] > l_sim_w[i]):
        topic_changes_W.append(1)
    else:
        topic_changes_W.append(0)

print("Vector based topic changes\n")
for i in range(len(vecs)):
    if(topic_changes_V[i] == 1):
        print(non_empty_docs[i])

print("\nWord based topic changes\n")
for i in range(len(vecs)):
    if(topic_changes_W[i] == 1):
        print(non_empty_docs[i])


