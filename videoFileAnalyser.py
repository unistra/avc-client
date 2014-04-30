###############################################################################
#
#  videoFileAnalyser (c) Univesity of Strasbourg
#  Developper: F. Schnell
#
#  A script to automatically extract images from a video file (mp4), 
#  comparing them to keep significant ones
#  
###############################################################################


import subprocess, os
import ImageChops, Image
import math, shutil

# Only useful if OCRanalyse=True
# https://code.google.com/p/pytesser/
from pytesser import *  

# Variables
sizeChangeThreshold=5000   # used only in File Size change comparison method
picsExtraction = True   # extract pictures from video files
videoFilePath="enregistrement-video.mp4"   # name of the video to analyse
extractionInterval= "0.1" # 1 / time interval  : 1= each seconds, 0.1 each 10 secs...
outputPath="tests" # Output folder
cleanFiles=True # remove extacted files to only keep different ones renamed D1.jpg, D2.jpg, etc
OCRanalyse=True # perform OCR on "slides"

print "> videoFileAnalyser started..."

def rmsdiff(im1, im2):
    """Calculate the root-mean-square difference between two images
    source : http://code.activestate.com/recipes/577630-comparing-two-images/"""
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*(idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

if picsExtraction==True:
    print "> extracting images from video..."
    p= subprocess.Popen(["ffmpeg","-i",videoFilePath,"-r",extractionInterval,"-f","image2",outputPath+"/%05d.jpg"])
    p.communicate() #waiting for ffmpeg to finish before continuing script

if 0: # Test
    print "> comparing pictures..."
    im1=Image.open(outputPath+"/00001.jpg")
    im2=Image.open(outputPath+"/00001.jpg")
    print rmsdiff(im1,im2)
   
if 0: # Square root method not working well on my test samples
    print "Square root comparison method" 
    previousDiff=rmsdiff(Image.open(outputPath+"/00001.jpg"),Image.open(outputPath+"/00001.jpg"))  
    
if 1: # file size changes comparaison method (very quick)
    print "File size changes comparaison method (very quick)"
    previousFileSize=os.path.getsize(outputPath+"/00001.jpg")
    print "Selected Size Change Threshold is : "+str(sizeChangeThreshold)

previousFileName="00001.jpg"
slideIndex=1
shutil.copy2(outputPath+"/"+previousFileName,outputPath+"/D"+str(slideIndex)+".jpg")

for fileName in (os.listdir(outputPath)):
    if fileName != "00001.jpg" or fileName !="D1.jpg":
        
        if 1: # File Size comparison method
            currentFileSize=os.path.getsize(outputPath+"/"+fileName)
            diffSize=abs(currentFileSize-previousFileSize)
            print fileName +" --- "+ str(currentFileSize) + " abs diff is: "+ str(diffSize)
            if diffSize > sizeChangeThreshold: 
                slideIndex+=1
                #print ">>>>>>>>>>>>>> " + str(fileName)
                shutil.copy2(outputPath+"/"+fileName, outputPath+"/D"+str(slideIndex)+".jpg")                    
            previousFileSize=currentFileSize 
        
        if 0: # Root Mean Square comparison method (don't work well on my test sample)
            currentfileName= fileName
            diff = rmsdiff(Image.open(outputPath+"/"+previousFileName),Image.open(outputPath+"/"+currentfileName))  
            print "difference betweeen " + previousFileName+ " and "+ currentfileName+ " is "+ str(diff)
            deltaDiff=math.fabs(diff-previousDiff)
            print "diff - previousDiff", deltaDiff
            if deltaDiff > 10:
                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> New dia detected :" + currentfileName
            previousFileName=currentfileName
            previousDiff=diff
            
if cleanFiles==True:
    for fileName in (os.listdir(outputPath)):
        if "D" in fileName:
            pass
        else:
            os.remove(outputPath+"/"+fileName)

if OCRanalyse==True:
    print "> starting OCR with pytesser"
    for fileName in (os.listdir(outputPath)):
        
        if 0: # Using pytesser (2007, no french dic) https://code.google.com/p/pytesser/
            im = Image.open(outputPath+"/"+fileName)
            text = image_to_string(im)
            print "############## "+fileName+" ############"
            print text
            print "########################################"
            
        if 1: # Using tesseract-ocr-setup-3.02.02.exe on Windows
            inputFile=os.getcwd()+"/"+outputPath+"/"+fileName
            outputFile=os.getcwd()+"/"+outputPath+"/"+(fileName.split(".")[0])+".txt"
            print inputFile
            print outputFile
            app='tesseract.exe'
            appPath=os.path.join(r'C:\Program Files (x86)/Tesseract-OCR',app)
            print "appPath", appPath
            commandLine=[app, inputFile,outputFile ]
            p= subprocess.Popen([r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe', inputFile ,outputFile  ])
            p.communicate()

