import speech_recognition as sr
import math
import sys

def AudioToText():
    
    r = sr.Recognizer()

    FileChunkNames = open("ChunkData/" + FileName + "/NewChunkNames.txt", "r")
    ChunkNamesRaw = FileChunkNames.readlines()
    ChunkNames = []
    FileChunkNames.close()
    
    for i in ChunkNamesRaw:
        temp = ""
        for j in i:
            if(j != "\n"):
                temp = temp + j
        
        ChunkNames.append(temp)

    FileChunkText = open("ChunkData/" + FileName + "/text.txt", "w")

    for i in ChunkNames:
        print("Processing", i)
        with sr.AudioFile("AudioChunks/" + FileName + "/" + i) as Source:
            try:
                FileChunkText.write(i + "\n")
                AudioData = r.record(Source)
                Text = r.recognize_google(AudioData)
                print("\n" + Text + "\n")
                FileChunkText.write(Text + "\n")
            except:
                FileChunkText.write("\n")
                continue
    
    FileChunkText.close()

def TextSplitter():

    IndexPoints = []

    i = input("Enter number of index points - ")
    i = int(i)

    while(i > 0):

        Temp = input("Enter min:sec - ")

        Min = 0
        Sec = 0
        Time = 0
        Flag = 0

        for j in Temp:
            
            if(Flag == 0):
                if(j != ":"):
                    Min = Min * 10 + int(j)
                else:
                    Flag = 1
            else:
                Sec = Sec * 10 + int(j)
        
        Flag = 0

        if(Sec >= 60):
            print("Invalid index point, enter again")
        else:
            Time = Min * 60 + Sec
            IndexPoints.append(float(Time))
            i = i - 1
    
    print("\n")

    FileDuration = open("ChunkData/" + FileName + "/NewDuration.txt", "r")
    #FileDuration = open("ChunkData/" + FileName + "/Duration.txt", "r")
    #FileSpeechText = open("ChunkData/" + FileName + "/text.txt", "r")

    DurationRaw = FileDuration.readlines()
    #SpeechTextRaw = FileSpeechText.readlines()

    FileDuration.close()
    #FileSpeechText.close()

    Duration = []
    #SpeechText = []
    
    for i in DurationRaw:
        
        temp = ""
        
        for j in i:
            if(j != "\n"):
                temp = temp + j
        
        Duration.append(float(temp))

    """for i in range(0, len(SpeechTextRaw)):
        
        temp = ""
        
        if(i%2 == 0):
            continue
        
        for j in SpeechTextRaw[i]:
            if(j != "\n"):
                temp = temp + j
        
        SpeechText.append(temp)"""
    
    #IndexedText = []

    IndexPoints.append(float(sum(Duration)))

    for i in range(0, len(IndexPoints)):
        for j in range(0, i):
            IndexPoints[i] = IndexPoints[i] - IndexPoints[j]

    CumulativeTime(Duration)

    for i in range(0, len(IndexPoints)):
        
        Time = IndexPoints[i]
        temp = ""
        
        if(i == 0):
            j = 0

        while(j < len(Duration)):
        
            if(Duration[j] <= Time):
                
                #if(temp == ""):
                #    temp = SpeechText[j]
                #else:
                #    temp = temp + "|||||||||" + SpeechText[j]
                
                Time = Time - Duration[j]
                j = j + 1
            
            else:

                print("Error in index point",i,"=",Time)
                
                if(i != len(IndexPoints) - 1):
                    print("Adding error to next index point\n")
                    IndexPoints[i + 1] = IndexPoints[i + 1] + Time
                
                #IndexedText.append(temp)
                break
    
    #for i in IndexedText:
    #    print(i, "\n\n\n\n")

def CumulativeTime(Duration):

    res = []

    for i in range(0, len(Duration)):
        if(i != len(Duration) - 1):
            Duration[i + 1] = Duration[i] + Duration[i + 1]
    
    for i in range(0, len(Duration)):
        res.append(str(math.floor(Duration[i]//60)) + ":" + str(math.floor(Duration[i]%60)))
    
    for i in res:
        print(i)

if(len(sys.argv) > 1):
    
    FileName = sys.argv[1]

    AudioToText()
    #TextSplitter()