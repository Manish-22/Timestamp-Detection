import os as os
import sys

try:
    Start = int(sys.argv[1])
    End = int(sys.argv[2])
    File = sys.argv[3]
except:
    print("python run-all.py <Starting video number> <Ending video number> <File to run>")

if(File == "make-audio"):
    Command = "python make-audio.py"
elif(File == "make-chunks"):
    Command = "python make-chunks.py"
elif(File == "audio-to-text"):
    Command = "python audio-to-text.py"
elif(File == "clean-text"):
    Command = "python clean-text.py"
elif(File == "K-means"):
    Command = "python K-means.py"
elif(File != "all"):
    exit()

if(File == "all"):
    
    Command = "python make-audio.py"
    for i in range(Start, End + 1):
        os.system(Command + " video" + str(i))
    
    Command = "python make-chunks.py"
    for i in range(Start, End + 1):
        os.system(Command + " video" + str(i))
    
    Command = "python audio-to-text.py"
    for i in range(Start, End + 1):
        os.system(Command + " video" + str(i))
    
    Command = "python clean-text.py"
    for i in range(Start, End + 1):
        os.system(Command + " video" + str(i))
    
    Command = "python K-means.py"
    for i in range(Start, End + 1):
        os.system(Command + " video" + str(i))
        
else:
    
    for i in range(Start, End + 1):
        os.system(Command + " video" + str(i))