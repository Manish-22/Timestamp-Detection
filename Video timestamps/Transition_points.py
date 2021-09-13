import os
import subprocess
name,coeff= input("Enter the video name and the selection coefficient:").split()
mydir = os.path.join(os.getcwd(),'Images')
for f in os.listdir(mydir):
    os.remove(os.path.join(mydir, f))
flag=input("Do you want to blur the video(yes or no)")
try:
    os.remove('transitionpoints.txt')
except:
    pass
if flag=='yes':
    subprocess.call(
        f'ffmpeg -i Videos/{name}.mp4 -filter_complex "[0:v]crop=130:110:500:250,boxblur=27[b0];[0:v]crop=130:110:500:0,boxblur=27[b1]; [0:v][b0]overlay=500:250[ovr0];[ovr0][b1]overlay=500:0[v]" -map "[v]" Videos/{name}-blurred.mp4', shell=True)
    subprocess.call(f'ffmpeg -i "Videos/{name}-blurred.mp4" -vsync 0 -vf select=\'gt(scene\,{coeff})\' -f image2 "Images/img-%04d.png',shell=True)
    subprocess.call(f'ffmpeg -i "Videos/{name}-blurred.mp4"  -vf "select=\'gt(scene\,{coeff})\',metadata=print:file=transitionpoints.txt" -an -f null -',shell=True)
else:
    subprocess.call(
        f'ffmpeg -i "Videos/{name}.mp4" -vsync 0 -vf select=\'gt(scene\,{coeff})\' -f image2 "Images/img-%04d.png', shell=True)
    subprocess.call(
        f'ffmpeg -i "Videos/{name}.mp4" -vf "select=\'gt(scene\,{coeff})\',metadata=print:file=transitionpoints.txt" -an -f null -', shell=True)

