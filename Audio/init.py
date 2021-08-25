import os as os
from pathlib import Path

def MakeDirectories():

    path = str(Path(__file__).parent.resolve())

    ChunkPath = path + "/AudioChunks"
    SampleVideoPath = path + "/SampleVideo"
    SampleAudioPath = path + "/SampleAudio"
    NormalizedAudioPath = path + "/NormalizedAudio"
    ChunkDataPath = path + "/ChunkData"
    
    if os.path.exists(ChunkPath) == False:
        os.mkdir(ChunkPath)

    if os.path.exists(SampleVideoPath) == False:
        os.mkdir(SampleVideoPath)

    if os.path.exists(SampleAudioPath) == False:
        os.mkdir(SampleAudioPath)

    if os.path.exists(NormalizedAudioPath) == False:
        os.mkdir(NormalizedAudioPath)
    
    if os.path.exists(ChunkDataPath) == False:
        os.mkdir(ChunkDataPath)

MakeDirectories()