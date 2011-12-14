########################################################################################
#
# AudioCours Cut tool - ULP Multimedia
# Developer: francois schnell (@ulpmm.us-strasbg.fr)
#
# A small tool to cut exiting AudioCours recordings into smaller parts
# 
# Possible usages:
#    - have more than one presentations in a recording
#    - want to get rid off the begin or end of a recording
#
# You need to download first the "mp3splt.exe" free utility:
# mp3splt.sourceforge.net
#
# In the GUI, indicate the cut times and the ending time (the duration of the mp3)
# AudioCours Cut tool will create a new folder per track and will process
# the timecode, copy and rename pictures, etc.
#
########################################################################################

# Python import
import os

# External libs iimport
import wx

class mainFrame(wx.Frame):
    """
    Main GUI frame for AV cut.
    A small tool to cut exiting AudioCours recordings into smaller parts.
    Possible usages:
    - have more than one presentations in a recording
    - want to get rid off the begin or end of a recording
    Folder named "px" will be created (where x is the part number: 1,2,...)
    """
    
    def __init__(self, parent, title):
        """
        Constructor, GUI setting up.
        """
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(600, 300),
                          style=wx.DEFAULT_FRAME_STYLE)  
        # vars
        self.recordingPath=""
        self.tracks=[]
        self.timecodeAll=[]
        self.cutTimes=[]
        
        # widgets
        panel=wx.Panel(self)
        btnOriginal= wx.Button(panel, -1, "Select original folder")
        self.entryOriginal= wx.TextCtrl(panel, -1,"", size=(500,-1))
        labelCuts=wx.StaticText(panel,-1,"Enter time cues for cuts: hh:mm:ss")
        self.entryCue1=wx.TextCtrl(panel, -1,"", size=(100,-1))
        self.entryCue2=wx.TextCtrl(panel, -1,"", size=(100,-1))
        self.entryCue3=wx.TextCtrl(panel, -1,"", size=(100,-1))
        self.entryCue4=wx.TextCtrl(panel, -1,"", size=(100,-1))
        self.entryCue5=wx.TextCtrl(panel, -1,"", size=(100,-1))
        btnCut= wx.Button(panel, -1, "<<<   Cut and process!   >>>")
        
        #bindings
        self.Bind(wx.EVT_BUTTON, self.findFolder, btnOriginal)
        self.Bind(wx.EVT_BUTTON, self.process, btnCut)
        
        # test case (example for an mp3 of 2mn30s duration
        self.entryCue1.SetValue("00.00.33")
        self.entryCue2.SetValue("00.01.36")
        self.entryCue3.SetValue("00.02.32")

        # layout
        vbox=wx.BoxSizer(wx.VERTICAL)   
        vbox.Add(btnOriginal,0,wx.ALIGN_CENTER|wx.ALL,border=10)
        vbox.Add(self.entryOriginal,0,wx.ALIGN_CENTER|wx.ALL,border=5)
        vbox.Add(labelCuts,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(self.entryCue1,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(self.entryCue2,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(self.entryCue3,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(self.entryCue4,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(self.entryCue5,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(btnCut,0,wx.ALIGN_CENTER|wx.ALL,border=10)
        panel.SetSizer(vbox)
        
        self.Show(True)     
    
    def findFolder(self,evt):  
        """ select original recording folder """
        openDir=wx.DirDialog(self)
        openDir.ShowModal()
        self.recordingPath=openDir.GetPath()
        print self.recordingPath
        self.entryOriginal.SetValue(self.recordingPath)
        
    def process(self,evt): 
        """ process and cut """
        self.cutTimes=[]
        self.cutTimes.append(0)
        # get cut times
        c1=self.entryCue1.GetValue()
        c2=self.entryCue2.GetValue()
        c3=self.entryCue3.GetValue()
        c4=self.entryCue4.GetValue()
        c5=self.entryCue5.GetValue()
        if c1 != "": self.cutTimes.append(self.time_in_seconds(c1))
        if c2 != "": self.cutTimes.append(self.time_in_seconds(c2))
        if c3 != "": self.cutTimes.append(self.time_in_seconds(c3))
        if c4 != "": self.cutTimes.append(self.time_in_seconds(c4))
        if c5 != "": self.cutTimes.append(self.time_in_seconds(c5))
        print "- Cut times defined by the user:"
        print self.cutTimes
        print "- reading timecode file..."
        f_global_timecode=open(self.recordingPath+"\\timecode.csv")
        global_times=f_global_timecode.read().split("\n")[:-1]
        print ">>> ---",global_times
        print "- global time code:"
        # 
        ix=0
        for x in global_times: 
            global_times[ix]=round(float(x),2)
            ix+=1
        print global_times
        
        #cut main mp3 file into tracks p1.mp3, p2.mp3, etc
        totalTracks=len(self.cutTimes)-1
        print "totalTracks:",str(totalTracks)
        cutIndex=0
        for tr in range(totalTracks):
            cutBegin=self.time_in_ms(self.cutTimes[cutIndex])
            print "cutBegin:",cutBegin
            cutEnd=self.time_in_ms(self.cutTimes[cutIndex+1])
            print "cutEnd:",cutEnd
            mp3ToCut=self.recordingPath+"\\enregistrement-micro.mp3"
            print "mp3ToCut: ",mp3ToCut
            mp3Output="p"+str(cutIndex+1)+".mp3"
            print "mp3Output: ",mp3Output
            os.system('mp3splt.exe "%s" %s %s -d "%s" -o %s ' \
            % (mp3ToCut,cutBegin,cutEnd,self.recordingPath,mp3Output))
            cutIndex+=1
                
        for i in [1,2,3,4,5]:
                
            if os.path.isfile(self.recordingPath+"/p"+str(i)+".mp3"):
                print "- found a p"+str(i)+".mp3 file"
                print "- creating folder p"+str(i)
                try:
                    os.mkdir(self.recordingPath+"/p"+str(i))
                except:
                    pass
                print "- moving p"+str(i)+".mp3 file in his new folder and renaming"
                os.system('move "%s" "%s"' % (self.recordingPath+"\\p"+str(i)+".mp3",
                                          self.recordingPath+"\\p"+str(i)+"\\enregistrement-micro.mp3"))
                print "- renaming mp3 file to enregistrement-micro.mp3"
                print "- making screenshot folder"
                try:
                    os.mkdir(self.recordingPath+"\\p"+str(i)+"\\screenshots")
                except:
                    pass
                #create a smile file for this track
                smil=SmilGen("audio",self.recordingPath+"\\p"+str(i)+"\\")
                #create a timecode file for this track
                timecodeFile=open(self.recordingPath+"\\p"+str(i)+"\\timecode.csv",'a')
                print "Found slides for this track:"
                diaIDglob=1
                diaIDtrack=1
                for j in global_times:
                    if (float(j)< self.cutTimes[i]) and (float(j)> self.cutTimes[i-1]):
                        print ">>> "+str(j)
                        if i>1 and diaIDtrack==1:
                            # Make a copy of the last slide in the previous track
                            os.system('copy "%s" "%s"' % (self.recordingPath+"\\screenshots\\D"+str(diaIDglob-1)+".jpg",
                                    self.recordingPath+"\\p"+str(i)+"\\screenshots\\D"+str(diaIDtrack)+".jpg"))
                            os.system('copy "%s" "%s"' % (self.recordingPath+"\\screenshots\\D"+str(diaIDglob-1)+"-thumb.jpg",
                                    self.recordingPath+"\\p"+str(i)+"\\screenshots\\D"+str(diaIDtrack)+"-thumb.jpg"))
                            # write time of this first slide
                            timecodeFile.write("0.00"+"\n")
                            # write smil file
                            smil.smilEvent("0.00",diaIDtrack)
                            diaIDtrack+=1
                            
                        # Make a copy of the j slides and thumbnails  and rename
                        os.system('copy "%s" "%s"' % (self.recordingPath+"\\screenshots\\D"+str(diaIDglob)+".jpg",
                                self.recordingPath+"\\p"+str(i)+"\\screenshots\\D"+str(diaIDtrack)+".jpg"))
                        os.system('copy "%s" "%s"' % (self.recordingPath+"\\screenshots\\D"+str(diaIDglob)+"-thumb.jpg",
                                self.recordingPath+"\\p"+str(i)+"\\screenshots\\D"+str(diaIDtrack)+"-thumb.jpg"))
                        # corrected time and write time code
                        adjustedTime=j-float(self.cutTimes[i-1])
                        timecodeFile.write(str(adjustedTime)+"\n")
                        # write smil file
                        smil.smilEvent(str(adjustedTime),diaIDtrack)
                        
                        diaIDtrack+=1
                    diaIDglob+=1       
                timecodeFile.close()
                smil.smilEnd("audio")
        print "Finished processing!"
                               
    def time_in_seconds(self,time="00.00.00"):
        """ Returns integer seconds from hh:mm:ss format"""
        t=time.split(".")
        seconds= int(t[0])*3600+ int(t[1])*60+int(t[2])
        return seconds
    
    def time_in_ms(self,time=0.0):
        """ Where input time is in seconds and returns time as mm.ss for mp3split"""
        hh=int(time//3600)
        time_left=time%3600
        mm=int(time_left//60)
        ss=int(time_left%60)
        minutes= hh*60+mm
        timeResult=str(minutes)+"."+str(ss)    
        if 1: print ">>> computed timeResult :",timeResult
        return timeResult

class SmilGen:
    """ A class to produce a SMIL file on the fly """
    def __init__(self,usage,workDirectory):
        """ Create the first part of the smil file """
        self.smilBegin='<?xml version="1.0"?>\n'\
        +'<!DOCTYPE smil PUBLIC "-//W3C//DTD SMIL 2.0//EN" "http://www.w3.org/2001/SMIL20/SMIL20.dtd">\n'\
        +'<smil xmlns="http://www.w3.org/2001/SMIL20/Language">\n'\
        +'<head>\n'\
        +'<meta name="title" content="MediaCours"/>\n'\
        +'<meta name="author" content="ULP Multimedia"/>\n'\
        +'<meta name="copyright" content="Copyright ULP Multimedia"/>\n'
        if usage=="audio":
            self.smilLayout='<layout>\n'\
            +'<root-layout width="1024" height="768"/>\n'\
            +'<region id="Images" width="1024" height="768" fit="meet" />\n'\
            +'</layout>\n'\
            +'</head>\n'\
            +'<body>\n'\
            +'<par>\n'
        if usage=="video":
            self.smilLayout="""<layout>
            <root-layout width="800" height="600"/>
            <region id="Images" left="0" width="800" height="600" fit="meet" />
            <topLayout width="320" height="240">
            <region id="Video" left="0" width="320" height="240" fit="meet"/>
            </topLayout>
            </layout>
            </head>
            <body>
            <par>"""
            
        self.smilFile=open (workDirectory +'\\cours.smil','w')
        self.smilFile.write(self.smilBegin)
        self.smilFile.write(self.smilLayout)
        
    def smilEvent(self,timeStamp,diaId):
        """     
        When screenshot occur => writting the event in the SMIL
        and link it to the screenshot in the screenshots folder
        Parameter:
        timeStamp: a time stamp for the event (number of seconds since the 
        begining of the recording)
        """
        self.smilFile.write('<a href="screenshots/D'+str(diaId)+'.jpg" external="true">\n'\
        + '<img begin="'+timeStamp+'" region="Images" src="screenshots/D'\
        + str(diaId)+'.jpg"/> </a>\n')
        
    def smilEnd(self,usage,videoEncoder="real"):
        """ 
        Write the end part of the SMIL file
        Parameters:
        usage= "audio" or "video"
        videoEncoder= "real" or "wmv" 
         """
        if usage=="audio":
            self.smilFile.write('<audio src="enregistrement-micro.mp3" />\
            \n</par>\n</body>\n</smil>')
        if usage=="video":
            if videoEncoder=="real":
                self.smilFile.write('<video region="Video"' \
                + ' src="enregistrement-video.rm" />\n'\
                +'</par>\n'\
                +'</body>\n'\
                +'</smil>')
            if videoEncoder=="wmv":
                self.smilFile.write('<video region="Video" '\
                +' src="enregistrement-video.wmv" />\n'\
                +'</par>\n'\
                +'</body>\n'\
                +'</smil>')
            if videoEncoder=="flash":
                self.smilFile.write('<video region="Video" '\
                +' src="enregistrement-video.flv" />\n'\
                +'</par>\n'\
                +'</body>\n'\
                +'</smil>')                                
        self.smilFile.close()

if __name__ == '__main__':
    print "Launching Audio Cut, a tool to cut a recording into smaller ones ..."
    app=wx.App(redirect=False)
    gui=mainFrame(None,title="AVC Cut 0.1")
    app.MainLoop()
    
    