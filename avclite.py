#!/usr/bin/env python
# -*- coding: latin-1 -*-
#####
#
#     Light version of Audiovideocast based on Screencasting
#     Developer : F. Schnell 
#
#####

from __future__ import division

import datetime
import os
import subprocess
import sys
from thread import start_new_thread
import time
import webbrowser
import ConfigParser
import winsound

import wx
from mimify import mp


__version__="1.0"


# Global variables
global pathData,audioinputName,videoFileOutput,recording,maxDuration,url

pathData=""
"Gives recording default folder path"
audioinputName=""
"Audio input name"
videoFileOutput=""
"Video file output path"
#recordingDuration=""
"Duration of the current recording"
recording=False
"recording status True or False"
maxDuration=14400  #14400 = 4h, 3600 = 1h
"max duration 3600=1h"
mp4ToDesktop=True
"record mp4 to Desktop"
url="https://audiovideocast.unistra.fr/avc/myspace_home"
#url="https://audiovideocast-test.u-strasbg.fr/avc/publication_screencast"
"url of the pubish button"

def readConfFile(confFile="configuration-Lite.txt"):
    """ Reading conf. file """
    global url
    fconf=open(confFile,"r")
    config= ConfigParser.ConfigParser()
    config.readfp(fconf)
    if config.has_option("AVCLite","url") == True:
        url=config.get("AVCLite","url")
        print "found url:",url
     

def getAudioVideoInputFfmpeg(pathData=pathData):
        """A function to get Audio input from ffmpeg.exe (http://ffmpeg.zeranoe.com/builds/)
        Returns a list of two lists : [audioDevices,videoDevices]"""
        #ffmpeg.exe don't work with input number. It is necessary to get the name of the Direcshow input.
        #also subprocess.Popen returns an empty string I therefore create the output in a file that i read just after
        #Ask ffmpeg.exe to give devices seen by direcshow on windows and write it to devices.txt file in the AVC data folder       
        cmd = 'ffmpeg -list_devices true -f dshow -i dummy > "%s"\devices.txt 2>&1' %pathData
        if 0: os.system(cmd)
        subprocess.Popen(cmd,stdin=subprocess.PIPE,shell=True)
        #Read back devices.txt
        audioDevices=[] # List of audio devices
        videoDevices=[] # List of video devices
        audioIndex=None # Index position where audio devices listing is starting
        videoIndex=None # Index position where video devices listing is starting
        fileDevices=open(pathData+"\devices.txt","r") #as direct shell communication is not possible (=>file intermediary)
        devicesList=fileDevices.readlines()
        fileDevices.close()
        def fixCaracters(name):
            name=name.replace("Ã©","é")
            name=name.replace("Â®","®")
            name=name.replace("Ã¨","è")
            name=name.replace("Ãª","ê")
            return name
        # searching audio devices
        for index,device in enumerate(devicesList):
            if device.find("audio devices")>0:
                audioIndex= int(index) 
                print "Found 'audio devices' from Direcshow/ffmpeg, taking first device by default (0)"
            if (audioIndex!=None)and(index>audioIndex) and (device.find("exit")<0):
                aDevice=device.split('"')[1]
                print index-(audioIndex+1),":", aDevice
                audioDevices.append(fixCaracters(aDevice))
        # searching video devices
        for index,device in enumerate(devicesList):
            if device.find("video devices")>0:
                videoIndex= int(index) 
                print "Found 'video devices' from Direcshow/ffmpeg, taking first device by default (0)"
            if device.find("audio devices")>0:
                break
            if (videoIndex!=None) and (index>videoIndex):
                aDevice=device.split('"')[1]
                print index-(videoIndex+1),":", aDevice
                videoDevices.append(fixCaracters(aDevice))    
        print "audio device deduced from devices.txt", audioDevices
        print "video device deduced from devices.txt", videoDevices    
        
        if "UScreenCapture" not in videoDevices:
            infoBox=MessageBoxUscreenMedia(frame, "Infos")
        return [audioDevices,videoDevices]
    
