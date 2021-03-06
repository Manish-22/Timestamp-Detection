from gensim.models import Word2Vec
import numpy as np
from nltk.cluster import KMeansClusterer
from nltk.cluster.util import euclidean_distance
import sys
import random

def KMeans(FileName):

    FileCleanText = open("ChunkData/" + FileName + "/CleanedText.txt", "r")
    
    CleanTextRaw = FileCleanText.readlines()

    FileCleanText.close()

    CleanText = []

    for i in CleanTextRaw:
        Temp = i.strip()
        Temp = Temp.split(', ')
        CleanText.append(Temp)

    FileChunkDuration = open("ChunkData/" + FileName + "/NewDuration.txt", "r")

    ChunkDurationRaw = FileChunkDuration.readlines()

    FileChunkDuration.close()
 
    ChunkDuration = []

    for i in ChunkDurationRaw:
        Temp = ""
        for j in i:
            if(j != "\n"):
                Temp = Temp + j

        ChunkDuration.append(float(Temp))

    for i in range(0, len(CleanText)):
        for j in range(0, len(CleanText[i])):
            if(CleanText[i][j] == ''):
                CleanText[i].remove(CleanText[i][j])
                break
    
    i = 0

    while i < len(CleanText):
        if(len(CleanText[i]) == 0):
            if(i < len(CleanText) - 1):
                CleanText.pop(i)
                ChunkDuration[i + 1] = ChunkDuration[i] + ChunkDuration[i + 1]
                ChunkDuration.pop(i)
            else:
                CleanText.pop(i)
                ChunkDuration[i - 1] = ChunkDuration[i] + ChunkDuration[i - 1]
                ChunkDuration.pop(i)
        i = i + 1
    
    NumClusters = int(sum(ChunkDuration) // 240) + 1

    Model = Word2Vec(CleanText, min_count = 1, sg = 1)

    VectorizedText = []

    for i in CleanText:
        VectorizedText.append(Vectorizer(i, Model))
    
    VectorizedText = np.array(VectorizedText)

    FileLabels = open("ChunkData/" + FileName + "/Labels.txt", "w")

    for i in range(0, 50):

        InitialCentroids = RandomizeCentroids(ChunkDuration, VectorizedText)
        KClusterer = KMeansClusterer(NumClusters, initial_means = InitialCentroids ,distance = euclidean_distance, avoid_empty_clusters = True)

        Labels = KClusterer.cluster(VectorizedText, assign_clusters=True)
        for j in range(0, len(Labels)):
            if(j != len(Labels) - 1):
                FileLabels.write(str(Labels[j]) + ", ")
            elif(i != 50):
                FileLabels.write(str(Labels[j]) + "\n")
            else:
                FileLabels.write(str(Labels[j]))

    FileLabels.close()

def RandomizeCentroids(ChunkDuration, Text):

    CumulativeDuration = 0
    IndexPool = []
    Centroids = []

    for i in range(0, len(ChunkDuration)):
        if(CumulativeDuration + ChunkDuration[i] <= 240):
            CumulativeDuration = CumulativeDuration + ChunkDuration[i]
            IndexPool.append(i)
        else:
            CumulativeDuration = CumulativeDuration + ChunkDuration[i] - 240
            Centroids.append(Text[random.choice(IndexPool)])
            IndexPool = []
            IndexPool.append(i)
    
    Centroids.append(Text[random.choice(IndexPool)])

    return Centroids


def printTransitionPoints(ChunkDuration, Labels):
    
    TransitionPoints = []

    Temp = 0
    for i in ChunkDuration:
        Temp = Temp + i
        TransitionPoints.append(ToTime(Temp))

    Prev = None 

    for i in range(0, len(Labels)):
        if(Prev is None):
            Prev = Labels[i]
        else:
            if(Prev != Labels[i]):
                Prev = Labels[i]
                print(TransitionPoints[i])

def ToTime(x):

    if(len(str(int(x % 60))) == 0):
        Sec = ":00"
    elif(len(str(int(x % 60))) == 1):
        Sec = ":0" + str(int(x % 60))
    else:
        Sec = ":" + str(int(x % 60))
    
    return str(int(x // 60)) + Sec

def Vectorizer(Sentence, Model):
	
    Vector = []
    n = 0
	
    for i in Sentence:
        if n == 0:
            Vector = Model.wv[i]
        else:
            Vector = np.add(Vector, Model.wv[i])
        n += 1

    return np.asarray(Vector)/n

if(len(sys.argv) > 1):
    
    FileName = sys.argv[1]

    KMeans(FileName)