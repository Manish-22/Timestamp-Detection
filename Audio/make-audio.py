import os as os
from pydub import AudioSegment
import sys

def MakeAudio(FileName):

    CommandVidToMP3 = "ffmpeg -i SampleVideo/" + FileName + ".mp4" + " SampleAudio/" + FileName + ".mp3"
    CommandMP3ToWav = "ffmpeg -i SampleAudio/" + FileName + ".mp3" + " SampleAudio/" + FileName + ".wav"

    os.system(CommandVidToMP3)
    os.system(CommandMP3ToWav)

def NormalizeAudio(FileName):

    RawAudio = AudioSegment.from_wav("SampleAudio/" + FileName + ".wav")
    
    TargetdBFS = -20
    Change = TargetdBFS - RawAudio.dBFS
    NormalizedAudio = RawAudio.apply_gain(Change)

    print(RawAudio.dBFS)
    print(NormalizedAudio.dBFS)

    #NormalizedAudio.export("NormalizedAudio/" + FileName + ".wav", format = "wav")

if(len(sys.argv) > 1):
    
    FileName = sys.argv[1]
    
    MakeAudio(FileName)
    NormalizeAudio(FileName)