def engageRecording(pathData,audioinputName):
    """ Engage recording """
    global ffmpegHandle
    HD720p="1280:720"
    HD1080p="1920:1080"
    SD480p="640:480"
    resolution=HD720p
    time = datetime.datetime.now()
    timeStr=str(time)
    if mp4ToDesktop==False:
        videoFileOutput = pathData+"/"+timeStr[0:10]+'-'+ timeStr[11:13] +"h-"+timeStr[14:16] +"m-" +timeStr[17:19]+"s.mp4"
    if mp4ToDesktop==True:
        videoFileOutput = os.environ["UserProfile"]+"/Desktop/"+timeStr[0:10]+'-'+ timeStr[11:13] +"h-"+timeStr[14:16] +"m-" +timeStr[17:19]+"s.mp4"   
    
    cmd=('ffmpeg -f dshow -i video="UScreenCapture" -f  dshow -i audio="%s" -q 5 -vf scale=%s -pix_fmt yuv420p "%s"')%(audioinputName, resolution, videoFileOutput)

    ffmpegHandle=subprocess.Popen(cmd,stdin=subprocess.PIPE,shell=True)
    # Audio cue to confirm recording state
    winsound.Beep(800,100)
    start_new_thread(checkMedia,(videoFileOutput,10,))
    
def stopRecording():
    """ Stop recording """
    global ffmpegHandle
    recordingEnd=time.time()
    try:
        ffmpegHandle.stdin.write("q") 
        print "sending q command to ffmpeg and wait 20 s before trying to kill "
        ffmpegHandle.kill()
    except:
        print "WARNING: Can't stop properly FFMPEG subprocess, attempting forced taskkill, media may not be directly readable..."
        text=_("WARNING: Can't stop properly FFMPEG subprocess,\n attempting forced stop, media may not be readable.")
        dialog=wx.MessageDialog(None,message=text,caption="WARNING",style=wx.OK|wx.ICON_INFORMATION)
        dialog.ShowModal()
        #writeInLogs("- WARNING: Can't stop properly FFMPEG subprocess, attempting forced taskkill, media may lack header as a result and may not be directly readable... "+ str(datetime.datetime.now())+"\n")
        os.popen("taskkill /F /IM  ffmpeg.exe") 
    winsound.Beep(800,100)
    time.sleep(0.2)
    winsound.Beep(800,100)

def publish(pathData):
    """ Open Publish recording"""
    # Open publishing URL
    webbrowser.open(url, new=2, autoraise=True)
    #subprocess.Popen('explorer "%s"'%(pathData))
    
def openFolder(pathData):
    # Open explorer folder
    subprocess.Popen('explorer "%s"'%(pathData))
        
def createRecordingsFolder():
    """ Create recordings folder """
    # Create a default folder for the recordings
    pathData=os.environ["ALLUSERSPROFILE"]+"\\audiovideocast"
    if os.path.isdir(os.environ["ALLUSERSPROFILE"]+"\\audiovideocast"):
        print "Default user data exists at ALLUSERSPROFILE\\audiovideocast : OK"
    else: 
        print "Creating default data folder in ALLUSERSPROFILE\\audiovideocast"
        os.mkdir(pathData) 
    return pathData

def checkMedia(mediaFile="",checkDelay=10):
    """ Check if the media file - mp3, flv or mp4 - is created and not empty after checkDelay seconds""" 
    fileToCheck=mediaFile
    print"\nIn checkMedia...fileToCheck",fileToCheck
    time.sleep(checkDelay) #gives some time for recording thread to begin
    print "\n checking media file", mediaFile 
    if not os.path.isfile (fileToCheck):
        text=" Probleme d'enregistrement, media non cree."
        dialog=wx.MessageDialog(None,message=text,caption="WARNING",style=wx.OK|wx.ICON_INFORMATION)
        dialog.ShowModal()
    if os.path.isfile (fileToCheck):
        mediaFileSize=os.stat(fileToCheck).st_size
        print "mediaFileSize=",mediaFileSize 
        if mediaFileSize == 0:
            text="L'enregistrement video ou audio semble vide."
            dialog=wx.MessageDialog(None,message=text,caption="WARNING",style=wx.OK|wx.ICON_INFORMATION)
            dialog.ShowModal()

