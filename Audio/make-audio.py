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

    LowPassFilteredAudio = RawAudio.low_pass_filter(3000)
    HighPassFilteredAudio = LowPassFilteredAudio.high_pass_filter(300)
    
    TargetdBFS = -20
    Change = TargetdBFS - HighPassFilteredAudio.dBFS
    NormalizedAudio = HighPassFilteredAudio.apply_gain(Change)
    
    NormalizedAudio.export("NormalizedAudio/" + FileName + ".wav", format = "wav")

if(len(sys.argv) > 1):
    
    FileName = sys.argv[1]
    
    MakeAudio(FileName)
    NormalizeAudio(FileName)