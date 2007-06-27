###############################################################################
#
#  VideoLogTool (c) ULP Multimedia 2007
#  Developper: Francois Schnell  (AT ulpmultimedia.u-strasbg.fr)
#
# A command-line tool to automatically detect changes of a video input and take
# screenshots (plus a generate a timecode file)
#
#
# Requires VideoCapture module(Windows):http://videocapture.sourceforge.net/
###############################################################################

import time,os,sys,fnmatch
from optparse import OptionParser
from VideoCapture import Device

        
def compareImages(img1,img2, pixLimit=100, imgLimit=200,step=4):
    """
    Compare two images  for a posible change with the following parameters:
    - pixLimit: a pixel is considered changed above this value
    - imgLimit: the minimal number of pixels which have to change to
                     consider that the picture is changed   
    For information in a 768*576 picture there is 442368 pixels
    - step: test a pixel each 'step' pixels (default=1)
            Expl: if step=4, test pixels 0,4,8,12,etc...
    """
    img1 = img1.getdata()
    img2 = img2.getdata()
    totalPixels= len(img1)
    pixdiff = 0
    step=4 # test a pixel at each step (step=2 => check pix 0,2,4...)
    for i in range(totalPixels/step):
        if abs(sum(img1[i*step]) - sum(img2[i*step])) > pixLimit:
            pixdiff += 1
            if pixdiff > imgLimit:
                return True

if __name__=="__main__":
    
    ## Global variables
    videoInput=0
    diaId=0
    tempo=1 # at which interval to check for changes (seconds)
    path=r"C:\Documents and Settings\franz\Bureau\test" # the path where to put the data (timecode + screenshots folder)
    #path=""
    pixLimit=100 #a pixel is considered changed above this value (RGB sum)
    imgLimit=200 # number of pixels wich have to change to have a postive test 
    step=4 # test a pixel each 'step' pixels (default=1)
    monitoring=True
    
    ## Read command line arguments
    print "Launching videoLog tool...\n"
    parser=OptionParser()
    parser.add_option("-v", "--videoinput",dest="videoInput",
    help="Give here the video input to use (default 0)")
    parser.add_option("-p", "--path",dest="path",
    help="Path to data folder inside double quotes.")
    parser.add_option("-x", "--pixLimit",dest="pixLimit",
    help="Differential value above which a pixel is considered changed (default=100).")
    parser.add_option("-i", "--imgLimit",dest="imgLimit",
    help="An image is considered changed above imgLimit pixels(default=200).")
    parser.add_option("-t", "--tempo",dest="tempo",
    help="Make an image comparison each tempo seconds (default=1).")
    parser.add_option("-s", "--step",dest="step",
    help="Check a pixel each 'step' pixels: If step=2 check for pixels 0,2,4,etc.")
    parser.add_option("-m", "--monitoring",dest="monitoring",
    help="Monitoring option: a monitoring.jpg image is saved each second (True or False).")
    (options,args)=parser.parse_args()
    if options.path!=None: 
        path=options.path
    if options.videoInput!=None:
        videoInput=int(options.videoInput)
    print "Using videoInput= ",str(videoInput)
    if options.tempo!=None:
        tempo=int(options.tempo)
    print "Using tempo= ",str(tempo)
    if options.step!=None:
        step=int(options.step)
    print "Using step= ",str(step)
    if options.pixLimit!=None:
        pixLimit=int(options.pixLimit)
    print "Using pixLimit= ",str(pixLimit)
    if options.imgLimit!=None:
        imgLimit=int(options.imgLimit)
    print "Using imgLimit= ",str(imgLimit)    
    if options.monitoring=="True":
        monitoring=True
    elif options.monitoring=="False":
        monitoring=False
    print "Using monitoring= ", str(monitoring) 
    
    
    ## Define the working directory and create a screenshots directory
    if path=="":
        path=os.getcwd()
        print "Using path= ",path
    try:os.mkdir(path+"/screenshots")
    except: pass

    print "Beginning VideoLog..."
    
    ## Open video input and take a first screenshot
    cam = Device(videoInput)
    oldImage=cam.getImage()
    ## Open a timecode file
    #timecode=open(path+"/timecode.csv","a")
    t0=time.time()
    
    print "Comparing images... ",
    while 1:
        time.sleep(tempo)
        print "*",
        newImage=cam.getImage()
        if compareImages(oldImage,newImage,imgLimit,pixLimit,step=1) or diaId==0:
            print " Screenshot "+str(diaId)+" "
            oldImage=newImage
            diaId += 1
            t=time.time()
            newImage.save(path+"/screenshots/" + 'D'+ str(diaId)+'.jpg')
            timeStamp = str(round((t-t0),2))
            timecode=open(path+"/timecode.csv","a")
            timecode.write(timeStamp+"\n")
            timecode.close()
        if monitoring==True:
            cam.getImage().save("monitoring.jpg")

    timecode.close()
    print "End of program"



