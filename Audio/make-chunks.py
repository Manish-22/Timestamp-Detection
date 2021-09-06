import os as os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import scipy.io.wavfile as wav
import sys
from pathlib import Path
import math
import itertools
import shutil

def MakeIndex():
    
    ChunkDataPath = path + "/ChunkData/" + FileName

    print(ChunkDataPath)

    if os.path.exists(ChunkDataPath) == False:
        os.mkdir(ChunkDataPath)

    FileIndexRaw = open("ChunkData/" + FileName + "/IndexRaw.txt", "w").close()

    CommandGenIndex = "ffmpeg -i " +  "SampleVideo/" + FileName + ".mp4" + " -vf " + "select='gte(scene,0.05)',metadata=print:file=ChunkData/" + FileName + "/IndexRaw.txt" + " -an -f null -"
    
    os.system(CommandGenIndex)

    FileIndexRaw = open("ChunkData/" + FileName + "/IndexRaw.txt", "r")
    FileIndex = open("ChunkData/" + FileName + "/Index.txt", "w")

    Corpus = [i[32:] if(i[32].isdigit()) else i[33:] for i in list(itertools.islice(FileIndexRaw, 0, None, 2))]

    for i in Corpus:
        FileIndex.write("%s" % i)

def MakeChunks():

    NormalizedAudio = AudioSegment.from_wav("NormalizedAudio/" + FileName + ".wav")
    
    File = open("ChunkData/" + FileName + "/ChunkNames.txt", "w")

    SilenceLength = 625
    SilenceThreshold = -46
        
    ChunkPath = path + "/AudioChunks/" + FileName

    if os.path.exists(ChunkPath) == False:
        os.mkdir(ChunkPath)
    else:
        shutil.rmtree(ChunkPath)
        os.mkdir(ChunkPath)

    Chunks = split_on_silence(NormalizedAudio, min_silence_len = SilenceLength , silence_thresh = SilenceThreshold, keep_silence = True)

    j = 0
    for i, Chunk in enumerate(Chunks):
        ChunkName = "chunk{0}.wav".format(i)
                
        if(j == 0):
            File.write(ChunkName)
            j = 1
        else:
            File.write("\n" + ChunkName)
                
        Chunk.export(ChunkPath + "/" + ChunkName, format="wav")
    
    File.close()

def ChunkDetails():

    ChunkPath = path + "\AudioChunks\\" + FileName

    NumberOFChunks = len([f for f in os.listdir(ChunkPath)if os.path.isfile(os.path.join(ChunkPath, f))])

    File = open("ChunkData/" + FileName + "/Duration.txt", "w")

    ChunkNames = []

    for i in range(0, NumberOFChunks):
        ChunkNames.append("chunk{0}.wav".format(i))

    for i in range(0, NumberOFChunks):
        (source_rate, source_sig) = wav.read("AudioChunks/" + FileName + "/" + ChunkNames[i])
        Duration = len(source_sig) / float(source_rate)
        if(i == 0):
            File.write(str(Duration))
        else:
            File.write("\n" + str(Duration))
    
    File.close()

