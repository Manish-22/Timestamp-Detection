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

def vectorizer(sentence,m):
	vec=[]
	num_w = 0
	for word in sentence:
		try:
			if num_w == 0:
				vec = m.wv[word]
			else:
				vec = np.add(vec,m[word])
			num_w+=1
		except:
			pass
	
	return np.asarray(vec)/num_w 

if os.path.isfile("eng.txt"):
    os.remove("eng.txt")
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
#file=open("eng.txt", "a")

docs=[]
no_of_images = 11
for k in range(1,no_of_images):
	if(k<10):
		imgpth = "img-000"+str(k)+".png"
	else:
		imgpth = "img-00"+str(k)+".png"
	#imgpth="test3.webp"
	# for imgpth in os.listdir("."):
	#     if imgpth.endswith(".png"):
	image = cv2.imread(imgpth)
	img =PIL.Image.open(imgpth)

	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
	_,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) 
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
	dilated = cv2.dilate(thresh,kernel,iterations = 13) 
	contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) 

	l=[]
	for contour in contours:
    		[x,y,w,h] = cv2.boundingRect(contour)

    		if h>300 and w>300:
        		continue
    		if h<40 or w<40:
        		continue
    
    		cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    		img1=img.crop((x,y,x+w,y+h))
    		l.append(pytesseract.image_to_string(img1))
	
	#if k in [2,4,5,7,9,12,14,18,24,25,27]:
		#cv2.imshow("show",image)
		#cv2.waitKey()
	
	doc_text = []
	l.reverse()
	#file.write(imgpth)
	#file.write("\n")
	for i in l:
    		doc_text.extend(clean.text_preprocessing(i))
    		#file.write(i)
	#file.close()
	docs.append(doc_text)
	print(k)

non_empty_docs = [x for x in docs if x]



model = Word2Vec(non_empty_docs,min_count = 1,sg=1)


vec_docs = []

for doc in non_empty_docs:
	vec_docs.append(vectorizer(doc,model))


X = np.array(vec_docs)
#X = np.transpose(X)

wcss = []

for i in range(1,4):
	kmeans = KMeans(n_clusters = i,init = 'k-means++',random_state = 42)
	kmeans.fit(X)
	wcss.append(kmeans.inertia_)

plt.plot(range(1,4),wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()


n_clusters = 3
clf = KMeans(n_clusters=n_clusters,max_iter=100,init='k-means++',n_init=1)
labels = clf.fit_predict(X)
print(labels)

for index,sentence in enumerate(non_empty_docs):
	print(str(labels[index])+":"+str(sentence))



#for doc in docs:
	#print(doc)
#cv2.imshow("show",image)
#cv2.waitKey()