class MessageBoxUscreenMedia(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, pos=(150, 150), size=(450, 260))
        
        panel=wx.Panel(self)
        panel.SetBackgroundColour("#5789FF") 
        textToShow= "\n'Screen Capture DirectShow source Filter' ne semble pas présent sur ce PC,\n Ce filtre permet aux applications Windows d'enregistrer l'écran.\n\nIl peut être téléchargé sur le site du développeur Umedia (page, fichier) :\n" 
        infoLabel = wx.StaticText(panel, -1,  textToShow,style=wx.ALIGN_LEFT)
        infoLabel2 = wx.StaticText(panel, -1,  "\nRelancer l'application après installation.",style=wx.ALIGN_LEFT)
        panel.SetBackgroundColour("steel blue") 
        infoLabel.SetForegroundColour("white")
        infoLabel2.SetForegroundColour("white")
        
        self.btnSiteUmedia = wx.Button(parent=panel, id=-1, label="http://umediaserver.net/components",size=(400,40))
        self.Bind(wx.EVT_BUTTON,self.openUmediaSite,self.btnSiteUmedia)
        
        self.btnDownload = wx.Button(parent=panel, id=-1, label="http://umediaserver.net/bin/UScreenCapture.zip",size=(400,40))
        self.Bind(wx.EVT_BUTTON,self.downloadFilter,self.btnDownload)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(infoLabel, flag=wx.ALIGN_CENTER)
        self.sizer.Add(self.btnSiteUmedia, flag=wx.ALIGN_CENTER)
        self.sizer.Add(self.btnDownload, flag=wx.ALIGN_CENTER)
        self.sizer.Add(infoLabel2, flag=wx.ALIGN_CENTER)
        
        panel.SetSizer(self.sizer)
        panel.Layout()
        self.Show()
        
    def openUmediaSite(self,evt):
        url="http://umediaserver.net/components/index.html"
        webbrowser.open(url, new=2, autoraise=True)
    def downloadFilter(self,evt):
        url="http://umediaserver.net/bin/UScreenCapture.zip"
        webbrowser.open(url, new=2, autoraise=True)    
    

