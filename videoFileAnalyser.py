###############################################################################
#
#  videoFileAnalyser (c) Univesity of Strasbourg
#  Developper: F. Schnell
#
#  A command-line tool to automatically extract images from a video file (mp4), 
#  comparing them to keep significant ones
#  
###############################################################################


import subprocess, os
import ImageChops, Image
import math

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

if 1:
    print "> extracting images from video..."
    p= subprocess.Popen(["ffmpeg","-i","enregistrement-video.mp4","-r","0.1","-f","image2","tests/%05d.jpg"])
    p.communicate() #waiting for ffmpeg to finish before continuing script

if 0: # Test
    print "> comparing pictures..."
    im1=Image.open("tests/1.jpg")
    im2=Image.open("tests/7.jpg")
    print rmsdiff(im1,im2)
    
if 1:
    print "to do :"
    print "begin with first picture and make a copy D1.jpg"
    print "go through pic, if rms difference > threshold create n.jpg"
    print "remove others pics when finished"
    
    for fileName in (os.listdir("tests")):
        if fileName != "00001.jpg":
            print fileName
            #currentRms =
            