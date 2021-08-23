import os as os
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence
import scipy.io.wavfile as wav
import speech_recognition as sr
import math

#TestA

#Defining the name of the file to be processed
FileName = "yttest1"

def CheckDirectories():

    ChunkPath = "B:/PESU Labs/Mini Project/build2/AudioChunks"
    SampleVideoPath = "B:/PESU Labs/Mini Project/build2/SampleVideo"
    SampleAudioPath = "B:/PESU Labs/Mini Project/build2/SampleAudio"
    NormalizedAudioPath = "B:/PESU Labs/Mini Project/build2/NormalizedAudio"
    ChunkDataPath = "B:/PESU Labs/Mini Project/build2/ChunkData"
    
    if os.path.exists(ChunkPath):
        print("Folder containing audio chunks exists")
    else:
        print("Creating folder for audio chunks")
        os.mkdir(ChunkPath)

    if os.path.exists(SampleVideoPath):
        print("Folder containing sample video exists")
    else:
        print("Creating folder for sample video")
        os.mkdir(SampleVideoPath)

    if os.path.exists(SampleAudioPath):
        print("Folder containing sample audio exists")
    else:
        print("Creating folder for sample audio")
        os.mkdir(SampleAudioPath)

    if os.path.exists(NormalizedAudioPath):
        print("Folder containing normalized audio exists")
    else:
        print("Creating folder for normalized audio")
        os.mkdir(NormalizedAudioPath)
    
    if os.path.exists(ChunkDataPath):
        print("Folder containing chunk data exists")
    else:
        print("Creating folder for chunk data")
        os.mkdir(ChunkDataPath)

def MakeAudio(FileName):

    print("Converting video(mp4) to audio(wav)")

    CommandVidToMP3 = "ffmpeg -i SampleVideo/" + FileName + ".mp4" + " SampleAudio/" + FileName + ".mp3"
    CommandMP3ToWav = "ffmpeg -i SampleAudio/" + FileName + ".mp3" + " SampleAudio/" + FileName + ".wav"

    os.system(CommandVidToMP3)
    os.system(CommandMP3ToWav)

def NormalizeAudio(FileName):

    print("Normalizing sample audio")

    RawAudio = AudioSegment.from_wav("SampleAudio/" + FileName + ".wav")
    NormalizedAudio = effects.normalize(RawAudio)
    NormalizedAudio.export("NormalizedAudio/" + FileName + ".wav", format = "wav")

def MakeChunks(FileName):

    print("Creating audio chunks from normalized audio")

    NormalizedAudio = AudioSegment.from_wav("NormalizedAudio/" + FileName + ".wav")

    (source_rate, source_sig) = wav.read("NormalizedAudio/" + FileName + ".wav")
    Duration = len(source_sig) / float(source_rate)
    MaxChunks = Duration / 8
    
    ChunkDataPath = "B:/PESU Labs/Mini Project/build2/ChunkData/" + FileName

    if os.path.exists(ChunkDataPath):
        print("Folder containing chunk data for ", FileName, "exists")
    else:
        print("Creating folder for chunk data of", FileName)
        os.mkdir(ChunkDataPath)
    
    File = open("ChunkData/" + FileName + "/ChunkNames.txt", "a")

    SilenceLength = 425
    SilenceThreshold = -43

    while(True):
        
        print("Splitting using silence length =", SilenceLength, "silence threshold =", SilenceThreshold)
        
        Chunks = split_on_silence(NormalizedAudio, min_silence_len = SilenceLength , silence_thresh = SilenceThreshold, keep_silence = True)

        if(len(Chunks) > MaxChunks):
            
            if(len(Chunks) > 3 * MaxChunks):
                SilenceThreshold = SilenceThreshold - 1
            elif(len(Chunks) > 2.5 * MaxChunks):
                SilenceLength = SilenceLength + 125
            elif(len(Chunks) > 2 * MaxChunks):
                SilenceLength = SilenceLength + 75
            elif(len(Chunks) > 1.5 * MaxChunks):
                SilenceLength = SilenceLength + 50
            else:
                SilenceLength = SilenceLength + 25
            
            print("Number of chunks =", len(Chunks),"Max chunks =", MaxChunks)
        
        else:
            
            print("Number of chunks =", len(Chunks),"Within max chunk limit, exporting chunks")
            ChunkPath = "B:/PESU Labs/Mini Project/build2/AudioChunks/" + FileName

            if os.path.exists(ChunkPath):
                print("Folder containing audio chunks for ", FileName, " exists")
            else:
                print("Creating folder for audio chunks of ", FileName)
                os.mkdir(ChunkPath)

            j = 0
            for i, Chunk in enumerate(Chunks):
                ChunkName = "chunk{0}.wav".format(i)
                
                if(j == 0):
                    File.write(ChunkName)
                    j = 1
                else:
                    File.write("\n" + ChunkName)
                
                print("Creating chunk ", i)
                Chunk.export(ChunkPath + "/" + ChunkName, format="wav")
            
            break