class MainFrame(wx.Frame):
    """ 
    Main frame of the app.
    """
    def __init__(self, parent, title):
        
        global mp4ToDesktop
        wx.Frame.__init__(self, parent, -1, title, pos=(150, 150), size=(850, 690))
        
        self.Bind(wx.EVT_CLOSE, self.onCloseFrame)
        
        panel=wx.Panel(self)
        panel.SetBackgroundColour((29,29,29)) 
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        
        self.faviconIdle = wx.Icon('images/avc_icone.ico', wx.BITMAP_TYPE_ICO)
        self.faviconRecording = wx.Icon('images/avc_icone_on.ico', wx.BITMAP_TYPE_ICO)
        
        self.SetIcon(self.faviconIdle)
    
        self.statusBar=self.CreateStatusBar()
        
        if mp4ToDesktop==True:
            self.statusBar.SetStatusText("Dossier d'enregistrement : Bureau")
        else:
            self.statusBar.SetStatusText("Dossier d'enregistrement : "+pathData)
        
        menubar=wx.MenuBar()
        menuInformation=wx.Menu()
        menubar.Append(menuInformation,"Menu")
        helpMenu=menuInformation.Append(wx.NewId(),"Site Audiovideocast et aide")
        self.Bind(wx.EVT_MENU,self.helpInfos,helpMenu)
        conf=menuInformation.Append(wx.NewId(),"Choisir un autre dossier d'enregistrement")
        self.Bind(wx.EVT_MENU,self.selectFolder,conf)
        version=menuInformation.Append(wx.NewId(),"A propos - Version")
        self.Bind(wx.EVT_MENU,self.about,version)
        self.SetMenuBar(menubar)
                    
        im1 = wx.Image('images/avc_top.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        imExplications=wx.Image('images/avc_bot.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.timeLabel= wx.StaticText(panel, -1,"Durée (hh.mm.ss) : débutez un enregistrement ",size=(800,30),style=wx.ALIGN_CENTER)
        font = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.timeLabel.SetFont(font)
        self.timeLabel.SetForegroundColour("white")
        text1="""\n\n 1) Pour enregistrer l'écran et le micro cliquez sur "Enregistrer!" et cette fenêtre se minimisera automatiquement.\n\n 2) Pour arrêter l'enregistrement cliquez sur le fenêtre "AC" depuis la barre des tâches puis cliquez sur "stop".\n\n 3) Pour accéder à votre enregistrement et éventuellement le publier sur audiovideocast cliquez sur "Explorer"/"Publier".\n"""

        
        self.btnRecord = wx.Button(parent=panel, id=-1, label="Enregistrer !",size=(100,50))
        self.Bind(wx.EVT_BUTTON, self.orderRecording, self.btnRecord)
        self.btnStop = wx.Button(parent=panel, id=-1, label="Stop",size=(100,50))
        self.Bind(wx.EVT_BUTTON, self.orderStopRecording, self.btnStop)
        self.Bind(wx.EVT_BUTTON, self.orderStopRecording, self.btnStop)
        btnPublish = wx.Button(parent=panel, id=-1, label="Publier",size=(100,50))
        self.Bind(wx.EVT_BUTTON, self.orderPublish,btnPublish)
        btnOpen = wx.Button(parent=panel, id=-1, label="Explorer",size=(100,50))
        self.Bind(wx.EVT_BUTTON, self.orderOpen,btnOpen)
        
        sizerV = wx.BoxSizer(wx.VERTICAL)
        sizerH=wx.BoxSizer()
        padding1=65
        sizerV.Add(wx.StaticBitmap(panel, -1, im1, (5, 5)), 0, wx.ALIGN_CENTER|wx.BOTTOM, 25)
        #sizerV.Add(sizerH, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizerV.Add(sizerH, 0, wx.ALIGN_LEFT|wx.LEFT, 105)
        sizerH.Add(self.btnRecord, 0, wx.ALIGN_CENTER|wx.RIGHT, padding1)
        sizerH.Add(self.btnStop, 0, wx.ALIGN_CENTER|wx.RIGHT, padding1)
        sizerH.Add(btnPublish, 0, wx.ALIGN_CENTER|wx.RIGHT, padding1)
        sizerH.Add(btnOpen, 0, wx.ALIGN_CENTER|wx.RIGHT, padding1)
        sizerV.Add(self.timeLabel, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 40)
        
        #sizerV.Add(text, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizerV.Add(wx.StaticBitmap(panel, -1, imExplications, (5, 5)), 0, wx.ALIGN_CENTER|wx.TOP, 0)
        
        panel.SetSizer(sizerV)
        panel.Layout() 

    def onCloseFrame(self, evt):
        print "Destroy main frame"
        global recording
        if recording==True:
            dialog = wx.MessageDialog(self, message = "Arrêter l'enregistrement ?", caption = "Caption", style = wx.YES_NO, pos = wx.DefaultPosition)
            response = dialog.ShowModal()
            if (response == wx.ID_YES):
                stopRecording()
                self.Destroy()
                sys.exit()
            else:
                evt.StopPropagation()
        if recording==False:
            self.Destroy()
            sys.exit()    
    
    def update(self, evt):
        """ Update duration label and stop recording if above maxDuration """
        global maxDuration,recording
        delta=datetime.datetime.now()-self.recordingStart
        self.timeLabel.SetLabel( "Enregistrememt en cours : "+ str(delta)[0:7].replace(":",".") )
        deltaSecs=delta.days*(3600*24)+delta.seconds
        if deltaSecs > maxDuration:
            print "!!! Recording above maximum duration !!!"
            wx.Frame.SetIcon(self, self.faviconIdle)
            self.btnRecord.SetBackgroundColour("white")
            self.btnStop.SetBackgroundColour("white")
            if recording ==True:
                recording=False
                self.timer.Stop()
                wx.Frame.SetIcon(self, self.faviconIdle)
                stopRecording()
            if recording==False:
                self.statusBar.SetStatusText("Enregistrement précédent stoppé car > "+str(maxDuration)+" secondes")
            text="Enregistrement stoppé car trop long (> "+str(maxDuration/3600)+" heures)" 
            dialog=wx.MessageDialog(self,message=text,
            style=wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
            dialog.ShowModal()
            
        
    def orderRecording(self,evt):
        """Order recording from GUI button"""
        #self.btnRecord.SetBackgroundColour((117,117,117))
        #self.btnRecord.SetWindowStyle(wx.SUNKEN_BORDER)
        #self.btnRecord.Refresh()
        self.btnRecord.SetForegroundColour((117,117,117))
        if 0: self.btnStop.SetBackgroundColour((43,223,188))
        self.btnStop.SetBackgroundColour((253,174,79))
        self.timeLabel.SetForegroundColour((253,106,26))
        def laterOn():
            """ Calllater so the GUI state is visible and non blocking"""
            global recording
            wx.Frame.SetIcon(self, self.faviconRecording)
            if recording==False:
                recording=True
                self.Iconize( True )
                wx.Frame.SetIcon(self, self.faviconRecording)
                self.recordingStart=datetime.datetime.now()
                self.timer.Start(1000)
                engageRecording(pathData,audioinputName)
            if recording==True:
                self.statusBar.SetStatusText("Enregistrement en cours...")
        wx.CallLater(500,laterOn)
        
    def orderStopRecording(self,evt):
        """Order stop recording from GUI button"""
        global recording
        wx.Frame.SetIcon(self, self.faviconIdle)
        self.btnRecord.SetBackgroundColour("white")
        self.btnRecord.SetForegroundColour("black")
        self.btnStop.SetBackgroundColour("white")
        self.timeLabel.SetForegroundColour("white")
        self.timeLabel.Refresh()
        self.timeLabel.SetLabel("- Fin d'enregistrement -")
        if recording ==True:
            recording=False
            self.timer.Stop()
            #tbicon.SetIcon(icon1, "Audiovideocast en attente")
            #self.tbicon.SetIcon(self.faviconIdle, "Audiovideocast en attente...")
            wx.Frame.SetIcon(self, self.faviconIdle)
            stopRecording()
        if recording==False:
            self.statusBar.SetStatusText("Pas d'enregistrement en cours")
            
    def orderOpen(self,evt):
        """ Order Open/Publish from the GUI button"""
        global mp4ToDesktop
        if mp4ToDesktop==False:
            openFolder(pathData)
        if mp4ToDesktop==True:    
            print "go to", os.environ["UserProfile"]+"/Desktop/"
            openFolder(os.environ["UserProfile"]+"\\Desktop")
            
    def orderPublish(self,evt):
        """ Order Open/Publish from the GUI button"""
        publish(pathData)
        
    def helpInfos(self,evt):
        """ A function to provide help on how to use the software"""
        url="http://audiovideocast.unistra.fr"
        webbrowser.open(url, new=2, autoraise=True)
        
    def selectFolder(self,evt):
        """ A function to select the recording folder"""
        global pathData,mp4ToDesktop
        print "In configuration"
        openDir=wx.DirDialog(self)
        openDir.ShowModal()
        selectedPath=openDir.GetPath()
        if selectedPath !="":
            pathData= selectedPath
        print  "has been changed to ...",pathData
        self.statusBar.SetStatusText("Dossier d'enregistrement : "+pathData)
        mp4ToDesktop=False
        
    def about(self,evt):
        """ A function to show an about popup"""
        text="AudioVideoCast Lite version "+__version__+"  \n\nhttp://audiovideocast.unistra.fr/\n\n"
        dialog=wx.MessageDialog(self,message=text,
        style=wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
        dialog.ShowModal()

if __name__=="__main__":
        
    __version__="1.0"
    
    readConfFile()
    
    # Create a data folder if not present in ALLUSERSDATA
    pathData=createRecordingsFolder()
    
    app=wx.App(redirect=False)
    frame = MainFrame(None, "Audiovideocast Lite") 
    frame.Show(True)
    
    # Use audio source
    try:
        audioinputName=getAudioVideoInputFfmpeg(pathData)[0][0]
    except IndexError:
        text="Merci de brancher un micro et de relancer l'application."
        #dialog=wx.MessageBox(text, 'Audiovideocast Lite Warning', wx.OK | wx.ICON_INFORMATION)
        dialog=wx.MessageDialog(None,message=text,caption="Audiovideocast Lite WARNING",style=wx.OK|wx.ICON_INFORMATION)
        dialog.ShowModal()

        
        
    
    app.MainLoop()