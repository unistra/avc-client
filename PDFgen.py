#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

###############################################################################
# CreatePDF script for audiocours verion 2  
# (c) UMP Multimedia November 2006
# Programmer :  francois schnell
###############################################################################

import sys
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm, inch

class CreatePDF:
    """
    A class to create a PDF with the slides from AudioCours Version 2 recording
    
    Usage:
    
    Python CrezatePDF.py myDirectoryPath yourfilename (without the .pdf)
    """
    
    def __init__(self):
        """
        Initialize the PDF (A4) and reade the timecode file
        """
        self.pdf = Canvas(workingDirectory+"/"+pdfName+".pdf")
        timecode= open(workingDirectory+"/timecode.csv",'r')
        self.slides=[]
        for line in timecode:
            print "Found slide at t (seconds) = "+line
            self.slides.append(line)
        self.slides=self.slides[1:]#Don't use the first slide
        print "\nNumber of slides to process :", len(self.slides)
        print "\nPlease wait while processing ..."
        
    def timeToHMS(self,t):
        """ 
        Return a Hour Minute Seconds string from the time given in seconds
        """
        t=float(t)
        hours=int(t/3600)
        mins=int(t-hours*3600)/60
        seconds=int(t-hours*3600-mins*60)
        hms= str(hours)+" h "+str(mins)+" m "+str(seconds)+" s "
        return  hms
        
    def produce(self):
        """
        Draw in the PDF the screenshots and datas
        (2 screenshots per page : Up and Down)
        """
        d=1
        # Slides Positions
        SUx,SUy=3*cm,3*cm # upper slide
        SDx,SDy=3*cm,16*cm #Slide Down (bottom)
        Swidth,Sheight= 16*cm,11*cm
        
        while d <= len(self.slides):
            
            self.pdf.setFont("Courier", 10)
            #self.pdf.setStrokeColorRGB(1,1,0)
            self.pdf.setStrokeColor("grey")
            self.pdf.setLineWidth(2) 
        
            if d % 2 == 0: # Upper slide
                captureTime =self.timeToHMS(self.slides[d-1])
                self.pdf.drawString(SUx, SUy-0.5*cm, "^ Capture "+str(d)+\
                " (timing = "+ captureTime +")")
                self.pdf.drawImage(workingDirectory+"/screenshots/D"+str(d)+\
                ".jpg", SUx,SUy,width=Swidth,height=Sheight)
                self.pdf.rect(SUx,SUy,Swidth,Sheight, fill=0)
                self.pdf.showPage()
                if d==len(self.slides):
                    self.pdf.save()
                
            if d % 2 != 0: # Down slide (bottom)
                captureTime =self.timeToHMS(self.slides[d-1])
                self.pdf.drawString(SDx,SDy-cm*0.5, "^ Capture "+str(d)+\
                " (timing = "+ captureTime +")")
                self.pdf.drawImage(workingDirectory+"/screenshots/D"+str(d)+\
                ".jpg", SDx,SDy, width=Swidth,height=Sheight)
                self.pdf.rect(SDx,SDy,Swidth,Sheight, fill=0)
                if d==len(self.slides):
                    self.pdf.showPage()
                    self.pdf.save()
            d+=1
        if len (self.slides)>= 1: print "\nPDF File saved"
        if len(self.slides)<1: print "\nNo slides to process : No PDF produced"
        
if __name__ == "__main__":
    
    if sys.argv[1]!="":
        
        workingDirectory= sys.argv[1] # read the folder to use
        pdfName=sys.argv[2] # the name of the PDF file to produce
        myPDF=CreatePDF()
        myPDF.produce()
