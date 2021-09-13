import os as os
import sys

Start = int(sys.argv[1])
End = int(sys.argv[2])
File = sys.argv[3]

if(File == "make-audio"):
    Command = "python make-audio.py"
elif(File == "make-chunks"):
    Command = "python make-chunks.py"
elif(File == "audio-to-text"):
    Command = "python audio-to-text.py"
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

else:
    
    for i in range(Start, End + 1):
        os.system(Command + " video" + str(i))