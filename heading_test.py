import cv2
import PIL
import pytesseract
import clean
import os
import numpy as np
from gensim.models import Word2Vec
import nltk
from sklearn.cluster import KMeans
from sklearn import cluster
from sklearn import metrics
from sklearn.decomposition import PCA
from scipy.cluster import hierarchy
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'


def vectorizer(sentence, m):
    vec = []
    num_w = 0
    for word in sentence:
        try:
            if num_w == 0:
                vec = m.wv[word]
            else:
                vec = np.add(vec, m.mv[word])
            num_w += 1
        except:
            pass

    return np.asarray(vec)/num_w


l = []
no_of_images = 28
for k in range(1, no_of_images):
    if(k < 10):
        imgpth = "Videos\img-000"+str(k)+".png"
    else:
        imgpth = "Videos\img-00"+str(k)+".png"
    # imgpth="test3.webp"
    # for imgpth in os.listdir("."):
    #     if imgpth.endswith(".png"):
    image = cv2.imread(imgpth)
    img = PIL.Image.open(imgpth)
    w, h = img.size
    #points = np.array([[0,img.size[1]*0.4], [0,img.size[1]*0.3], [img.size[0],img.size[1]*0.3], [img.size[0],img.size[1]*0.4]])
    points = [
        np.array([[0, h*0.4], [0, h*0.25], [w, h*0.25], [w, h*0.4]], dtype=np.int32)]
    # cv2.drawContours(image,points,0,(0,0,0),2)

    [x, y, w, h] = cv2.boundingRect(points[0])
    img1 = img.crop((x, y, x+w, y+h))
    l.append(pytesseract.image_to_string(img1))

    #cv2.imshow('image', image)
    # cv2.waitKey()

non_empty_docs = [clean.text_preprocessing(i) for i in l]
non_empty_docs = [x for x in non_empty_docs if x]

model = Word2Vec(non_empty_docs, min_count=1, sg=1)


vec_docs = []

for doc in non_empty_docs:
    vec_docs.append(vectorizer(doc, model))


X = np.array(vec_docs)
#X = np.transpose(X)

wcss = []

for i in range(1, 4):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 4), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()


n_clusters = 3
clf = KMeans(n_clusters=n_clusters, max_iter=100, init='k-means++', n_init=1)
labels = clf.fit_predict(X)
print(labels)

for index, sentence in enumerate(non_empty_docs):
    print(str(labels[index])+":"+str(sentence))