def ChunkRemake():

    MinChunkLen = 10
    Error = 0.25

    FileChunkNames = open("ChunkData/" + FileName + "/ChunkNames.txt", "r")
    FileDuration = open("ChunkData/" + FileName + "/Duration.txt", "r")
    FileIndexPoints = open("ChunkData/" + FileName + "/Index.txt", "r")

    ChunkPath = path + "\AudioChunks\\" + FileName
    NumberOFChunks = len([f for f in os.listdir(ChunkPath)if os.path.isfile(os.path.join(ChunkPath, f))])

    ChunkNamesRaw = FileChunkNames.readlines()
    DurationRaw = FileDuration.readlines()
    IndexPointsRaw = FileIndexPoints.readlines()
    
    FileChunkNames.close()
    FileDuration.close()
    FileIndexPoints.close()

    ChunkNames = []
    Duration = []
    IndexPoints = []

    for i in ChunkNamesRaw:
        temp = ""
        for j in i:
            if(j != "\n"):
                temp = temp + j
        
        ChunkNames.append(temp)
    
    for i in DurationRaw:
        temp = ""
        for j in i:
            if(j != "\n"):
                temp = temp + j
        
        Duration.append(float(temp))
    
    for i in IndexPointsRaw:
        temp = ""
        for j in i:
            if(j != "\n"):
                temp = temp + j
        
        IndexPoints.append(float(temp))

    i = 0
    j = 0
    Time = 0

    while(i < NumberOFChunks and j < len(IndexPoints)):
        
        Time = Time + Duration[i]
        
        if(Time + Error < IndexPoints[j]):
            i = i + 1
        elif((Time + Error > IndexPoints[j]) and (Time - Error < IndexPoints[j])):
            j = j + 1
            i = i + 1
        else:
            Chunk = AudioSegment.from_wav("AudioChunks/" + FileName + "/" + ChunkNames[i])
            
            CutPoint1 = int(truncate(IndexPoints[j] - Time + Duration[i], 3) * 1000)
            CutPoint2 = int(truncate(Time - IndexPoints[j], 3) * 1000)
            
            FirstChunk = Chunk[:CutPoint1]
            SecondChunk = Chunk[-CutPoint2:]
            
            if os.path.exists("AudioChunks/" + FileName + "/" + ChunkNames[i]):
                os.remove("AudioChunks/" + FileName + "/" + ChunkNames[i])
            
            FirstChunk.export("AudioChunks/" + FileName + "/" + ChunkNames[i], format = "wav")

            NewChunkName = "Chunk" + str(NumberOFChunks) + ".wav"
        
            SecondChunk.export("AudioChunks/" + FileName + "/" + NewChunkName, format = "wav")

            ChunkNames.insert(i + 1, NewChunkName)
    
            Duration.insert(i + 1, CutPoint2/1000)
            Duration[i] = CutPoint1/1000
            
            Time = Time - Duration[i + 1]

            i = i + 1
            j = j + 1
            NumberOFChunks = NumberOFChunks + 1
    
    i = 0
    j = 0
    Time = 0
    Flag = False

    while(i < NumberOFChunks):

        Time = Time + Duration[i]

        if(j < len(IndexPoints)):
            
            if((Time + Error > IndexPoints[j]) and (Time - Error < IndexPoints[j])):
            
                j = j + 1

                if((Duration[i] < MinChunkLen) and (i != 0)):
                    MergeChunk(ChunkNames[i - 1], ChunkNames[i])
                    Duration[i - 1] = Duration[i - 1] + Duration[i]
                    Duration.pop(i)
                    ChunkNames.pop(i)
                    NumberOFChunks = NumberOFChunks - 1
                    Flag = True
                    continue
                else:
                    i = i + 1
                    Flag = True
                    Time = Time + Duration[i]

                Flag = True

        if(Duration[i] < MinChunkLen):
            
            if(i == 0):
                
                if(Flag == False):
                    MergeChunk(ChunkNames[i], ChunkNames[i + 1])
                    Time = Time - Duration[i]
                    Duration[i] = Duration[i] + Duration[i + 1]
                    Duration.pop(i + 1)
                    ChunkNames.pop(i + 1)
                    NumberOFChunks = NumberOFChunks - 1

            elif(i + 1 == NumberOFChunks):

                if(Flag == False):
                
                    MergeChunk(ChunkNames[i - 1], ChunkNames[i])
                    Duration[i - 1] = Duration[i - 1] + Duration[i]
                    Duration.pop(i)
                    ChunkNames.pop(i)
                    NumberOFChunks = NumberOFChunks - 1
                else:
                    i = i + 1
        
            else:

                if((Duration[i - 1] > Duration[i + 1]) and (Flag == False)):
                    
                    MergeChunk(ChunkNames[i - 1], ChunkNames[i])
                    Duration[i - 1] = Duration[i - 1] + Duration[i]
                    Duration.pop(i)
                    ChunkNames.pop(i)
                    NumberOFChunks = NumberOFChunks - 1
                
                else:
                    
                    MergeChunk(ChunkNames[i], ChunkNames[i + 1])
                    Time = Time - Duration[i]
                    Duration[i] = Duration[i] + Duration[i + 1]
                    Duration.pop(i + 1)
                    ChunkNames.pop(i + 1)
                    NumberOFChunks = NumberOFChunks - 1

        else:

            i = i + 1
            Flag = False

    FileNewChunkNames = open("ChunkData/" + FileName + "/NewChunkNames.txt", "w")
    FileNewDuration = open("ChunkData/" + FileName + "/NewDuration.txt", "w")

    for i in range(0, len(ChunkNames)):
        if(i == 0):
            FileNewChunkNames.write(ChunkNames[i])
        else:
            FileNewChunkNames.write("\n" + ChunkNames[i])
    
    for i in range(0, len(Duration)):
        if(i == 0):
            FileNewDuration.write(str(Duration[i]))
        else:
            FileNewDuration.write("\n" + str(Duration[i]))
    
    FileNewChunkNames.close()
    FileNewDuration.close()

def MergeChunk(Chunk1, Chunk2):
    
    Chunk1Path = "AudioChunks/" + FileName + "/" + Chunk1
    Chunk2Path = "AudioChunks/" + FileName + "/" + Chunk2
    ExportPath = Chunk1Path

    Sound1 = AudioSegment.from_wav(Chunk1Path)
    Sound2 = AudioSegment.from_wav(Chunk2Path)

    MergedSound = Sound1 + Sound2

    if os.path.exists(Chunk1Path):
        os.remove(Chunk1Path)

    if os.path.exists(Chunk2Path):
        os.remove(Chunk2Path)
        
    MergedSound.export(ExportPath, format="wav")

path = str(Path(__file__).parent.resolve())

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

if(len(sys.argv) > 1):
    
    FileName = sys.argv[1]
    #MakeIndex()
    MakeChunks()
    ChunkDetails()
    ChunkRemake()