def ChunkDetails(FileName):

    print("Finding chunk lengths and number of chunks")
    
    ChunkPath = "B:/PESU Labs/Mini Project/build2/AudioChunks/" + FileName

    NumberOFChunks = len([f for f in os.listdir(ChunkPath)if os.path.isfile(os.path.join(ChunkPath, f))])

    File = open("ChunkData/" + FileName + "/Duration.txt", "a")

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

def ChunkRemake(FileName):

    print("Finding small chunks and merging them")

    MinChunkLen = 10
    FileChunkNames = open("ChunkData/" + FileName + "/ChunkNames.txt", "r")
    FileDuration = open("ChunkData/" + FileName + "/Duration.txt", "r")

    ChunkPath = "B:/PESU Labs/Mini Project/build2/AudioChunks/" + FileName
    NumberOFChunks = len([f for f in os.listdir(ChunkPath)if os.path.isfile(os.path.join(ChunkPath, f))])

    ChunkNamesRaw = FileChunkNames.readlines()
    DurationRaw = FileDuration.readlines()

    ChunkNames = []
    Duration = []

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

    i = 0

    while(i < NumberOFChunks):
        
        if(Duration[i] < MinChunkLen):
            
            if(i == 0):
                
                MergeChunk(FileName, ChunkNames[i], ChunkNames[i + 1])
                Duration[i] = Duration[i] + Duration[i + 1]
                Duration.pop(i + 1)
                ChunkNames.pop(i + 1)
                NumberOFChunks = NumberOFChunks - 1

            elif(i + 1 == NumberOFChunks):
                
                MergeChunk(FileName, ChunkNames[i - 1], ChunkNames[i])
                Duration[i - 1] = Duration[i - 1] + Duration[i]
                Duration.pop(i)
                ChunkNames.pop(i)
                NumberOFChunks = NumberOFChunks - 1
        
            else:

                if(Duration[i + 1] > Duration[i - 1]):
                    
                    MergeChunk(FileName, ChunkNames[i], ChunkNames[i + 1])
                    Duration[i] = Duration[i] + Duration[i + 1]
                    Duration.pop(i + 1)
                    ChunkNames.pop(i + 1)
                    NumberOFChunks = NumberOFChunks - 1
                
                else:
                    
                    MergeChunk(FileName, ChunkNames[i - 1], ChunkNames[i])
                    Duration[i - 1] = Duration[i - 1] + Duration[i]
                    Duration.pop(i)
                    ChunkNames.pop(i)
                    NumberOFChunks = NumberOFChunks - 1
        else:
            i = i + 1
    
    FileChunkNames.close()
    FileDuration.close()

    FileNewChunkNames = open("ChunkData/" + FileName + "/NewChunkNames.txt", "a")
    FileNewDuration = open("ChunkData/" + FileName + "/NewDuration.txt", "a")

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

def MergeChunk(FileName, Chunk1, Chunk2):
    
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

def AudioToText(FileName):

    print("Converting audio to text")
    
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

    FileChunkText = open("ChunkData/" + FileName + "/text.txt", "a")

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

def TextSplitter(FileName):

    print("Splitting text based on index points")

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

def Testing(FileName):

    MakeAudio(FileName)
    NormalizeAudio(FileName)
    MakeChunks(FileName)
    ChunkDetails(FileName)
    ChunkRemake(FileName)
    AudioToText(FileName)

#Testing(FileName)
#AudioToText(FileName)
TextSplitter(FileName)