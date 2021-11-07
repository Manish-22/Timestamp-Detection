import random
import sys


def buildAdjMatrix(FileName):
    
    FileLabels = open("ChunkData/" + FileName + "/Labels.txt", "r")
    LabelsRaw = FileLabels.readlines()
    FileLabels.close()

    Labels = []

    for i in LabelsRaw:
        Temp = i.strip().split(', ')

        for j in range(0, len(Temp)):
            Temp[j] = int(Temp[j])
        
        Labels.append(Temp)

    n = len(Labels[0])

    AdjMatrix = [[0 for j in range(0, n)] for i in range(0, n)]

    for i in range(0, n):
        for j in range(0, n):
            if(i == j):
                AdjMatrix[i][j] = -1
            for k in range(j + 1, n):
                if Labels[i][j] == Labels[i][k]:
                    AdjMatrix[j][k] = AdjMatrix[j][k] + 1
                    AdjMatrix[k][j] = AdjMatrix[k][j] + 1

    for i in AdjMatrix:
        for j in i:
            print(j, end=" " )
        print("\n\n")

if(len(sys.argv) > 1):
    
    FileName = sys.argv[1]
    
    buildAdjMatrix(FileName)