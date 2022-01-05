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

    nRows = len(Labels)
    nCols = len(Labels[0])

    AdjMatrix = [[0 for j in range(0, nCols)] for i in range(0, nCols)]

    for i in range(0, nRows):
        for j in range(0, nCols):
            if Labels[i][j] == 0:
                continue
            for k in range(j + 1, nCols):
                if Labels[i][j] == Labels[i][k]:
                    AdjMatrix[j][k] = AdjMatrix[j][k] + 1
                    AdjMatrix[k][j] = AdjMatrix[k][j] + 1
    
    for i in range(0, nCols):
        AdjMatrix[i][i] = -1

    for i in AdjMatrix:
        for j in i:
            print(j, end=" " )
        print("\n\n")

if(len(sys.argv) > 1):
    
    FileName = sys.argv[1]
    
    buildAdjMatrix(FileName)