#!/usr/bin/env python
# -*- coding: latin-1 -*-
#*****************************************************************************
#
#     MediaCours (Windows AudioVideoCast client and 'standalone' version)
#     Also known as Audiovideocours (previous name)
#    (c) Universite de Strasbourg  2006-2012
#     Conception and development : francois.schnell [AT] unistra.fr  
#---
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#*******************************************************************************


__version__="2.0a2"

## Python import (base Python 2.4)
import sys,os,time,datetime,tarfile,ConfigParser,threading,shutil,gettext,zipfile
import subprocess, socket, winsound, traceback, webbrowser
from thread import start_new_thread, exit
from urllib2 import urlopen
from os import chdir
from ftplib import FTP

## External Python libs import
import wx, wx.lib.colourdb # GUI
import wx.lib.hyperlink as hl
import msvcrt,pythoncom,pyHook,serial # access MS C/C++ Runtime lib, MS COM, hook, serial port
from PIL import GifImagePlugin  # Python Imaging Lib
from PIL import JpegImagePlugin # Static imports from PIL for py2exe
from PIL import Image, ImageGrab# used for screenshots
import pymedia.audio.sound as sound # for mp3 or ogg encoding
import pymedia.audio.acodec as acodec
import pymedia.muxer as muxer
from pywinauto import * # used to put app. back on foreground
#from reportlab.platypus.doctemplate import FrameBreak # PDF lib.
import cherrypy

## Local imports 
from FMEcmd import * # Script to control Flash Media Encoder and genrate profile.xml file
import htmlBits      # HTML chuncks for html format output

#----------------------------------------------------------------------------------------

## Some default global variables in case no configuration file is found
videoFormatFFMPEG="flv"
"parameter for FFMPEG encoder used since version 2.0 of the AVC client, flv or mp4 (flv by default until AVC server compatible with client mp4 uploads)"
audioEncoder=False
"Choice of audio encoder (if any, otherwise False)"
videoEncoder="flash"
"""Choice of the videoencoder to use if usage=video
'wmv' = Windows Media Encoder ; 'real'= Real producer """
remoteControl=False
"If True the client will also act as a mini server for maintenance purposes. Go to http://your-PC:port"
remotePort="8080"
"Remote access port"
standalone=True
"GUI design, False=amphi (always running in background, minimal choices), True= individual PC"
# Publishing form variables
publishingForm=False
"Indicates there's no publishing form on the client and everything is done on the website"
title=""
"Recording's title"
description=""
"Recording's description"
name=""
"Author's name"
firstname=""
"Author's firstname"
login=""
"Author's login"
genre=""
"Eventual access code"
ue=""
" To use the app without a  webserver to publish to"
recording = False
" Recording Status : to know if we are recording now" 
last_session_recording_start="None"
" Date/time of the last recording start since the app. is running"
last_session_recording_stop="None"
" Date/time of the last recording stop since the app. is running"
app_startup_date="None"
"Date/time when the app. has been launched"
last_session_publish_order="None"
"Date/time when the app. has been launched"
last_session_publish_problem="None"
"Date/time when the app. encountered an error while publishing "
workDirectory="" 
"The working/current directory"
dirName=""
"The data directory"
pathData=None
"Path/name of the folder containing the recordings"
id= ""
"An id which can be received and send from the socket (for external control or monitoring)"
samplingFrequency= 48000
"Default sampling frequency for audio recording"
stopKey= "F8" 
"Default key to start/stop recording if you don't have the serial Kb"
socketEnabled=False
"To listen to a socket for eventual orders from a server"
portNumber= 3737
"Socket port to listen to for server orders (sending an eventual ID also)"
READ_CHUNK= 512
"Chunck size for pymedia audio reading"
cparams= { 'id': acodec.getCodecID( 'mp3' ),
           'bitrate': 64000,
           'sample_rate': 48000 ,
           'channels': 1 } 
"Set of parameters for the pymedia audio Encoder"
nameRecord="enregistrement-micro.mp3"
"Dafault name of the audio recording"        
tryFocus=False
"A boolean variable to inform when the app is trying to get focus back on a frame"
serialKeyboard=False
"To indicate if the special keyboard must be used"
keyboardPort=0
"Serial port number to use for serial keyboard"
videoprojectorInstalled=False
"To indicate if a videoprojector bust be used on a serial plug"
videoprojectorPort=1
"Port number of the serial port for the videoprojector"
tempo = 0
"If tempp = 0 => no tempo (Nb of seconds to wait before each screenshot)"
lastEvent=time.time()
"Initialize last Event time as a global variable"
videoProjON='PWR ON\x0D'
"Video proj protocol : ON (EPSON here)"
videoProjOFF='PWR OFF\x0D'
"Video proj protocol : OFF (EPSON here)"
ftpUrl="audiovideocours.u-strasbg.fr"
"FTP URL server for online publication"
urlserver= "https://audiovideocours.u-strasbg.fr/avc/publication"
"Default URL of the audiovideocours server containing the submit form"
urlLiveState="http://audiovideocast.unistra.fr/avc/livestate"
"URL of the live form status"
eventDelay=1.5
"Number of seconds before allowing a new screenshot"
recordingPlace= "not given"
"Optional location indication for the log file and the server" 
maxRecordingLength=18000
"Maximum recording length in seconds(1h=3600s,5h=18000s)"
usage="audio"
"Usage ='audio' for audio and 'video' for video recording or 'screencast' for screen grabbing / screencasting (Grab the desktop as a video source, requires FFMPEG and 'Screen Capture DirectShow source filter' freeware on Windows)"
"A generic access code"
smilBegin=""" <?xml version="1.0"?>
<!DOCTYPE smil PUBLIC "-//W3C//DTD SMIL 2.0//EN" "http://www.w3.org/2001/SMIL20/SMIL20.dtd">
<smil xmlns="http://www.w3.org/2001/SMIL20/Language">
<head>
<meta name="title" content="MediaCours"/>
<meta name="author" content="ULP Multimedia"/>
<meta name="copyright" content="Copyright ULP Multimedia"/>
<layout>
<root-layout width="1024" height="768"/>
<region id="Images" width="1024" height="768" fit="meet" />
</layout>
</head>
<body>
<par>
"""
"Smil template"
loginENT="initial"
"Login"
emailENT="initial"
"Email"
live=False
"Live choice enable or not in GUI"
language="French"
"Current language in the GUI"
videoinput="0"
"Video input"
audioinput="0"
"Audio input"
flashServerIP="130.79.188.196"
"Flash Server IP for live sessions"
formFormation="" # a default entry for "formation" in the publishing form
"Automatically fills the formation field with this value"
lastGlobalEvent=time.time()
"Indicates last keyboard or mouse activity"
liveCheckBox=False
"Indicates if user wants(checked) a live session from the GUI"
audioVideoChoice=False # give the possibility to choose between an audio or video recording
"Show in the GUI the choice between a video or audio recording"
screencastChoice=False
"Show in the GUI an additional choice for screencasting"
ftpHandleReady=False
"For live session: indicates if we have an open FTP connection to send live screenshots"
previewPlayer="realplayer"
"Standalone preview player ( realplayer or browser), used in standalone mode only"
if 1:# in case no server informations found in the configuration file
    ftpLogin=""
    "FTP login for publishing and live screenshots"
    ftpPass=""
    "FTP password for publishing and live screenshots"
    
#------- i18n settings ------------------------------------------------------------------
gettext.install("mediacours","locale")
#----------------------------------------------------------------------------------------

def readConfFile(confFile="mediacours.conf"):
    """ 
    Read the configuration file and get those values as global vars 
    """
    print "Search and read configuration (if it exist):"
    
    global confFileReport,id,urlserver,samplingFrequency,createMp3,stopKey,portNumber,pathData\
    ,serialKeyboard,startKey,videoprojectorInstalled,videoprojectorPort,keyboardPort\
    ,videoProjON,videoProjOFF,ftpUrl,eventDelay,maxRecordingLength,recordingPlace\
    ,usage,cparams,bitrate,socketEnabled,standalone,videoEncoder,audioEncoder,amxKeyboard,liveCheckBox,\
    language,ftpLogin,ftpPass,cparams, videoinput,audioinput,flashServerIP\
    ,formFormation, audioVideoChoice,urlLiveState,publishingForm, remoteControl, remotePort,previewPlayer, videoFormatFFMPEG, screencastChoice
    
    confFileReport=""
    
    section="mediacours"
    
    def readParam(param):
        global confFileReport
        param=str(param)
        paramValue= config.get(section,param)
        if paramValue=="True" or paramValue=="False":
            paramValue=eval(paramValue)
        if (param != "ftpPass") and (param != "ftpLogin"):
            print "... "+param+" = ", paramValue
            #writeInLogs("\n\t:"+param+"= "+paramValue)
            confFileReport += "\n\t:"+str(param)+"= "+str(paramValue)
        return paramValue
    try:
    #if 1:
        fconf=open(confFile,"r")
        config= ConfigParser.ConfigParser()
        config.readfp(fconf)
        if config.has_option(section,"language") == True: language=readParam("language")
        if config.has_option(section,"usage") == True: usage=readParam("usage")
        if config.has_option(section,"pathData") == True: pathData=readParam("pathData")
        if config.has_option(section,"standalone") == True: standalone=readParam("standalone")
        if config.has_option(section,"videoEncoder") == True: videoEncoder=readParam("videoEncoder")
        if config.has_option(section,"audioEncoder") == True: audioEncoder=readParam("audioEncoder")
        if config.has_option(section,"urlserver") == True: urlserver=readParam("urlserver")
        if config.has_option(section,"samplingFrequency") == True: samplingFrequency=readParam("samplingFrequency")
        if config.has_option(section,"bitrate") == True: cparams['bitrate']=eval(readParam("bitrate"))
        if config.has_option(section,"stopKey") == True: stopKey=readParam("stopKey")
        if config.has_option(section,"socketEnabled") == True: socketEnabled=readParam("socketEnabled")
        if config.has_option(section,"portNumber") == True: portNumber=int(readParam("portNumber"))
        if config.has_option(section,"serialKeyboard") == True: serialKeyboard=readParam("serialKeyboard")
        if config.has_option(section,"amxKeyboard") == True: amxKeyboard=readParam("amxKeyboard")
        if config.has_option(section,"keyboardPort") == True: keyboardPort=int(readParam("keyboardPort"))
        if config.has_option(section,"videoprojectorInstalled") == True: videoprojectorInstalled=readParam("videoprojectorInstalled")
        if config.has_option(section,"videoprojectorPort") == True: videoprojectorPort=int(readParam("videoprojectorPort"))
        if config.has_option(section,"videoProjON") == True: videoProjON=readParam("videoProjON")
        if config.has_option(section,"videoProjOFF") == True: videoProjOFF=readParam("videoProjOFF")
        if config.has_option(section,"ftpUrl") == True: ftpUrl=readParam("ftpUrl")
        if config.has_option(section,"eventDelay") == True: eventDelay=float(readParam("eventDelay"))
        if config.has_option(section,"maxRecordingLength") == True: maxRecordingLength=float(readParam("maxRecordingLength"))
        if config.has_option(section,"ftpLogin") == True: ftpLogin=readParam("ftpLogin")
        if config.has_option(section,"ftpPass") == True: ftpPass=readParam("ftpPass")
        if config.has_option(section,"live") == True: liveCheckBox=readParam("live")
        if config.has_option(section,"videoinput") == True: videoinput=readParam("videoinput")
        if config.has_option(section,"audioinput") == True: audioinput=readParam("audioinput")
        if config.has_option(section,"flashServerIP") == True: flashServerIP=readParam("flashServerIP")
        if config.has_option(section,"formFormation") == True: formFormation=readParam("formFormation")
        if config.has_option(section,"audioVideoChoice") == True: audioVideoChoice=readParam("audioVideoChoice")
        if config.has_option(section,"screencastChoice") == True: screencastChoice=readParam("screencastChoice")
        if config.has_option(section,"urlLiveState") == True: urlLiveState=readParam("urlLiveState")
        if config.has_option(section,"publishingForm") == True: publishingForm=readParam("publishingForm")
        if config.has_option(section,"remoteControl") == True: remoteControl=readParam("remoteControl")
        if config.has_option(section,"remotePort") == True: remotePort=int(readParam("remotePort"))
        if config.has_option(section,"previewPlayer") == True: previewPlayer=readParam("previewPlayer")
        if config.has_option(section,"videoFormatFFMPEG") == True: videoFormatFFMPEG=readParam("videoFormatFFMPEG")
        #if config.has_option(section,"screencasting") == True: screencasting=readParam("screencasting")
        
        fconf.close()
    except:
    #if 0:
        print "Something went wrong while reading the configuration file..."

def showVuMeter():
    """ If available in installation folder show VUMeter.exe
    http://www.vuplayer.com/files/vumeter.zip """
    try:
        subprocess.Popen(["VUMeter.exe"])
    except:
        print "Couldn't find VUMeter.exe"    
             
def stopFromKBhook():
    """
    Start/stop recording when asked from the PC keyboard 'stopKey'
    """
    global frameEnd, frameBegin, tryFocus,id
    #screenshot()#gives a delay too long in case of live recording here
    if recording==False and tryFocus==False:
        windowBack(frameBegin)
        showVuMeter()
        # try to show a vumeter here
        #showVuMeter()
    if recording==True and tryFocus==False:
        print "id:",id
        if id=="":
            print "Trying to put Ending frame back foreground..."
            if live==False:
                screenshot()
            print "stop recording now recordStop()"    
            recordStop()
            windowBack(frameEnd)
            
        else:
            recordStop()
            print "Not showing usual publishing form"
            start_new_thread(confirmPublish,())
            frameUnivr.Show()
    # make sure buttons "publish" and "cancel" are enabled for user input
    #if 1:
    try:
        if btnPublish.IsEnabled()==False:
            btnPublish.Enable(True)
        if btnCancel.IsEnabled()==False:
            btnCancel.Enable(True)
    except:
        print "warning! tried to check if buttons 'publish' and 'cancel' were enabled but had problems" 
            
def OnKeyboardEvent(event):
    """
    Catching keyboard events from the hook and deciding what to do
    """
    global stopKey,lastEvent,lastGlobalEvent
    if 0: winsound.Beep(300,50) # For testing purposes
    lastGlobalEvent=time.time()# For shutdownPC_if_noactivity
    screenshotKeys=["Snapshot","Space","Return","Up","Down","Right",
    "Left","Prior","Next"]
    if (stopKey!="") and (event.Key== stopKey)and (tryFocus==False):
        print "from hook stopKey= :", stopKey
        global recording, fen1
        print "Escape Key pressed from the hook ..."
        start_new_thread(stopFromKBhook,())
    if event.Key in screenshotKeys and( (time.time()-lastEvent)>eventDelay):
       start_new_thread(screenshot,()) 
       lastEvent=time.time()
    # Show each key stroke (for debug only)
    if 0:
        print 'MessageName:',event.MessageName
        print 'Message:',event.Message
        print 'Time:',event.Time
        print 'Window:',event.Window
        print 'WindowName:',event.WindowName
        print 'Ascii:', event.Ascii, chr(event.Ascii)
        print 'Key:', event.Key
        print 'KeyID:', event.KeyID
        print 'ScanCode:', event.ScanCode
        print 'Extended:', event.Extended
        print 'Injected:', event.Injected
        print 'Alt', event.Alt
        print 'Transition', event.Transition
        print '---'
    return True # return True to pass the event to other handlers 

def OnMouseEvent(event):
    """
    Catching mouse events from the hook and deciding what to do
    """
    global recording,lastEvent,lastGlobalEvent
    lastGlobalEvent=time.time()# For shutdownPC_if_noactivity
    if  (recording == True) and (tryFocus == False)\
    and( (time.time()-lastEvent)>eventDelay):
        if (event.MessageName == "mouse left down") or (event.Wheel==1)\
         or (event.Wheel==-1):
            if 0: winsound.Beep(300,50) # For testing purposes
            start_new_thread(screenshot,())
            lastEvent=time.time()
    if 0: # For debug purpose put 0 for example
        print 'MessageName:',event.MessageName
        print 'Message:',event.Message
        print 'Time:',event.Time
        print 'Window:',event.Window
        print 'WindowName:',event.WindowName
        print 'Position:',event.Position
        print 'Wheel:',event.Wheel
        print 'Injected:',event.Injected
        print '---'
    return True # return True to pass the event to other handlers 

def recordNow():
    """
    Record the audio input now with pymedia or video via an external encoder 
    """
    global recording, diaId, timecodeFile, t0, dateTime0, dirName, workDirectory
    global snd,ac,cparams, nameRecord,usage,smil,pathData, last_session_recording_start
    usage=frameBegin.usage
    recording= True
    last_session_recording_start=getTime()
    ftpHandleReady=False
    # Visual cue to confim recording state
    tbicon.SetIcon(icon2, "Enregistrement en cours")
    # Audio cue to confirm recording state
    winsound.Beep(800,100)
    diaId = 0 # initialize screenshot number and time
    t0 = time.time() 
    dateTime0 = datetime.datetime.now()
    print "- Recording now ! ... ( from recordNow() )"
    dirName = str(dateTime0)
    dirName = dirName[0:10]+'-'+ dirName[11:13] +"h-"+dirName[14:16] +"m-" +dirName[17:19]+"s"+"-"+recordingPlace#+ "-"+ dirName[20:22]
    workDirectory=pathData+"\\"+dirName
    print "workDirectory= ",workDirectory
    os.mkdir(workDirectory)
    writeInLogs("- Begin recording at "+ str(datetime.datetime.now())+"\n")
    os.mkdir(workDirectory + "/screenshots")
    start_new_thread(screenshot,())    
    
    def record():
        """ Record audio only - mp3 - with pymedia"""
        global recording, cparams
        f= open( workDirectory+'\\'+nameRecord, 'wb' )
        ac= acodec.Encoder( cparams )
        snd= sound.Input(cparams["sample_rate"],cparams["channels"], sound.AFMT_S16_LE)
        snd.start()
        while recording==True:
            time.sleep(0.1)
            if (time.time()-t0 > maxRecordingLength): 
                writeInLogs("- Recording duration > maxRecordingLength => Stop recording  "+\
                str(datetime.datetime.now())+"\n")
                recordStop()
            s= snd.getData()
            if s and len( s ):
              for fr in ac.encode(s):
                f.write( fr )
                #print "*",
            if recording == False:
                snd.stop()
                print "-- stopped recording now --"

    def ffmpegAudioRecord():
        """ Record mp3 using FFMPEG and liblamemp3 """
        print "In ffmpegAudioRecord function"
        audioFileOutput=workDirectory+"/"+nameRecord
        #cmd="ffmpeg.exe -f alsa -ac 2 -i pulse -acodec libmp3lame  -aq 0  -y -loglevel 0 "+workDirectory+"/"+nameRecord
        cmd=('ffmpeg -f dshow -i audio="'+audioinputName+'" "%s"')%(audioFileOutput)
        print "send cmd to DOS:", cmd
        if 0: # No possibility to hide DOS window this way    
            os.system(cmd)
        if 1:
            subprocess.Popen(cmd, shell=True)
        
    def ffmpegScreencastingRecord():
        """Record the desktop as a video source, requires FFMPEG and 'Screen Capture DirectShow source filter' on Windows """
        global audioinput, videoinput
        print "In ffmpegScreencastingRecord"
        print "Searching for audioinput text at postion 0"
        videoFileOutput=workDirectory+"/enregistrement-video."+videoFormatFFMPEG
        #audioinputName= getAudioVideoInputFfmpeg(pathData=pathData)[0][int(audioinput)]
        #videoinputList= getAudioVideoInputFfmpeg(pathData=pathData)[1]
        if "UScreenCapture" not in videoinputList:
            dialogText= "Didn't find 'UScreenCapture' as the default video source for screen recording\n "\
             " please stop (F8) and check you've installed 'Screen Capture DirectShow source filter' \n "\
             "Windows freeware : http://www.umediaserver.net/umediaserver/download.html" 
            print dialogText
            dialog=wx.MessageDialog(None,message=dialogText,
            style=wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
            dialog.ShowModal()
            return 0
        if videoFormatFFMPEG=="flv": 
            cmd=('ffmpeg -f dshow -i video="UScreenCapture" -f dshow -i audio="%s" -q 5 "%s"')%(audioinputName, videoFileOutput)
            subprocess.Popen(cmd,shell=True)
        if videoFormatFFMPEG=="mp4": 
            cmd=('ffmpeg -f dshow -i video="UScreenCapture" -vcodec mpeg4 -f dshow -i audio="%s" -q 5 "%s"')%(audioinputName, videoFileOutput)
            subprocess.Popen(cmd,shell=True)
        #os.system(cmd)
        
    def ffmpegVideoRecord():
        """Record video using FFMPEG """
        print "In ffmpegVideoRecord..."
        global audioinput, videoinput
        videoFileOutput=workDirectory+"/enregistrement-video."+videoFormatFFMPEG
        print "audioinput and videoinput", audioinput,type(audioinput), videoinput, type(videoinput)
        #audioinputName= getAudioVideoInputFfmpeg(pathData=pathData)[0][int(audioinput)]
        #videoinputName= getAudioVideoInputFfmpeg(pathData=pathData)[1][int(videoinput)]
        ## TODO : add a check to be sure there's at least one video source ?
        print "FfmpegVideoRecord video input set to:", videoinputName
        print "FfmpegVideoRecord audio input set to:", audioinputName
        if videoFormatFFMPEG=="flv":
            #hide DOS console:
            if 1:
                print "... ((( Using subprocess to order FFMPEG and hide Shell/DOS window ))) ..."
                subprocess.Popen(["ffmpeg","-f","dshow","-i","video="+videoinputName,"-f","dshow","-i","audio="+audioinputName,"-q","5","%s"%videoFileOutput],shell=True)
            if 0: #worked but switech to subprocess as there's no way to hide the console this way
                cmd=('ffmpeg -f dshow -i video="%s" -f dshow -i audio="%s" -q 5 "%s"')%(videoinputName, audioinputName, videoFileOutput)
        if videoFormatFFMPEG=="mp4": # if we want an mp4 output instead of a flv
            cmd=('ffmpeg -f dshow -i video="%s" -vcodec mpeg4 -f dshow -i audio="%s" -q 5 "%s"')%(videoinputName, audioinputName, videoFileOutput)
            print "send cmd to DOS:", cmd
            os.system(cmd)
        
    def windowsMediaEncoderRecord():
        """
        --- DEPRECATED ---
        Record Video with Windows Media Encoder Series 9
        """ 
        scriptPath=r' cscript.exe C:\"Program Files\Windows Media Components\Encoder\WMCmd.vbs"'
        arguments=" -adevice 1 -vdevice 1 -output "+\
        dirName+"\enregistrement-video.wmv -duration "+str(maxRecordingLength)
        os.system(scriptPath+arguments)
        
    def realProducerRecord():
        """ 
        --- DEPRECATED ---
        Record video with Real Producer basic 
        """
        MaximumRecordingLength=str(maxRecordingLength)
        fileVideo=workDirectory+ '\\enregistrement-video.rm'
        if live==False:
            print "Videoinput and audio port = ",videoinput,audioinput
            os.system(('producer.exe -vc %s -ac %s -pid pid.txt -o "%s" -d %s')%(videoinput,audioinput,fileVideo,MaximumRecordingLength))
        elif live==True:
            #todoLiveReal=r'producer.exe -vc '+videoinput+' -ac '+videoinput+' -pid pid.txt -o '+fileVideo+" -sp 130.79.188.5/"+recordingPlace+".rm"
            page = urlopen(urlLiveState,\
            "recordingPlace="+recordingPlace+"&status="+"begin")
            print "------ Response from Audiocours : -----"
            serverAnswer= page.read() # Read/Check the result
            print serverAnswer
            todoLiveReal=('producer.exe -vc %s -ac %s -pid pid.txt -o "%s" -sp 130.79.188.5/%s.rm')%(videoinput,audioinput,fileVideo,recordingPlace)
            print todoLiveReal
            os.system(todoLiveReal)
            
    def flashMediaEncoderRecord():
        """
        Record video with Flash Media Encoder
        """
        print "In flashMediaEncoderRecord()"
        global flv,flashServer,FMLEpid,urlLiveState
        if live==True:
            print "Going for live==True"
            liveParams="""<rtmp>
            <url>rtmp://"""+flashServerIP+"""/live</url>
            <backup_url></backup_url>
            <stream>"""+recordingPlace+"""</stream>
            </rtmp>"""
            #Send the information that live is ON
            #urlLiveState="http://audiovideocours.u-strasbg.fr/audiocours_v2/servlet/LiveState"
            page = urlopen(urlLiveState,\
            "recordingPlace="+recordingPlace+"&status="+"begin")
            html=page.read()
            if 0:
                print "------ Response from Audiocours : -----"
                serverAnswer= page.read() # Read/Check the result
                print serverAnswer
        else:
            liveParams=""
        #flvPath=r"C:\Documents and Settings\franz\Bureau\newsample.flv"
        if usage=="video":
            flvPath=pathData+'\\'+ dirName+ '\\enregistrement-video.flv'
        elif usage=="audio":
            flvPath=pathData+'\\'+ dirName+ '\\enregistrement-micro.mp3'
            
        print flvPath  
        print "In FlashMediaRecord() videoinput=",videoinput,"audioinput=",audioinput
        print "Current directory is", os.getcwd()
        if os.path.isfile("startup.xml")==True:
            print ">>>   Found startup.xml in AudioVideoCours folder. This profile will be used by Flash Media Encoder insted of the configuration file parameters."
            #subprocess.Popen(["FMEcmd.exe", "/P","startup.xml"])
            flv=FMEcmd(videoDeviceName=videoinput,audioDeviceName=audioinput,
                       flvPath=flvPath,liveParams=liveParams,externalProfile=True,usage=usage,live=live,pathData=pathData)
            flv.record()
            #FMEprocess=flv.record()
            #FMLEpid=FMEprocess.pid
            FMLEpid=flvPath # FME use the full path of the flv not the pid...
        else:
            print "FME: using configuration file parameters"
            flv=FMEcmd(videoDeviceName=videoinput,audioDeviceName=audioinput,
                       flvPath=flvPath,liveParams=liveParams,externalProfile=False,usage=usage,live=live,pathData=pathData)
            flv.record()
            #FMEprocess=flv.record()
            #FMLEpid=FMEprocess.pid
            FMLEpid=flvPath # FME use the full path of the flv not the pid...
    
    def liveStream():
        """ Control VLC for *audio* live stream """
        global vlcPid,dirName
        time.sleep(2)
        print "Going audio live with VLC ..."
        vlcapp='C:\\Program'+' '+'Files\\VideoLAN\\VLC\\vlc.exe'
        command=r'C:\"Program Files"\VideoLAN\VLC\vlc.exe -vvvv '
        file=pathData+"\\"+dirName+"\\enregistrement-micro.mp3"
        typeout="#standard{access=http,mux=raw}"
        # try to launch a pre-configured trayit!.exe to hide VLC GUI
        try:
            subprocess.Popen(['trayit!'])
            #time.sleep(0.5)
        except:
            pass
        if 0: # Using os.system (meaning there will be a DOS window visible)
            os.system('%s -vvvv "%s" --sout %s'%(command,file,typeout))
        if 1: # Using subprocess (no DOS window visible)
            arg1= '-vvvv '+file
            arg2= '"#standard{access=http,mux=asf}"'
            subprocess.Popen(['%s'%(vlcapp),"-vvvv",file,"--sout","%s"%typeout])
    
    # Check for usage and engage recording
    if usage=="audio" and audioEncoder==True:
        start_new_thread(ffmpegAudioRecord,())
    else:
        if usage=="audio" and audioEncoder==False:
            start_new_thread(record,())
        
    if live==True:
        start_new_thread(liveScreenshotStart,())
    
    if live==True and usage=="audio":
        #start_new_thread(liveStream,())
        start_new_thread(flashMediaEncoderRecord,())
    
        #Send the information that live is ON
        page = urlopen(urlLiveState,\
        "recordingPlace="+recordingPlace+"&status="+"begin")
        print ">>>>>>>>>>>>>>>>>>>",urlLiveState
        print ">>>>>>>>>>>>>>>>>>>",recordingPlace
        
        if 0:#For Degub
            print "------ Response from Audiocours : -----"
            serverAnswer= page.read() # Read/Check the result
            print serverAnswer
    print "Usage is > ", usage
    
    if usage=="screencast":
        print "searching for FFMPEG for starting screencasting ..."    
        start_new_thread(ffmpegScreencastingRecord,())
    else:
        if usage=="video" and videoEncoder=="flash":
            print "searching for Flash Media Encoder"    
            start_new_thread(flashMediaEncoderRecord,())
        if usage=="video" and videoEncoder=="ffmpeg":
            print "searching for FFMPEG"    
            start_new_thread(ffmpegVideoRecord,())
        if usage=="video" and videoEncoder=="wmv":
            print "searching Windows Media Encoder ..."   
            start_new_thread(windowsMediaEncoderRecord,())
        if usage=="video" and videoEncoder=="real":
            print "searching Real media encoder"    
            start_new_thread(realProducerRecord,())
                        
def screenshot():
    """
    Take a screenshot and thumbnails of the screen
    """
    global recording, diaId, t0, timecodeFile
    time.sleep(tempo)
    if recording == True: #or False?
        myscreen= ImageGrab.grab() #print "screenshot from mouse"
        t = time.time()
        diaId += 1
        myscreen.save(workDirectory+"/screenshots/" + 'D'+ str(diaId)+'.jpg')
        timeStamp = str(round((t-t0),2))
        print "Screenshot number ", diaId," taken at timeStamp = ", timeStamp
        timecodeFile = open (workDirectory +'\\timecode.csv','a')
        timecodeFile.write(timeStamp+"\n")
        timecodeFile.close()
        """smilFile.write('<a href="screenshots/D'+str(diaId)+'.jpg" external="true">\n'\
        + '<img begin="'+timeStamp+'" region="Images" src="screenshots/D'\
        + str(diaId)+'.jpg"/> </a>\n')"""
        myscreen.thumbnail((256,192))
        myscreen.save(workDirectory+"/screenshots/" + 'D'+ str(diaId)+'-thumb'+'.jpg')
        if live==True and ftpHandleReady:
            time.sleep(3) # in live mode add a tempo to have the current dia (after an eventual transition)
            #if 1:
            try:
                livescreen= ImageGrab.grab()
                livescreen.save(workDirectory+"/screenshots/Dlive.jpg")
                print "[FTP] sending live screenshot"
                f = open(workDirectory+"/screenshots/Dlive.jpg",'rb') 
                ftpHandle.storbinary('STOR '+recordingPlace+'.jpg', f) 
                f.close() 
            #if 0:
            except:
                print "Couldn't send live screenshot to FTP port"
                if recording==True:
                    try:
                        print "trying to open a new FTP handle..."
                        liveScreenshotStart()
                    except:
                        print "Couldn't retry FTP send"
                    
def liveScreenshotStream():
    """ send screenshot at regular interval in live mode"""
    # Function not currently used
    while live==True and recording==True:
        time.sleep(5) # in live mode add a tempo to have the current dia (after an eventual transition)
        f = open(workDirectory+"/screenshots/" + 'D'+ str(diaId)+'.jpg','rb') 
        ftp.storbinary('STOR '+recordingPlace+'.jpg', f) 
        f.close() 
                
def liveScreenshotStart():
    """ Open ftpLiveHandle for live screenshots capabilities """
    global ftpHandle, ftpHandleReady
    #ftpHandleReady=False
    try:
        ftpHandle = FTP(ftpUrl)
        ftpHandle.login(ftpLogin, ftpPass)
        ftpHandle.cwd("live")
        print "[FTP] Opened ftpLiveHandle for live screenshots capabilities "
        ftpHandleReady=True
    except:
        print "couldn't open ftpHandle"

def liveScreenshotStop():
    """ Close ftpLiveHandle """
    global ftpHandle
    ftpHandle.quit()
    ftpHandleReady=False

def recordStop():
    """
    Stop recording the audio input now
    """
    global recording,timecodeFile,FMLEpid, last_session_recording_stop
    print "In recordStop() now..."
    
    ## Create smile file
    try:
        smil=SmilGen(usage,workDirectory)
        f=open(workDirectory+"/timecode.csv")
        diaTime=f.read().split("\n")[:-2]
        f.close()
        diaId=1
        for timeStamp in diaTime:
            smil.smilEvent(timeStamp,diaId+1)
            diaId+=1
        smil.smilEnd(usage,videoEncoder)
    except:
        writeInLogs("- Problem while genration smil file... "+ str(datetime.datetime.now())+"\n") 
    ## Create html file and thirdparty forlder
    try:
        htmlGen()
    except:
        writeInLogs("- Problem at generating html and thirdparty folder... "+ str(datetime.datetime.now())+"\n")
    
    recording= False
    
    last_session_recording_stop=getTime()
    print "Recording is now = ", recording
    # Visual cue to confirm recording state
    tbicon.SetIcon(icon1, usage+"cours en attente")
    # Audio cue to confirming recording state (2 bis when recording stopped)
    winsound.Beep(800,100)
    time.sleep(0.2)
    winsound.Beep(800,100)
    if live==True:
        flv.stop(FMLEpid="rtmp://"+flashServerIP+"/live+"+recordingPlace)
        #if 1:
        try:
            liveScreenshotStop()
        #if 0:
        except:
            print "problem with FTP connection"
    if live==True:
        page = urlopen(urlLiveState,\
        "recordingPlace="+recordingPlace+"&status="+"end")
        if 0:#For debug
            print "------ Response from Audiocours : -----"
            serverAnswer= page.read() # Read/Check the result
            print serverAnswer
    lastEvent=time.time()     
    #timecodeFile.close()
    if usage=="audio" and audioEncoder==True:
        os.popen("taskkill /F /IM  ffmpeg.exe")
    if usage=="video" and videoEncoder=="ffmpeg":
        os.popen("taskkill /F /IM  ffmpeg.exe")
    if usage=="video" and videoEncoder=="wmv":
        os.popen("taskkill /F /IM  cscript.exe")
    if usage=="video" and videoEncoder=="real":
        os.popen("signalproducer.exe -P pid.txt")
    if usage=="video" and videoEncoder=="flash": 
        flv.stop(FMLEpid)
    if usage=="screencast":
        os.popen("taskkill /F /IM  ffmpeg.exe") 
    if live==True:
        liveFeed.SetValue(False) #uncheck live checkbox for next user in GUI    
    """
    if live==True and usage=="audio":
        os.system('tskill vlc')
        try:
            #os.system('tskill trayit!')
            subprocess.Popen(['tskill','trayit!'])
        except:
            pass
    """
    writeInLogs("- Stopped recording at "+ str(datetime.datetime.now())+"\n")
    
def playAudio():
    """
    Play the sound file from the folder selected
    """
    global  workDirectory, fen1 
    print "... playSound"
    mixer= sound.Mixer()
    dm= muxer.Demuxer( 'mp3' )
    dc= acodec.Decoder( cparams )
    sndOut= sound.Output( cparams["sample_rate"],cparams["channels"], sound.AFMT_S16_LE )
    bytesRead= 0
    f= open( workDirectory+'\\'+nameRecord, 'rb' )
    s=' '
    while len( s ):
        s= f.read(READ_CHUNK)
        frames= dm.parse( s )
        if frames:
                for fr in frames:
                  r= dc.decode( fr[ 1 ] )
                  if r and r.data:
                    sndOut.play( r.data )
        else:
              time.sleep( .01 ) 
    while sndOut.isPlaying(): time.sleep( 0.05 )
    sndOut.stop()
    
def createZip():
    """ zip all recording data in a .zip folder """
    frameEnd.statusBar.SetStatusText("Please wait ...(creating archive) ...")
    #frameEnd.statusBar.w
    zip = zipfile.ZipFile(pathData+"\\"+dirName+".zip", 'w')
    for fileName in os.listdir ( workDirectory ):
        if os.path.isfile (workDirectory+"\\"+fileName):
            zip.write(workDirectory+"\\"+fileName,
            dirName+"/"+fileName,zipfile.ZIP_DEFLATED)
    for fileName in os.listdir ( workDirectory+"\\screenshots"):
        zip.write(workDirectory+"\\screenshots\\"+fileName,
            dirName+"/"+"screenshots\\"+fileName,zipfile.ZIP_DEFLATED)
    zip.close()     

def confirmPublish(folder=''):
    """
    Publish the recording when hitting the 'publish' button 
    """
    global id,entryTitle,entryDescription,entryTraining,workDirectoryToPublish, dirNameToPublish,loginENT
    global emailENT,pathData, last_session_publish_order, last_session_publish_problem, standalone
    idtosend=id
    print "sockedEnabled: ", socketEnabled, "id: ",id
    last_session_publish_order=getTime()
    if socketEnabled==True and id != "": # useful for remote order only (doesn't go through publish())
        print "=> Creating Zip file (no publishing form, distant order)"
        workDirectoryToPublish=workDirectory # pathData + dirName
        dirNameToPublish=dirName
        try:
                createZip()
        except:
            print "Warning! couldn't create zip file!" 
    id="" # if confirmPublsih fails id is back to ""
    frameEnd.statusBar.SetStatusText(" Publication en cours, merci de patienter ...")
    # !!!!  Test: changing dirName and workDirectory to dirNameToPublish and workDirectoryToPublish
    # to avoid conflicts when publishing and recording a new file straight away
    if dirNameToPublish =="":
        frameEnd.statusBar.SetStatusText("Rien a publier ...")
    
    if dirNameToPublish != "":   
        writeInLogs("- Asked for publishing at "+ str(datetime.datetime.now())+\
        " with id="+idtosend+" title="+title+" description="+description+" mediapath="+\
        dirNameToPublish+".zip"+" prenom "+firstname+" name="+name+" genre="+genre+" ue="+ue+ " To server ="+urlserver+"\n")
        if 1:
        #try:
            # Send by ftp
            print "Sending an FTP version..."
            ftp = FTP(ftpUrl)
            ftp.login(ftpLogin, ftpPass)
            print "debut de ftp"
            f = open(workDirectoryToPublish+".zip",'rb')# file to send 
            #f = open(pathData+"\\"+dirName+".zip",'rb')# file to send 
            if folder=="canceled":
                print "Trying to open cancel forlder"
                ftp.cwd("canceled") 
            ftp.storbinary('STOR '+ dirNameToPublish+".zip", f) # Send the file
            f.close() # Close file and FTP
            ftp.quit()
            print "fin de ftp"
            if standalone == True:
                frameEnd.Hide()
                frameBegin.Show() 
        if 0:
        #except:
            print "!!! Something went wrong while sending the archive to the server !!!"
            last_session_publish_problem=getTime()
            if standalone == False:
                start_new_thread(rss_warning_client_feed,())
            writeInLogs("!!! Something went wrong while sending the Tar to the server at "\
            +str(datetime.datetime.now())+" !!!\n")
            frameEnd.statusBar.SetStatusText("Impossible d'ouvrir la connexion FTP")
            # Information DialogBox
            caption=_("!!! Publication ERROR !!!")
            text=_("IMPOSSIBLE TO PUBLISH\
            \nIs there an internet connection?\nIs the FTP port opened?")
            dialog=wx.MessageDialog(None,message=text,caption=caption,
            style=wx.OK|wx.ICON_INFORMATION)
            dialog.ShowModal()
            
        if folder=="":
            #try:
            if 1:
                #Send data to the AudioCours server (submit form)
                print "login ENT, emailENT  >>>>>>>>> " ,loginENT, emailENT
                if publishingForm==True:
                    urlParams="id="+idtosend+"&title="+title+"&description="+description+\
                    "&name="+name+"&firstname="+firstname+"&login="+loginENT+"&email="+emailENT+"&genre="+genre+"&ue="+ue+"&mediapath="+\
                    dirNameToPublish+".zip"
                    page = urlopen(urlserver,urlParams)
                    print "urlParams",urlParams
                    print "------ Response from Audiocours : -----"
                    serverAnswer= page.read() # Read/Check the result
                    print serverAnswer
                if publishingForm==False:
                    if idtosend=="": idtosend="none"
                    #urlParams="mediapath="+dirNameToPublish+".zip"+"&id="+idtosend
                    urlParams="mediapath="+dirNameToPublish+".zip"
                    def launch():
                        print "params>>"+urlserver+"?"+urlParams
                        useBrowser(urlserver+"?"+urlParams)
                        #command='"c:\program files\internet explorer\iexplore" '+urlserver+'?'+urlParams
                        #print "commande URL= ", command
                        #os.system(command)
                    start_new_thread(launch,())
    
            #except:
            if 0:
                print "Had problem while submitting the form"
            
        # set the id variable to id="" again
        idtosend= ""
        print "setting entry fields back to empty"
        entryTitle.SetValue("")
        entryDescription.SetValue("")
        entryLastname.SetValue("")
        entryFirstname.SetValue("")
        if formFormation=="": entryTraining.SetValue("")
        frameEnd.statusBar.SetStatusText("---")
    else:
        print "Pas de publication: pas d'enregistrement effectue"

def rss_warning_client_feed(what=""):
    """
    If a publication problem is encountered this code will attempt to write in an RSS feed on the server when the connection 
    is recovered. This function must be launched in a thread; 
    """    
    global PathData
    
    reporting_time_string=getTime() # time (string) at which the incident has been reported
    reporting_time= time.time() # for seconds computation
    t_span=172800 # total time during which to attempt server notification by RSS update (one day = 86400, 2 days= 172800)
    t_interval=60 # time interval for each try in seconds (1 minute= 60 seconds)
    print "Total time duration during which to attempt server notification (hours) =", str(t_span/3600.0)
    print "Time interval for each try in seconds =",t_interval
    
    def report(what=what):
        # a RSS head head not used for now cause i take the exist RSS file for now
        if what=="": what=" Publishing problem for "+ socket.gethostname()
        rss_head="""<?xml version="1.0"?>
        <rss version="2.0">
        <channel>
        <title>Audiovideocours RSS client warnings reports</title>
        <link></link>
        <description>This feed is updated when an audiovideocours client encounters a problem. </description>"""
        item_new="""<item>
        <title>"""+reporting_time_string+", "+what+"""</title>
        <link>"""+"http://"+socket.gethostname()+"""</link>
        <description>"""+reporting_time_string+", "+what+" IP:"+socket.gethostbyname(socket.gethostname())+"""</description>\n</item>"""
        rss_tail="</channel></rss>"
        # Retrieve RSS feed
        print "Attempting to open FTP connection to server..."
        # Retrieve server feed
        ftp = FTP(ftpUrl)
        ftp.login(ftpLogin, ftpPass)
        ftp.cwd("live") # moving clients-warnings.xml in "live" folder (for security reasons, restraining client FTP reach and still http accessible)
        
        # Checking if feed exists on server
        filelist=[]
        ftp.retrlines('LIST',filelist.append) 
        for f in filelist:
            if "clients-warnings.xml" in f:
                feedExists=True
                break
            else:
                feedExists=False
        
        if feedExists==False:
            print "clients-warnings.xml d'ont exist on the server, creating a new feed"
            content_new= rss_head+"\n"+item_new+"\n"+rss_tail   
        else:
            print "clients-warnings.xml exists on the server, updating this feed"
            gFile=open(pathData+"/clients-warnings.xml","wb")
            ftp.retrbinary('RETR clients-warnings.xml',gFile.write)
            gFile.close()
            # Write new warning item in RSS field
            f=open(pathData+"/clients-warnings.xml","r")
            content_old=f.read()
            #print content_old
            f.close()
            content_head=content_old.split("</description>",1)[0]+"</description>"
            content_body=content_old.split("</description>",1)[1]
            content_new= content_head+"\n"+item_new+content_body
            #print content_new
        # write new file
        f=open(pathData+"/clients-warnings.xml","w")
        f.write(content_new)
        f.close()
        # send file to FTP server
        f=open(pathData+"/clients-warnings.xml","rb")
        ftp.storbinary('STOR '+ "clients-warnings.xml", f) # Send the file
        f.close()
        # Close FTP session
        ftp.close()
         
    if 0: report(what)
    if 1:
        while (time.time()-reporting_time)<t_span:
            try:
                #print "time.time()-reporting_time =", time.time()-reporting_time," t_span =", t_span
                print "Trying to update clients-warnings.xml on FTP server"
                report(what)
                print "Publishing should be ok, no exceptions encountered at publishing"
                break
            except:
                print "Couldn't update clients-warnings.xml on FTP server, going to sleep for", str(t_interval),"seconds"
                time.sleep(t_interval)
                     
def LaunchSocketServer():
    """ 
    Launch a socket server, listen to eventual orders
    and decide what to do 
    """
    global id,recording,mySocket
    print "Client is listening for socket order on port",str(portNumber)
    mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    mySocket.bind ( ( '', portNumber ) )
    mySocket.listen ( 1 )
    while True:
        channel, details = mySocket.accept()
        print 'We have an opened connection with', details
        writeInLogs('- We have an opened connection with '+str(details)+"\n")
        received = channel.recv(100)
        writeInLogs("- received = "+str(received)+"\n")
        if received != "":
            if received=="SHOW_AVC":
                frameBegin.Show()
            if received=="SHUTDOWN_PC" and recording==False:
                os.system("shutdown -s -f")
            if received=="VERSION": 
                channel.send ('v ' + __version__)
            # search for an (id:xxxxx) pattern
            iDbegin1= received.find("(id:")
            iDbegin2= received.find("(title:")
            iDbegin3= received.find("(description:")
            iDend= received.find(")")
            iDrecord= received.find("(order:record)")
            if (iDbegin1 > -1)and (iDend > -1):
                id=received[(iDbegin1+4):iDend]
                print "received ID number ", id 
                if recording==False:
                    channel.send ( 'Received ID' + str(id))
                    windowBack(frameBegin)
                if recording==True:
                    channel.send ( 'Received ID' + str(id)+" !!! already recording !!!")
                    print "Already recording"
                if 0:
                    caption="Message Univ-R Debut"
                    text="Veulliez appuyer sur le bouton audiovideocours\
                    \ndu clavier de commande de la salle."
                    dialog=wx.MessageDialog(None,message=text,caption=caption,
                    style=wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
                    if dialog.ShowModal() == wx.ID_OK:
                        print "user clicked on OK in the Univ-r dialog"
                    else:
                        print "user canceled the Univ-R dialg"
                        print "putting id back to empty"
                        id=""
            if (iDbegin2 > -1)and (iDend > -1):
                title=received[(iDbegin2+6):iDend]
                print "received title ", title
            if (iDbegin3 > -1)and (iDend > -1):
                description=received[(iDbegin3+12):iDend]
                print "received description ", description
            if (iDrecord>-1):
                print "Reading now ..."
                recordNow()
        channel.close()
        
def windowBack(frame,windowTitle="Attention"):
    """
    Show the frame back in wiew
    """
    global tryFocus, recording
    print "windowTitle target= ", windowTitle
    tryFocus=True
    frame.Show()
    #time.sleep(0.5)
    frame.Show()
    def comeBack():
        print "-",
        appAuto = application.Application()
        #appAuto.connect_(handle = findwindows.find_windows(title = "Attention")[0])
        appAuto.connect_(handle = findwindows.find_windows(title = windowTitle)[0])
        appAuto.Attention.SetFocus()
        appAuto.Attention.Restore()
    for i in range(5):
        #print "Try set focus"
        try:
            comeBack()
            time.sleep(0.1)
        except:
            pass

    tryFocus=False
def setupHooks():
    """
    Setup hooks
    """
    hm = pyHook.HookManager ()  # create a hook manager
    hm.KeyDown = OnKeyboardEvent # watch for keyoard events
    #hm.MouseAll = OnMouseEvent # watch for all mouse events
    hm.MouseLeftDown = OnMouseEvent
    hm.MouseWheel= OnMouseEvent
    hm.HookKeyboard() # set the hook
    hm.HookMouse() # set the hook
    
def writeInLogs(what):   
    """
    Write events in a configuration file (one per month)
    """
    global logFile,pathData
    yearMonth=str(datetime.datetime.now())
    yearMonth=yearMonth[:7]
    #logFile = open ("log-"+yearMonth+".txt","a")
    logFile = open (pathData+"/log-audiovideocours-"+yearMonth+".txt","a")
    #logFile = open (os.environ["USERPROFILE"]+"/audiovideocours/log-audiovideocours-"+yearMonth+".txt","a")
    logFile.write(what)
    logFile.close()
def writeStack():
    """
    Write current exception stack with date stamp in the data folder for futher analysis (file: errlog.txt)
    """
    f=open(pathData+"/errlog.txt","a")
    f.write("\n"+str(datetime.datetime.now())+"\n")
    f.close()
    traceback.print_exc(file=open(pathData+"/errlog.txt","a"))
    
def kill_if_double():
    """ 
    Kill an eventual running instance of mediacours.exe
    """
    try:
        print "Trying to kill an eventual running instance of mediacours.exe."
        PID_f=open(os.environ["USERPROFILE"]+"\\PID_mediacours.txt",'r')
        PID=PID_f.readline()
        #print "PID of mediacours is ",PID
        #print "Killing PID ",PID
        os.popen("tskill "+PID)
    except:
        print "Passed kill_if_double"

def shutdownPC_if_noactivity():
    """ 
    This function must reside in a thread and be launched at startup
    """
    global lastGlobalEvent # lat time event given by the KB and mouse hooks
    tempoCheck=5 # time interval in seconds for each check
    noactivityMax=30 # time threshold in seconds over which the the PC will ... 
    #... shutdown if no activity is present 
    while 1:
        print "*",
        time.sleep(tempoCheck)
        if ((time.time()-lastGlobalEvent)>noactivityMax) and (recording==False):
            print "No activity over "+str(noactivityMax)+" s => shutdown the PC"
            #os.system("shutdown -s -f")
            print 'would do: os.system("shutdown -s -f")'
            
def htmlGen():
    """ Genereate html version for playback"""
    global workDirectory, usage
        
    f=open(workDirectory+"/timecode.csv")
    diaTime=f.read().split("\n")[:-2]
    f.close()
    diaArray="("
    for d in diaTime:
        diaArray+= d+","
    diaArray=diaArray[:-1]+")"
    if usage=="audio":
        media="enregistrement-micro.mp3"
        playerHeight="20"
        delayMediaSlides=0
    else:
        media="../enregistrement-video.flv"
        playerHeight="250"
        delayMediaSlides=-3
    title=workDirectory.split("\\")[-1]
    
    htmlVars="// --- Variable generated from script\n// timecode of slides for this recording\n"\
    +"var timecode=new Array"+diaArray+";\n"\
    +"var media='"+media+"';\nvar playerHeight='"+playerHeight+"';//Give height='20' for audio and '200' for video\n"\
    +"var title='"+title+"';\n"+"// ---"
            
    file=open(workDirectory+"/recording.html",'w')
    file.write(htmlBits.head)
    file.write(htmlVars)
    file.write(htmlBits.tail(delayMediaSlides=delayMediaSlides))
    file.close()
    
    ## copy third party script in a "thirdparty" folder
    os.mkdir(workDirectory+"\\thirdparty")
    shutil.copyfile("thirdparty\\player.swf",workDirectory+"\\thirdparty\\player.swf")
    shutil.copyfile("thirdparty\\swfobject.js",workDirectory+"\\thirdparty\\swfobject.js")
    #shutil.copyfile("thirdparty\\JSFX_ImageZoom.js",workDirectory+"\\thirdparty\\JSFX_ImageZoom.js")
    shutil.copyfile("thirdparty\\README.txt",workDirectory+"\\thirdparty\\README.txt")
                  
def useBrowser(what=""):
    """ Defining the browser to use for 'what' content"""
    print "In useBrowser function"
    if 1:
        webbrowser.open_new(what)
    if 0:
        if os.path.isfile("c:/program files (x86)/internet explorer/iexplore.exe") == True:
            print "useBrowser =","c:/program files (x86)/internet explorer/iexplore.exe"
            useBrowser='"c:/program files (x86)/internet explorer/iexplore.exe"'
        else:
            print "useBrowser =","c:/program files/internet explorer/iexplore.exe"
            useBrowser='"c:/program files/internet explorer/iexplore.exe"'
        subprocess.Popen(useBrowser+" "+what) # console should be hidden    
        #os.system(useBrowser+" "+what)

#################################################################################################################

class SerialHook:
    """
     A driver (soft hook) to an optional RS-232 keyboard used for amphi automation
    """
    def __init__(self):
        """ Open the serial port and initialize the serial keyboard"""
        print "Opening the serial port of the serial keyboard"
        self.ser = serial.Serial(int(keyboardPort))
        print "Setting DTR to level 1 : +12 Volts"
        self.ser.setDTR(level=1)  #set DTR line to specified logic level
        self.kb1=self.ser.getCD()
        print "Initial kb1= ",self.kb1
        self.kb2=self.ser.getDSR()
        print "Initial kb2= ",self.kb2
        self.kb3=self.ser.getCTS()
        print "Initial kb3= ",self.kb3
        self.kb4=self.ser.getRI()
        print "Initial kb4= ",self.kb4
        
    def listen(self,delta=0.001):
        """ Reads the state of the Kb at each delta """
        print "Entering listen loop ..."
        while 1:
            if (self.ser.getCD()!=self.kb1) and (self.ser.getCD()==True):
                self.kb1=True
                print "kb1 True"
                windowBack(frameBegin)
            if (self.ser.getCD()!=self.kb1) and (self.ser.getCD()==False):
                self.kb1=False
                print "kb1 False"
                if recording== True:
                    print "id:",id,"(optional id for this recording)"
                    if id=="":
                        windowBack(frameEnd)
                        recordStop()
                    else:
                        recordStop()
                        frameUnivr.Show()
                if recording==False:
                    frameBegin.Hide()
            if (self.ser.getDSR()!=self.kb2) and (self.ser.getDSR()==True):
                self.kb2=True
                print "kb2 True"
            if (self.ser.getDSR()!=self.kb2) and (self.ser.getDSR()==False):
                self.kb2=False
                print "kb2 False"
            if (self.ser.getCTS()!=self.kb3) and (self.ser.getCTS()==True):
                self.kb3=True
                print "kb3 True"
                if  videoprojectorInstalled==True:
                    videoprojector.projOn()
                    print "Send order: videoprojector ON"
            if (self.ser.getCTS()!=self.kb3) and (self.ser.getCTS()==False):
                self.kb3=False
                print "kb3 False"
            if (self.ser.getRI()!=self.kb4) and (self.ser.getRI()==True):
                self.kb4=True
                print "kb4 True"
                if  videoprojectorInstalled==True:
                    videoprojector.projOff()
                    print "Send order: videoprojector OFF"
            if (self.ser.getRI()!=self.kb4) and (self.ser.getRI()==False):
                self.kb4=False
                print "kb4 False"
            time.sleep(delta)
class AMX:
    """ 
    A class to read the optional 'capture ON/OFF' orders from the AMX
    keyboard in many UDS amphitheatres and start the recording through it.
    """
    def __init__(self):
        self.ser = serial.Serial(int(keyboardPort))
        print "AMX keyboard init"
    def listen(self,frameEnd, frameBegin, tryFocus):
        """ Listen to the AMX keyboard and decide what to do."""
        while 1:
            time.sleep(0.3)
            inWaiting= self.ser.inWaiting()
            if inWaiting>= 4:
                print "inWaiting =", inWaiting
                readBuffer= self.ser.read(inWaiting)
                print readBuffer
                if readBuffer == "START":
                    screenshot()
                    if recording==False and tryFocus==False:
                        windowBack(frameBegin)
                if readBuffer == "STOP":
                    screenshot()
                    if recording==True and tryFocus==False:
                        windowBack(frameEnd)
                        recordStop()            
    
class Videoprojector:
    """ 
    A class to control a videoprojector through RS232
     """
    def __init__(self):
        """ Open the serial port of the videoprojector"""
        print "Initiating videoprojector object..."
        #print "Opening serial port of the videoprojector"
        #self.ser = serial.Serial(videoprojectorPort)
    def projOn(self):
        """Send the 'switch on' command to the videoprojector"""
        self.ser = serial.Serial(videoprojectorPort)
        self.ser.write(videoProjON)
        self.ser.close()
        print "- sending "+videoProjON+" to port com "+str(videoprojectorPort)
    def projOff(self):
        """Send the 'switch off' command to the videoprojector"""
        self.ser = serial.Serial(videoprojectorPort)
        self.ser.write(videoProjOFF)
        self.ser.close()
        print "- sending "+videoProjOFF+" to port com "+str(videoprojectorPort)

class SmilGen:
    """ 
    A class to produce a SMIL file on the fly 
    """
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
        When screenshot occure => writting the event in the SMIL
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

class BeginFrame(wx.Frame):
    """
    A begining frame to warn the user he will begin to record
    """
    def __init__(self, parent, title):
        global liveFeed
        #self.usage="audio"
        self.usage=usage
        """Create the warning window"""
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(500, 400),
        style=wx.DEFAULT_FRAME_STYLE ^ (wx.CLOSE_BOX|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))
        
        favicon = wx.Icon('images/audiocours1.ico', wx.BITMAP_TYPE_ICO, 16, 16)
        statusMessage= " AudioVideoCast Version "+__version__
        self.statusBar=self.CreateStatusBar()
        self.statusBar.SetStatusText(statusMessage)
        wx.Frame.SetIcon(self, favicon)

        panel=wx.Panel(self)
        panel.SetBackgroundColour("white") 
        
        if standalone==True:
            menubar=wx.MenuBar()
            menuInformation=wx.Menu()
            menubar.Append(menuInformation,"Informations")
            help=menuInformation.Append(wx.NewId(),_("Help"))
            conf=menuInformation.Append(wx.NewId(),_("Configuration"))
            cutTool=menuInformation.Append(wx.NewId(),"Outil decoupe")
            version=menuInformation.Append(wx.NewId(),"Version")
            
            self.Bind(wx.EVT_MENU,self.help,help)
            self.Bind(wx.EVT_MENU,self.about,version)
            self.Bind(wx.EVT_MENU,self.cutAVCtool,cutTool)
            self.Bind(wx.EVT_MENU,self.configuration,conf)
            #self.SetMenuBar          
        if audioVideoChoice==True:
            radio1=wx.RadioButton(panel,-1,"audio")
            radio2=wx.RadioButton(panel,-1,"video")
            if usage=="screencast" or screencastChoice==True:
                radio3=wx.RadioButton(panel,-1,"screencast")
            if usage=="video":
                radio2.SetValue(True)
            if usage=="audio":
                radio1.SetValue(True)
            if usage=="screencast":
                radio3.SetValue(True)    
            def onRadio(evt):
                radioSelected=evt.GetEventObject()
                self.usage=radioSelected.GetLabel()
                print "Usage selected (audio or video or screencast):",self.usage
            self.Bind(wx.EVT_RADIOBUTTON ,onRadio,radio1)
            self.Bind(wx.EVT_RADIOBUTTON ,onRadio,radio2)
            if usage=="screencast" or screencastChoice==True:
                self.Bind(wx.EVT_RADIOBUTTON ,onRadio,radio3)
            
        im1 = wx.Image('images/ban1.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        text1="\n\t"+\
        _("By pressing the  ' Record ! '  button, the  recording will  ")+"\n\t"+\
        _("begin immediately and this window will disappear. ")
        if serialKeyboard==False:
            text1=text1+"\n\n\t"+\
            _("To stop the recording press the following key:   ")+stopKey+\
            ".   "
        text = wx.StaticText(panel, -1,  text1,size=(420,100),style=wx.LEFT)
        text.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL,wx.NORMAL, False,"MS Sans Serif"))
        text.SetBackgroundColour("steel blue") 
        text.SetForegroundColour("white")
        if 0: # for dev, what fonts are available on the system
            e=wx.FontEnumerator()
            e.EnumerateFacenames()
            fontList=e.GetFacenames()
            print fontList
        if  liveCheckBox==True:
            liveFeed=wx.CheckBox(panel,-1,_("Live streaming"),)
        btnRecord = wx.Button(parent=panel, id=-1, label=_("Record!"),size=(200,50))
        if standalone == True:
            btnNext = wx.Button(parent=panel, id=-1, label=_("Other choices"),size=(100,50))
            btnQuit = wx.Button(parent=panel, id=-1, label=_("Quit"),size=(100,50))
        sizerV = wx.BoxSizer(wx.VERTICAL)
        sizerH=wx.BoxSizer()
        sizerV.Add(wx.StaticBitmap(panel, -1, im1, (5, 5)), 0, wx.ALIGN_CENTER|wx.ALL, 0)
        sizerV.Add(text, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        if audioVideoChoice==True:
            sizerH2=wx.BoxSizer()
            sizerH2.Add(radio1,proportion=0,flag=wx.ALIGN_CENTER|wx.ALL,border=2)
            sizerH2.Add(radio2,proportion=0,flag=wx.ALIGN_CENTER|wx.ALL,border=2)
            if usage=="screencast" or screencastChoice==True:
                sizerH2.Add(radio3,proportion=0,flag=wx.ALIGN_CENTER|wx.ALL,border=2)
            sizerV.Add(sizerH2, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        if  liveCheckBox==True:
            sizerV.Add(liveFeed, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        sizerV.Add(sizerH, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizerH.Add(btnRecord, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        if standalone == True:
            sizerH.Add(btnNext, 0, wx.ALIGN_CENTER|wx.ALL, 10)
            sizerH.Add(btnQuit, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        panel.SetSizer(sizerV)
        panel.Layout() 
        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.engageRecording, btnRecord)
        if standalone == True:
            self.Bind(wx.EVT_BUTTON, self.SkiptoEndingFrame, btnNext)
            self.Bind(wx.EVT_BUTTON, self.exitApp, btnQuit)
        if standalone==True:
            self.SetMenuBar(menubar)
    
    def about(self,evt): 
        """An about message dialog"""
        text="AudioVideoCast version "+__version__+"  \n\n"\
        +_("Website:")+"\n\n"+\
        "http://audiovideocast.unistra.fr/"+"\n\n"\
        +"(c) UDS 2006-2013"
        dialog=wx.MessageDialog(self,message=text,
        style=wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
        dialog.ShowModal()
        
    def cutAVCtool(self,evt):
        """A tool to cut in AudioCours types recording """
        print "a tool to cut in avc recordings"
        frameCut=cutToolFrame(None,title="Outil cut")
    
    def help(self,evt):
        """ A function to provide help on how to use the software"""
        global pathData
        def launch():
            print "I'm in launch in help"
            try:
                useBrowser(what="http://audiovideocast.unistra.fr/avc/home")
                #subprocess.Popen([r'C:\Program Files\Internet Explorer\iexplore.exe',os.environ["USERPROFILE"]+"/audiovideocours/Aide_AudioCours_StandAlone.url"])
            except:
                print "Couldn't open or find Aide_AudioCours_StandAlone.url"
        start_new_thread(launch,())
    
    def configuration(self,evt):
        """ A fucntion to open the configuration file"""
        def launch():
            subprocess.Popen([r'C:\Windows\System32\notepad.exe',
                              os.environ["ALLUSERSPROFILE"]+"\\audiovideocours\\mediacours.conf"])
        start_new_thread(launch,())
        
    def exitApp(self,evt):
        """A function to quit the app"""
        print "exit"
        print "trying to close an eventual opened socket"
        try:
            mySocket.close()
        except:
            pass
        sys.exit()
        
    def SkiptoEndingFrame(self,evt):
        """Skip to Ending frame without recording"""
        frameBegin.Hide()
        frameEnd.Show()
        
    def engageRecording(self,evt):
        """Confirms and engage recording"""
        global live
        if  liveCheckBox==True:
            live=liveFeed.GetValue()
        if tryFocus==False:
            start_new_thread(recordNow,())
            self.Hide()

class EndingFrame(wx.Frame):
    """
    An ending frame which also enable to publish the recordings on a webserver
    """
    def __init__(self, parent, title):
        """Create the ending frame"""
        global entryTitle,entryDescription,entryTraining,entryLastname,entryFirstname,entryCode,btnPublish\
        ,btnCancel,loginENT,emailENT,entryLoginENT,entryLoginENT,entryEmail,textWeb,dirName,workDirectory
        windowXsize=500
        windowYsize=650
        fieldSize=420
        if standalone==True:
            windowXsize=500
            fieldSize=420  
        if publishingForm==False:
            windowYsize=250    
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(windowXsize, windowYsize),
            style=wx.DEFAULT_FRAME_STYLE ^ (wx.CLOSE_BOX|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))            
        favicon = wx.Icon('images/audiocours1.ico', wx.BITMAP_TYPE_ICO, 16, 16)
        wx.Frame.SetIcon(self, favicon)
        # Status bar
        self.statusBar=self.CreateStatusBar()
        self.statusBar.SetStatusText(_("Status bar"))
        panel=wx.Panel(self)
        #panel.SetBackgroundColour((244,180,56))
        panel.SetBackgroundColour("steel blue") 
        logos = wx.Image('images/ban1.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        textTitle = wx.StaticText(panel, -1, _("Title:"),size=(400,-1),style=wx.ALIGN_CENTER)
        entryTitle = wx.TextCtrl(panel, -1,"", size=(fieldSize, -1))
        textDescription = wx.StaticText(panel, -1, _("Eventual description:"),
        size=(400,-1),style=wx.ALIGN_CENTER)
        entryDescription = wx.TextCtrl(panel, -1,"", size=(fieldSize, -1))
        textLastname= wx.StaticText(panel, -1, _("Name:"),size=(400,-1),style=wx.ALIGN_CENTER)
        entryLastname = wx.TextCtrl(panel, -1,"", size=(fieldSize, -1))
        textFirstname= wx.StaticText(panel, -1, _("First name:"),size=(400,-1),style=wx.ALIGN_CENTER)
        entryFirstname = wx.TextCtrl(panel, -1,"", size=(fieldSize, -1))
        textTraining = wx.StaticText(panel, -1, _("Degree:"),size=(400,-1),style=wx.ALIGN_CENTER)
        entryTraining = wx.TextCtrl(panel,-1,"", size=(fieldSize, -1))
        entryTraining.SetValue(formFormation)
        textLoginENT=wx.StaticText(panel,-1, _("Identifiant ENT UDS:"),size=(400,-1),style=wx.ALIGN_CENTER)
        entryLoginENT = wx.TextCtrl(panel,-1,"", size=(fieldSize, -1))
        textEmail=wx.StaticText(panel,-1, _("Email :"),size=(400,-1),style=wx.ALIGN_CENTER)
        entryEmail = wx.TextCtrl(panel,-1,"", size=(fieldSize, -1))
        textCode=wx.StaticText(panel,-1, _("Access Code if you wish to set a limited access:"),
        size=(400,-1),style=wx.ALIGN_CENTER)
        entryCode = wx.TextCtrl(panel,-1,"", size=(fieldSize, -1))
        linkWebsite=hl.HyperLinkCtrl(panel, wx.ID_ANY, (_("Access to")+" audiovideocours.u-strasbg.fr"),
        URL="http://audiovideocours.u-strasbg.fr/",size=(300,-1),style=wx.ALIGN_CENTER)
        linkWebsite.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL,wx.NORMAL, False,'Arial'))
        linkWebsite.SetForegroundColour("white")
        linkWebsite.SetColours("white", "white", "white")
        textWeb=wx.StaticText(panel,-1, _("Pour publier sur le serveur, cliquez sur 'Publier' et remplissez \nle formulaire dans le navigateur qui se lancera."),size=(400,-1),style=wx.ALIGN_CENTER)
        textWeb.SetForegroundColour("white")
            
        for label in [textTitle,textDescription,textLastname,textFirstname,textTraining,textCode,
                      textLoginENT,textEmail]:
            label.SetForegroundColour("white")
            label.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL,wx.BOLD, False,"MS Sans Serif"))
        """
        for entry in [entryTitle,entryDescription,entryLastname,entryFirstname,entryTraining,entryCode]:
            #entry.SetBackgroundColour((254,236,170))
            #entry.SetBackgroundColour("light blue")
            pass
        """
        btnPublish = wx.Button(panel, -1, _("Publish!"),size=(130,50))
        btnCancel=wx.Button(panel, -1, _("Cancel"),size=(70,50))
        
        if standalone==True :
            btnPreview=wx.Button(panel, -1, _("Read"),size=(70,50))
            btnQuit=wx.Button(panel,-1,_("Quit"),size=(70,50))
            btnOpen=wx.Button(panel,-1,_("Open"),size=(70,50))
            
        hbox=wx.BoxSizer()
        hbox.Add(btnPublish,proportion=0,flag=wx.RIGHT,border=5)
        hbox.Add(btnCancel,proportion=0,flag=wx.RIGHT,border=5)
        
        if standalone==True :
            hbox.Add(btnPreview,proportion=0,flag=wx.RIGHT,border=5)
            hbox.Add(btnOpen,proportion=0,flag=wx.RIGHT,border=5)
            hbox.Add(btnQuit,proportion=0,flag=wx.RIGHT,border=5)
        pad1=4    
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticBitmap(panel, -1, logos, (5, 5)), 0, wx.ALIGN_CENTER|wx.ALL, 0)
        
        if publishingForm==True:
            sizer.Add(textTitle, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(entryTitle, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(textDescription, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(entryDescription, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(textLastname, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(entryLastname, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(textFirstname, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(entryFirstname, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(textTraining, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(entryTraining, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(textCode, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(entryCode, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(textLoginENT, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(entryLoginENT, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(textEmail, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
            sizer.Add(entryEmail, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        if publishingForm==False:
            for entry in [entryTitle,entryDescription,entryLastname,entryFirstname,entryTraining,entryCode,entryLoginENT,entryEmail]:
                entry.Hide()    
        sizer.Add(hbox, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        if publishingForm==True:
            sizer.Add(linkWebsite, 0, wx.ALIGN_CENTER|wx.ALL, 4)
        if publishingForm==False:
            sizer.Add(textWeb, 0, wx.ALIGN_CENTER|wx.ALL, 4)
        
        panel.SetSizer(sizer)
        panel.Layout() # what for ?
        
        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.publish, btnPublish)
        self.Bind(wx.EVT_BUTTON, self.exitPublish, btnCancel)
        
        if standalone==True :
            self.Bind(wx.EVT_BUTTON, self.readPreview, btnPreview)
            self.Bind(wx.EVT_BUTTON, self.exitApp, btnQuit)
            self.Bind(wx.EVT_BUTTON, self.openOldOne, btnOpen)
            
    def openOldOne(self,evt):
        """
        Open an old recording for latter playing or publishing
        """
        global workDirectory,dirName,previewPlayer
        selectPreview=wx.FileDialog(self)
        print "pathData=",pathData
        if pathData=="":
            pathData==os.getcwd()
        selectPreview.SetDirectory(pathData)
        if previewPlayer=="realplayer":
            print "Showing smil file for selection"
            selectPreview.SetWildcard("*.smil")
        else:
            print "Showing html file for selection"
            selectPreview.SetWildcard("*.html")
        selectPreview.ShowModal()
        toPlay= selectPreview.GetFilenames()
        dirName=os.path.basename(selectPreview.GetDirectory())
        print "dirName=",dirName
        workDirectory=selectPreview.GetDirectory()
    
        frameEnd.statusBar.SetStatusText(_("Current recording ")+workDirectory)
        if len(toPlay)>0:
            self.readPreview(self)
        print workDirectory
        
    def exitApp(self,evt):
        """A function to quit the app"""
        print "exit"
        sys.exit()
        
    def exitPublish(self,evt):
        """Don't publich the recordings on the webserver"""
        global dirNameToPublish, workDirectoryToPublish
        writeInLogs("- 'Cancel' button pressed at"+ \
        str(datetime.datetime.now())+"\n")
        folder="canceled"
        if tryFocus==False:
            self.Hide()
            if standalone == True:
                frameBegin.Show()
        if standalone==False:
            global entryTitle,entryDescription,entryTraining,entryLastname,entryFirstname
            global title,description,firstname,name,ue,login,loginENT,emailENT
            title= entryTitle.GetValue()
            description=entryDescription.GetValue()
            name=entryLastname.GetValue()
            firstname=entryFirstname.GetValue()
            ue=entryTraining.GetValue()
            genre=entryCode.GetValue()
            loginENT=entryLoginENT.GetValue()
            emailENT=entryEmail.GetValue()
            #login=entry3.GetValue()
            print "tile: ",title
            print "description: ",description
            print "name: ",name
            print "ue: ",ue
            print "prenom: ",firstname
            print "Creating .zip file..."
            createZip()      
            print "Zip file created" 
            
            workDirectoryToPublish=workDirectory
            dirNameToPublish=dirName
            start_new_thread(confirmPublish,(folder,))
            
        entryTitle.SetValue("")
        entryDescription.SetValue("")
        entryLastname.SetValue("")
        entryFirstname.SetValue("")
        entryLoginENT.SetValue("")
        entryEmail.SetValue("")
        if formFormation=="": entryTraining.SetValue("")

    def readPreview(self,evt):
        """Read the smil 'recording' file (audio or video + screenshots)"""
        def readSmilNow():
            if dirName =="":
                frameEnd.statusBar.SetStatusText(_("Nothing to read."))
            if workDirectory!="":
                #os.system("realplay.exe file://"+workDirectory+"/cours.smil") #also works
                try:
                    subprocess.Popen(["realplay.exe", "file://"+workDirectory+"/cours.smil"])
                except:
                    try:
                        # try to search for the common full path of realplay.exe
                        realplay="C:\\Program"+" "+"Files\\Real\\RealPlayer\\realplay.exe"
                        subprocess.Popen([realplay, "file://"+workDirectory+"/cours.smil"])
                    except:
                        caption="Audiovideocours Error Message"
                        text="RealPlayer software not found"
                        dialog=wx.MessageDialog(None,message=text,caption=caption,
                        style=wx.OK|wx.ICON_INFORMATION)
                        dialog.ShowModal()
        def readLocalWebPreview():
            """ Read a local web preview of the recording using the integrated cherrypy server"""
            if dirName =="":
                frameEnd.statusBar.SetStatusText(_("Nothing to read."))
            if workDirectory!="":
                print "Attempting to read web preview"
                useBrowser("http://localhost:"+str(remotePort)+"/"+dirName+"/recording.html")
                        
        if previewPlayer=="realplayer":
            start_new_thread(readSmilNow,())
        else:
            start_new_thread(readLocalWebPreview,())
        
    def publish(self,evt):
        """Publish the recording on the website"""
        global workDirectoryToPublish, dirNameToPublish,loginENT,emailENT
        writeInLogs("- 'Publish' button pressed at"+ \
        str(datetime.datetime.now())+"\n")
        workDirectoryToPublish=workDirectory
        dirNameToPublish=dirName
        print "dirNameToPublish =",dirNameToPublish
        print "workDirectoryToPublish =",workDirectoryToPublish
        if tryFocus==False:
            global title,description,name,firstname, ue,genre
            title= entryTitle.GetValue()
            description=entryDescription.GetValue()
            name=entryLastname.GetValue()
            firstname=entryFirstname.GetValue()
            ue=entryTraining.GetValue()
            genre=entryCode.GetValue()
            loginENT=entryLoginENT.GetValue()
            emailENT=entryEmail.GetValue()
            print "tile : ",title
            print "description: ",description
            print "name: ",name
            print "prenom: ",firstname
            print "ue: ",ue
            print "login ENT",loginENT
            print "email ENT",emailENT
            entryTitle.SetValue("")
            entryDescription.SetValue("")
            entryLastname.SetValue("")
            entryFirstname.SetValue("")
            entryCode.SetValue("")
            entryLoginENT.SetValue("")
            entryEmail.SetValue("")
            if formFormation=="": entryTraining.SetValue("")
            print "Creating .zip file..."
            btnPublish.Enable(False)
            btnCancel.Enable(False)
            try:
                createZip()
            except:
                print "Warning! couldn't create zip file!"      
            print "If no above warning, Zip file created" 
            btnPublish.Enable(True)
            btnCancel.Enable(True)
            if standalone !=True:
                self.Hide()
            start_new_thread(confirmPublish,())

class univrEndFrame(wx.Frame):
    """
    Optional: used when receiving an external order to stop a recording (from server)
    """
    def __init__(self, parent, title):
        global liveFeed
        """Create the warning window"""        
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(300,110),
        style=wx.DEFAULT_FRAME_STYLE)
        panel=wx.Panel(self)
        #panel.SetBackgroundColour("white") 
        text = wx.StaticText(panel, -1, "Enregistrement transmis pour Univ-r\net audiovideocours.u-strasbg.fr")  
        okButton=wx.Button(panel,size=(-1,-1),label="Fermer")
        self.Bind(wx.EVT_BUTTON, self.hideNow,okButton)
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(text,proportion=0,flag=wx.ALIGN_CENTER|wx.ALL,border=5)
        vbox.Add(okButton,proportion=0,flag=wx.ALIGN_CENTER|wx.ALL,border=5) 
        panel.SetSizer(vbox) 
        
    def hideNow(self,evt):
        """ Hide window"""
        self.Hide()
    
def onEndSession(evt):
    import winsound
    winsound.PlaySound("waves\\exit.wav",winsound.SND_FILENAME)
    writeInLogs("!!! RED ALERT: Windows Session is ending at "+ str(datetime.datetime.now())+" launching emergency procedures...")
            
class AVCremote:
    global welcome, pathData,recording

    def index(self):
        global welcome
        welcome="<p> ((( AudioVideoCast Client - Web Interface ))) </p> "
        welcome+="Recording now: "+str(recording)+" <br><br>"
        welcome+= "> client version : "+__version__+"</br>"
        welcome+= "> app_startup_date : "+app_startup_date+"</br>"
        welcome+= "> last_session_recording_start : "+last_session_recording_start+"</br>"
        welcome+= "> last_session_recording_stop : "+last_session_recording_stop+"</br>"
        welcome+= "> last_session_publish_order : "+last_session_publish_order+"</br>"
        welcome+= "> last_session_publish_problem : "+last_session_publish_problem+"</br>"
        welcome+= "> session data folder : "+pathData+"</br>"
        welcome+="<br><br><br>"
        # Ask for an order
        return welcome+'''
            <form action="getOrder" method="GET">
            Command : 
            <input type="text" name="order" size="50" />
            <input type="submit" />
            </form>'''
    index.exposed = True
    
    def getOrder(self, order = None):

        if order:
            print "received order:", order   
            if order=="list":
                print "trying to retrieve list for pathData", pathData
                return fileList(folderPath=pathData)[0]
            elif order=="help":
                helpList="""
                <p>Current available commands:</p>
                 
                help -> returns a list of available commands.<br>
                list -> returns a list of folders and files in your current data folder.<br>
                recover:NameOfFolder -> FTP folder to FTP server. <br>
                start -> start recording if not already recording. COMING SOON.<br>
                stop -> Stop recording if recording currently. COMING SOON.<br>
                """
                return helpList
            elif order.find("recover:")>=0:
                print "Attempting to recover an old recording folder..."
                fileOrFolder=order.split("recover:")[1].strip()
                recoverFeedback=recoverFileOrFolder(name=fileOrFolder, pathData=pathData, ftpUrl=ftpUrl, ftpLogin=ftpLogin, ftpPass=ftpPass)
                return recoverFeedback
            elif order=="start":
                print "will start recording if not already recording"
            elif order=="stop":
                print "will stop recording if recording currently"
            elif order.find("recover-f:")==True:
                print "will do later"
            else:
                return welcome+"You have order: %s " % order
        else:
            if order is None:
                # No name was specified
                return 'Please enter your order <a href="./">here</a>.'
            else:
                return 'No, really, enter your order <a href="./">here</a>.'
    getOrder.exposed = True

def goAVCremote(remPort=remotePort,pathData=pathData,hosts="127.0.0.1"):
    "Create an instance of AVCremote"
    print "Launch AVCremote thread"
    global traceback,remotePort

    cherrypy.config.update({'server.socket_host': hosts,
                        'server.socket_port': remPort, 
                        'tools.staticdir.on': True,
                        #'tools.staticdir.dir': "C:\\",
                        'tools.staticdir.dir': pathData,
                       })
    try:
        cherrypy.quickstart(AVCremote())
    except:
         # My attempt to relaunch with another port number fail for now 
        # => display a dialog box to users in the meantime
        dialog=wx.MessageDialog(None,message="[French] Attention, le port 80 ou 8081 est deja occupe (Skype, serveur?), la lecture avant publication ne sera pas possible.\n\
        Arretez l'application utilisant ce port ou changez le numero de port dans le fichier de configuration.\n\n[English] Warning, port 80 or 8081 is already used (Skype? server?), preview reading before publication won't be possible.\nStop the application using this port or change port number in configuration file",
                                caption="Port 80 ou 8081 non disponible, Port 80 or 8081 busy", style=wx.OK|wx.ICON_INFORMATION)
        dialog.ShowModal()
        print "!!! Couldn't launch integrated server at port "+str(remPort)+"!!!"
        writeInLogs("\nCouldn't launch integrated server at port "+str(remPort)+"!!!")      
        writeStack()
        writeInLogs("\nAttempting to launch server on redirected port 8080 now ")
       
        """
        if 1:
            time.sleep(5)
            print "Trying port 8081 now..."
            cherrypy.config.update({'server.socket_host': hosts,
                        'server.socket_port': 8081, 
                        'tools.staticdir.on': True,
                        #'tools.staticdir.dir': "C:\\",
                        'tools.staticdir.dir': pathData,
                       })
            remotePort=8081
            remPort=remotePort
            cherrypy.quickstart(AVCremote())
        if 0:
            print "!!! Couldn't launch integrated server at redirected 8080 port either !!!"
            writeInLogs("\nCouldn't launch integrated server at redirected 8080 port either")
            writeStack()
           """ 
def fileList(folderPath="."):
    "return a list of the files in the data folder"
    print "In def fileList folderPath=", folderPath
    def get_dir_size(folder):
        size = 0
        for path, dirs, files in os.walk(folder):
            for f in files:
                size +=  os.path.getsize( os.path.join( path, f ) )
        return str(   round((float(size)/(1024*1024)),2)   )+" Mo"
    content= os.listdir(folderPath)
    #print "Content list", content
    files_list =[]
    dirs_list=[]
    for i in content:
        if os.path.isfile(folderPath+"/"+i) == True:
            files_list.append(i)
            print os.path.getsize(folderPath+"/"+i)
        elif os.path.isdir(folderPath+"/"+i) == True:
            dirs_list.append(i)    
            print os.path.getsize(folderPath+"/"+i)
    answer="<p>Listing of files and folders in "+folderPath+" </p>"
    answer+="<p>Files:</p>"
    print "Files list",files_list
    print "Folders list", dirs_list
    for index,name in enumerate(files_list):
        size=os.path.getsize(folderPath+"/"+name)
        answer+=str(index)+" - "+name+" - "+str(round(float(size)/1024,2))+" Ko <br>"
    answer+="<p>Folders:</p>"    
    for index,name in enumerate(dirs_list):
        answer+=str(index)+" - "+name+" - "+get_dir_size(folderPath+"/"+name)+"<br>"
    print answer
    return [answer,files_list,dirs_list]

def getTime():
    "Returns current date/time in an appropriate string format"
    time= str(datetime.datetime.now())[:-7]
    return time 

def recoverFileOrFolder(name,pathData, ftpUrl,ftpLogin,ftpPass):
    "Recovering an folder back to the FTP server usualy following a remote order"
    
    if os.path.isdir(pathData+"/"+name):
        print "Creating Zip file of ...",name
        workDirectory=pathData+"/"+name
        zip = zipfile.ZipFile(pathData+"\\"+name+".zip", 'w')
        for fileName in os.listdir ( workDirectory ):
            if os.path.isfile (workDirectory+"\\"+fileName):
                zip.write(workDirectory+"\\"+fileName,
                name+"/"+fileName,zipfile.ZIP_DEFLATED)
        for fileName in os.listdir ( workDirectory+"\\screenshots"):
            zip.write(workDirectory+"\\screenshots\\"+fileName,
                name+"/"+"screenshots\\"+fileName,zipfile.ZIP_DEFLATED)
        zip.close()
        #writeInLogs("In recoverFolder, counldn't create ZIP file") 
        print "Opening FTP connection..."
        ftp = FTP(ftpUrl)
        ftp.login(ftpLogin, ftpPass)
        f = open(workDirectory+".zip",'rb') 
        ftp.storbinary('STOR '+ name+".zip", f)
        f.close() 
        ftp.quit()
        print "FTP closed."    
        result="Folder "+name+" zipped and transfered through FTP to the FTP server."
        return result 
    elif os.path.isfile(pathData+"/"+name):
        ftp = FTP(ftpUrl)
        ftp.login(ftpLogin, ftpPass)
        f = open(pathData+"/"+name,'rb') 
        ftp.storbinary('STOR '+ name, f)
        f.close() 
        ftp.quit()
        print "FTP closed."    
        result="File "+name+" transfered through FTP to the FTP server."
        return result 
    else:
        result=name+ " is is not a folder or a file. No action taken."
        return result
          
class cutToolFrame(wx.Frame):
    """
    AVC cut tool main GUI.
    A tool to cut exiting AudioCours recordings into smaller parts.
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
                          pos=(150, 150), size=(700, 600),
                          style=wx.DEFAULT_FRAME_STYLE)  
        # vars
        self.recordingPath=""
        self.tracks=[]
        self.timecodeAll=[]
        self.cutTimes=[]
        
        # widgets
        panel=wx.Panel(self)
        labelIntro=wx.StaticText(panel,-1,"Outil de decoupe d'un enregistrement Audiocours sous windows")
        btnOriginal= wx.Button(panel, -1, "Selection du dossier enregistrement audiocours")
        self.entryOriginal= wx.TextCtrl(panel, -1,"", size=(500,-1))
        labelCuts=wx.StaticText(panel,-1,"Instants de decoupe au format hh:mm:ss, example: 00.00.33;00.01.36;00.02.32")
        
        self.entryCue1=wx.TextCtrl(panel, -1,"", size=(100,-1))
        self.entryCue2=wx.TextCtrl(panel, -1,"", size=(100,-1))
        self.entryCue3=wx.TextCtrl(panel, -1,"", size=(100,-1))
        self.entryCue4=wx.TextCtrl(panel, -1,"", size=(100,-1))
        self.entryCue5=wx.TextCtrl(panel, -1,"", size=(100,-1))
        
        # Output text console
        self.consoleEntry=wx.TextCtrl(panel,style=wx.TE_MULTILINE | wx.HSCROLL)
        self.consoleEntry.SetBackgroundColour('black')
        self.consoleEntry.SetForegroundColour('white')
                                              
        btnCut= wx.Button(panel, -1, "<<<   Couper et calculer!   >>>")
        
        #bindings
        self.Bind(wx.EVT_BUTTON, self.findFolder, btnOriginal)
        self.Bind(wx.EVT_BUTTON, self.process, btnCut)
        
        # test case (example for an mp3 of 2mn30s duration
        self.entryCue1.SetValue("00.00.33")
        self.entryCue2.SetValue("00.01.36")
        self.entryCue3.SetValue("00.02.32")

        # layout
        vbox=wx.BoxSizer(wx.VERTICAL)   
        vbox.Add(labelIntro,0,wx.ALIGN_CENTER|wx.ALL,border=10)
        vbox.Add(btnOriginal,0,wx.ALIGN_CENTER|wx.ALL,border=10)
        vbox.Add(self.entryOriginal,0,wx.ALIGN_CENTER|wx.ALL,border=5)
        vbox.Add(labelCuts,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(self.entryCue1,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(self.entryCue2,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(self.entryCue3,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(self.entryCue4,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(self.entryCue5,0,wx.ALIGN_CENTER|wx.ALL,border=2)
        vbox.Add(btnCut,0,wx.ALIGN_CENTER|wx.ALL,border=10)
        vbox.Add(self.consoleEntry,proportion=1,flag=wx.EXPAND | wx.ALL, border=10)
        panel.SetSizer(vbox)
        self.Show(True)     
        self.writeConsole("Please select a recording folder to process and indicate cutting times")
    
    def writeConsole(self,text):
        "Write in Console precedte by date-time"
        self.consoleEntry.AppendText("\n["+getTime()+"] "+text)
    
    def findFolder(self,evt):  
        """ select original recording folder """
        openDir=wx.DirDialog(self)
        if pathData=="":
            pathData==os.getcwd()
        openDir.SetPath(pathData)
        openDir.ShowModal()
        self.recordingPath=openDir.GetPath()
        print self.recordingPath
        self.writeConsole("- Folder selected "+self.recordingPath)
        self.entryOriginal.SetValue(self.recordingPath)
        self.baseFolder=os.path.basename(self.recordingPath)
        
    def process(self,evt): 
        """ process and cut """
        print ">>> In process..."
        """
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
        self.writeConsole("- Cut times defined by user: "+str(self.cutTimes))
        try:
            f_global_timecode=open(self.recordingPath+"\\timecode.csv")
        except:
            self.writeConsole("- Warning : This is not a valid recorging folder. Processing stopped. \n")
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
            self.writeConsole("- cutting original mp3")
            mp3Output="p"+str(cutIndex+1)+".mp3"
            print "mp3Output: ",mp3Output
            #os.system('thirdparty\mp3splt.exe "%s" %s %s -d "%s" -o %s ' \
            #% (mp3ToCut,cutBegin,cutEnd,self.recordingPath,mp3Output))
            # warning !!! above commmand open dos window on the exe, try something like subprocess.Popen(['%s'%(vlcapp),"-vvvv",file,"--sout","%s"%typeout])
            subprocess.Popen(["thirdparty\mp3splt.exe","%s" % mp3ToCut,"%s"%cutBegin, "%s"%cutEnd,"-d","%s"%self.recordingPath,"-o","%s"%mp3Output])
            print ["thirdparty\mp3splt.exe","%s" % mp3ToCut,"%s"%cutBegin, "%s"%cutEnd,"-d","%s"%self.recordingPath,"-o","%s"%mp3Output]
            cutIndex+=1
            #self.consoleEntry.AppendText("\n- DEBUG:"+self.recordingPath+"\\p"+str(i)+".mp3")
            print "sleeping 2 sec to be sure mp3splt is finished"
            time.sleep(2) 
            """
        def makeNewRec():   
            print ">>> In process..."
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
            self.writeConsole("- Cut times defined by user: "+str(self.cutTimes))
            self.writeConsole("- Reading global timecode...")
            try:
                f_global_timecode=open(self.recordingPath+"/timecode.csv")
            except:
                self.writeConsole("- Warning : This is not a valid recorging folder no timecode.csv found. Processing stopped. \n")
            if not os.path.isfile(self.recordingPath+"/enregistrement-micro.mp3"):
                self.writeConsole("- Warning : This is not a valid recorging folder no enregistrement-micro.mp3 found. Processing stopped. \n")
                return 0
            
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
                self.writeConsole("- cutting original mp3")
                mp3Output="p"+str(cutIndex+1)+".mp3"
                print "mp3Output: ",mp3Output
                #os.system('thirdparty\mp3splt.exe "%s" %s %s -d "%s" -o %s ' \
                #% (mp3ToCut,cutBegin,cutEnd,self.recordingPath,mp3Output))
                # warning !!! above commmand open dos window on the exe, try something like subprocess.Popen(['%s'%(vlcapp),"-vvvv",file,"--sout","%s"%typeout])
                subprocess.Popen(["thirdparty\mp3splt.exe","%s" % mp3ToCut,"%s"%cutBegin, "%s"%cutEnd,"-d","%s"%self.recordingPath,"-o","%s"%mp3Output])
                print ["thirdparty\mp3splt.exe","%s" % mp3ToCut,"%s"%cutBegin, "%s"%cutEnd,"-d","%s"%self.recordingPath,"-o","%s"%mp3Output]
                cutIndex+=1
                #self.consoleEntry.AppendText("\n- DEBUG:"+self.recordingPath+"\\p"+str(i)+".mp3")
                pauseTime=5
                print "sleeping " +str(pauseTime)+"sec to be sure mp3splt is finished"
                self.consoleEntry.AppendText("\n- waiting for mp3split to finish - pausing for "+str(pauseTime)+" seconds ...")
                time.sleep(pauseTime)
                
            for i in [1,2,3,4,5]:
                print "checking for",  self.recordingPath+"/p"+str(i)+".mp3"
                if os.path.isfile(self.recordingPath+"/p"+str(i)+".mp3"):
                    self.consoleEntry.AppendText("\n- processing new sub recording")
                    print "- found a p"+str(i)+".mp3 file"
                    print "- creating folder p"+str(i)+"\n"
                    self.writeConsole("- creating folder p"+str(i)+"\n")
                    os.mkdir(self.recordingPath+"/p"+str(i))
                    print "- moving a copy of p"+str(i)+".mp3 file in his new folder and renaming"
                    if 1:#original code but flickering problems of the console in exe GUI
                        os.system('move "%s" "%s"' % (self.recordingPath+"\\p"+str(i)+".mp3",
                                                  self.recordingPath+"\\p"+str(i)+"\\enregistrement-micro.mp3"))
                    if 0:
                        print ">>> source:",self.recordingPath+"\\p"+str(i)+".mp3"
                        print ">>> destination:",self.recordingPath+"\\p"+str(i)+"\\enregistrement-micro.mp3"
                        subprocess.Popen(["move","%s"% self.recordingPath+"\\p"+str(i)+".mp3","%s"%self.recordingPath+"\\p"+str(i)+"\\enregistrement-micro.mp3"])
                    print "- renaming mp3 file to enregistrement-micro.mp3"
                    print "- making screenshot folder"
                    try:
                        os.mkdir(self.recordingPath+"\\p"+str(i)+"\\screenshots")
                    except:
                        print "- !!! Couldn't make screenshots folder !!!"
                        pass
                    #create a smile file for this track
                    smil=SmilGen("audio",self.recordingPath+"\\p"+str(i)+"\\")
                    #create a timecode file for this track
                    timecodeFile=open(self.recordingPath+"\\p"+str(i)+"\\timecode.csv",'a')
                    print "Found slides for this track:"
                    diaIDglob=1
                    diaIDtrack=1
                    for j in global_times:
                        self.consoleEntry.AppendText("*")
                        if (float(j)< self.cutTimes[i]) and (float(j)> self.cutTimes[i-1]):
                            print ">>> "+str(j)
                            if i>1 and diaIDtrack==1:
                                # Make a copy of the last slide in the previous track
                                if 0: #original code but flickering problems of the console in exe GUI
                                    os.system('copy "%s" "%s"' % (self.recordingPath+"\\screenshots\\D"+str(diaIDglob-1)+".jpg",
                                            self.recordingPath+"\\p"+str(i)+"\\screenshots\\D"+str(diaIDtrack)+".jpg"))
                                    os.system('copy "%s" "%s"' % (self.recordingPath+"\\screenshots\\D"+str(diaIDglob-1)+"-thumb.jpg",
                                            self.recordingPath+"\\p"+str(i)+"\\screenshots\\D"+str(diaIDtrack)+"-thumb.jpg"))
                                if 1:
                                    #subprocess.Popen(["copy","%s"%self.recordingPath+"\screenshots\D"+str(diaIDglob-1)+".jpg","%s"%self.recordingPath+"\p"+str(i)+"\screenshots\D"+str(diaIDtrack)+".jpg"])
                                    shutil.copy(self.recordingPath+"\screenshots\D"+str(diaIDglob-1)+".jpg",self.recordingPath+"\p"+str(i)+"\screenshots\D"+str(diaIDtrack)+".jpg")
                                    #subprocess.Popen(["copy","%s"%(self.recordingPath+"\screenshots\D"+str(diaIDglob-1)+"-thumb.jpg","%s"%self.recordingPath+"\p"+str(i)+"\screenshots\D"+str(diaIDtrack)+"-thumb.jpg")])
                                    shutil.copy(self.recordingPath+"\screenshots\D"+str(diaIDglob-1)+"-thumb.jpg",self.recordingPath+"\p"+str(i)+"\screenshots\D"+str(diaIDtrack)+"-thumb.jpg")
                                # write time of this first slide
                                timecodeFile.write("0.00"+"\n")
                                # write smil file
                                smil.smilEvent("0.00",diaIDtrack)
                                diaIDtrack+=1
                                
                            # Make a copy of the j slides and thumbnails  and rename
                            if 0:#original code but flickering problems of the console in exe GUI
                                os.system('copy "%s" "%s"' % (self.recordingPath+"\\screenshots\\D"+str(diaIDglob)+".jpg",
                                        self.recordingPath+"\\p"+str(i)+"\\screenshots\\D"+str(diaIDtrack)+".jpg"))
                                os.system('copy "%s" "%s"' % (self.recordingPath+"\\screenshots\\D"+str(diaIDglob)+"-thumb.jpg",
                                        self.recordingPath+"\\p"+str(i)+"\\screenshots\\D"+str(diaIDtrack)+"-thumb.jpg"))
                            if 1:
                                #copyfrom=self.recordingPath+"\screenshots\D"+str(diaIDglob)+".jpg"
                                #copyto=self.recordingPath+"\p"+str(i)+"\screenshots\D"+str(diaIDtrack)+".jpg"
                                #print "copyfrom:",copyfrom
                                #print "copyto:",copyto
                                #subprocess.Popen(["copy","%s" % self.recordingPath+"\screenshots\D"+str(diaIDglob)+".jpg","%s" % self.recordingPath+"\p"+str(i)+"\screenshots\D"+str(diaIDtrack)+".jpg"])
                                shutil.copy(self.recordingPath+"\screenshots\D"+str(diaIDglob)+".jpg",self.recordingPath+"\p"+str(i)+"\screenshots\D"+str(diaIDtrack)+".jpg")
                                #subprocess.Popen(["copy","%s" % self.recordingPath+"\\screenshots\\D"+str(diaIDglob)+"-thumb.jpg","%s" % self.recordingPath+"\\p"+str(i)+"\\screenshots\\D"+str(diaIDtrack)+"-thumb.jpg"])
                                shutil.copy(self.recordingPath+"\\screenshots\\D"+str(diaIDglob)+"-thumb.jpg",self.recordingPath+"\\p"+str(i)+"\\screenshots\\D"+str(diaIDtrack)+"-thumb.jpg")
                            # corrected time and write time code
                            adjustedTime=j-float(self.cutTimes[i-1])
                            timecodeFile.write(str(adjustedTime)+"\n")
                            # write smil file
                            smil.smilEvent(str(adjustedTime),diaIDtrack)
                            
                            diaIDtrack+=1
                        diaIDglob+=1       
                    timecodeFile.close()
                    smil.smilEnd("audio")
                    global workDirectory
                    workDirectory= self.recordingPath+"/p"+str(i)
                    try:
                        htmlGen()
                    except:
                        self.consoleEntry.AppendText("\n- Error: p* foler may already exist, please delete before")
                    #os.system('move "%s" "%s"' % (self.recordingPath+"/p"+str(i),os.path.basename(self.recordingPath)+"/pp"+str(i)+"-"+self.baseFolder))
                    #os.system('move "%s" "%s"' % (self.recordingPath+"/p"+str(i),self.recordingPath+"p"+str(i)+"-"+self.baseFolder))
                    print "moving to --> ", self.recordingPath+"-p"+str(i)
                    if 0:#original code but flickering problems of the console in exe GUI
                        os.system('move "%s" "%s"' % (self.recordingPath+"/p"+str(i),self.recordingPath+"-p"+str(i)))
                    if 0:
                        subprocess.Popen(["move","%s"%self.recordingPath+"/p"+str(i),"%s"%self.recordingPath+"-p"+str(i)])
                    if 0:
                        subprocess.Popen(["move","p"+str(i),"..\p"+str(i)],shell=True, stdout=subprocess.PIPE)
                    if 0:#screenshots folder empty :/ 
                        shutil.copytree(self.recordingPath+"/p"+str(i), self.recordingPath+"-p"+str(i))
                    #print "attempting to  :", 'move %s %s' % (self.recordingPath+"/p"+str(i),self.recordingPath+"-p"+str(i)+"-"+self.baseFolder)
            
            self.writeConsole("- Moving new folders to Audiovideocorus data folder")
            time.sleep(2)
            for i in [1,2,3,4,5]:
                if os.path.exists(self.recordingPath+"/p"+str(i)):
                    #subprocess.Popen(["move","%s"%self.recordingPath+"/p"+str(i),"%s"%self.recordingPath+"-p"+str(i)])
                    self.writeConsole("- Found and moving " + self.recordingPath+"/p"+str(i)+"to AVC data folder...")
                    os.system('move "%s" "%s"' % (self.recordingPath+"/p"+str(i),"%s"%self.recordingPath+"-p"+str(i)))
                    time.sleep(2)
                    
            print "Finished processing!"
            #self.writeConsole("- Finished processing\n")
            self.writeConsole("- End\n") 
        start_new_thread(makeNewRec,())   
        #makeNewRec()
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

def getAudioVideoInputFfmpeg(pathData=pathData):
        """A function to get Audio input from ffmpeg.exe (http://ffmpeg.zeranoe.com/builds/)
        Returns a list of two lists : [audioDevices,videoDevices]"""
        
        #ffmpeg.exe don't work with input number. It is necessary to get the name of the Direcshow input.
        #also subprocess.Popen returns an empty string I therefore create the output in a file that i read just after
        
        #Ask ffmpeg.exe to give devices seen by direcshow on windows and write it to devices.txt file in the AVC data folder       
        if 1:
            os.system('ffmpeg -list_devices true -f dshow -i dummy > "%s"\devices.txt 2>&1' %pathData)
        #Read back devices.txt
        audioDevices=[] # List of audio devices
        videoDevices=[] # List of video devices
        audioIndex=None # Index position where audio devices listing is starting
        videoIndex=None # Index position where video devices listing is starting
        fileDevices=open(pathData+"\devices.txt","r") #as direct shell communication is not possible (=>file intermediary)
        devicesList=fileDevices.readlines()
        print "device list from devices.txt", devicesList
        fileDevices.close()
        # searching audio devices
        for index,device in enumerate(devicesList):
            if device.find("audio devices")>0:
                audioIndex= int(index) 
                print "Found 'audio devices' from Direcshow/ffmpeg, taking first device by default (0)"
            if (audioIndex!=None)and(index>audioIndex) and (device.find("exit")<0):
                aDevice=device.split('"')[1]
                print index-(audioIndex+1),":", aDevice
                audioDevices.append(aDevice)
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
                videoDevices.append(aDevice)    
        print "audio device deduced from devices.txt", audioDevices
        print "video device deduced from devices.txt", videoDevices        
        return [audioDevices,videoDevices]
    
## Start app
if __name__=="__main__":

    # Check if another instance is already launched and kill it if it exist
    kill_if_double()
    time.sleep(1)#delay to be sure serial port is free if just killed a double?
    
    app_startup_date=getTime()
    ## GUI Define
    app=wx.App(redirect=False)
    
    # Create a default data audiovideocours folder if it doesn't exists
    if os.path.isdir(os.environ["USERPROFILE"]+"\\audiovideocours"):
        print "Default user data exists at USERPROFILE\\audiovideocours : OK"
    else: 
        print "Creating default data folter in USERPROFILE\\audiovideocours"
        os.mkdir(os.environ["USERPROFILE"]+"\\audiovideocours")
            
    # Set-up language
    if language=="French":
        print "Setting French language..."
        langFr = gettext.translation('mediacours', "locale",languages=['fr'])
        langFr.install()
        
    confFileReport=""    
    # Check if a configuration file exist in USERPROFILE
    # otherwise search for one in ALLUSERPROFILE
    if os.path.isfile(os.environ["USERPROFILE"]+"\\audiovideocours\\mediacours.conf"):
        print "Found and using configuration file in USERPROFILE\\audiovideocours"
        readConfFile(confFile=os.environ["USERPROFILE"]+"\\audiovideocours\\mediacours.conf")
    elif os.path.isfile(os.environ["ALLUSERSPROFILE"]+"\\audiovideocours\\mediacours.conf"):
        print "Found and using configuration file in ALLUSERSPROFILE\\audiovideocours"
        readConfFile(confFile=os.environ["ALLUSERSPROFILE"]+"\\audiovideocours\\mediacours.conf")
    else:
        print "No configuration file found"
        dialog=wx.MessageDialog(None,message="No configuration file found in either USERPROFILE or ALLUSERSPEOFILE",
                                caption="Audiovideocours Error Message", style=wx.OK|wx.ICON_INFORMATION)
        dialog.ShowModal()
    
    # Automatically detect IP of the recording place
    recordingPlace=socket.gethostbyname(socket.gethostname()).replace(".","_")
    #recordingPlace=socket.gethostbyaddr(socket.gethostname()) #gives also the litteral hostname (list)
    print "... recordingPlace = ", recordingPlace
    
    if pathData == None or pathData=="":
        #pathData=os.getcwd()
        pathData=os.environ["USERPROFILE"]+"\\audiovideocours"
        print "pathData=None => PathData is now ", pathData
    writeInLogs(confFileReport)
    
    # Start-up message
    print "AudioVideoCours client launched at ", datetime.datetime.now(), " ..."
    writeInLogs("\nAudioVideoCours client launched at "+ \
    str(datetime.datetime.now()))
    writeInLogs("\npathData is "+pathData)
   
    # Set-up hooks
    setupHooks()
    # Set-up videoprojector
    if videoprojectorInstalled==True:
        videoprojector=Videoprojector()
    # Start socket server
    if socketEnabled==True:
        start_new_thread(LaunchSocketServer,())
    # start shutdown PC thread if no PC activity detected
    if 0:
        start_new_thread(shutdownPC_if_noactivity,())
    # Write mediacours PID in a file (for use in the automatic updater) 
    PID_f=open(os.environ["USERPROFILE"]+"\\PID_mediacours.txt",'w')
    PID_f.write(str(os.getpid()))
    PID_f.close()
        
    ## GUI launch
    #app=wx.App(redirect=False)
    frameUnivr=univrEndFrame(None,title="Message Univ-R")
    #frameUnivr.Show()   
    frameBegin=BeginFrame(None,title="Attention")
    #frameBegin.Bind(wx.EVT_END_SESSION,onEndSession)

    #frameBegin.Show() # For debug
    frameBegin.Show()
    if standalone != True: frameBegin.Hide()
    frameEnd=EndingFrame(None,title="Attention")
    #frameEnd.Bind(wx.EVT_END_SESSION,onEndSession)
    frameEnd.Show()
    frameEnd.Hide()
    #frameEnd.Show() # For debug
    
    # get audio and video inputs
    #audioEncoder="ffmpeg"
    if 1:
        if audioEncoder==True or usage=="screencast" or videoEncoder=="ffmpeg": # if True search for Directshow devices on windows via ffmpeg.exe
            inputList=getAudioVideoInputFfmpeg(pathData=pathData)
            audioinputList=inputList[0]
            videoinputList=inputList[1]
            print "inputList", inputList
            print "audioinputList", audioinputList
            print "videoinputList", videoinputList
            #audioinputName= getAudioVideoInputFfmpeg(pathData=pathData)[0][int(audioinput)]
            audioinputName=audioinputList[int(audioinput)]
            try:
                #videoinputName= getAudioVideoInputFfmpeg(pathData=pathData)[1][int(videoinput)]
                videoinputName= videoinputList[int(videoinput)]
            except:
                videoinputName="None"
            if 1:
                audioinputName=audioinputName.replace("é","�")
                videoinputName=videoinputName.replace("é","�")
                # others french characters ?? https://forums.alliedmods.net/showthread.php?t=114798
            print "audioinput is  now >>>", audioinputName
            print "audioinput is  now >>>", videoinputName
            if 0: # Detecting non english characters and warning pop up ??
                if audioinputName.find("é")>=0:
                    dialogText= "!!! Warning : non english characters in audio input device name it may not work !!!" 
                    print dialogText
                    dialog=wx.MessageDialog(None,message=dialogText,
                    style=wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
                    dialog.ShowModal()
                if videoinputName.find("é")>=0:
                    dialogText= "!!! Warning : non english characters in video input device name it may not work !!!" 
                    print dialogText
                    dialog=wx.MessageDialog(None,message=dialogText,
                    style=wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
                    dialog.ShowModal()
    
    ## Use a special serial keyboard ?
    if serialKeyboard==True:
        if amxKeyboard==True:
            clavierAMX=AMX()
            start_new_thread(clavierAMX.listen,(frameEnd, frameBegin, tryFocus))
        else:
            clavier=SerialHook()    
            start_new_thread(clavier.listen,())
    ## Systray  
    if usage=="audio":
        icon1 = wx.Icon('images/audiocours1.ico', wx.BITMAP_TYPE_ICO)
        icon2 = wx.Icon('images/audiocours2.ico', wx.BITMAP_TYPE_ICO)
        tbicon = wx.TaskBarIcon()
        tbicon.SetIcon(icon1, "AudioCours en attente")
    if usage=="video":
        icon1 = wx.Icon('images/videocours1.ico', wx.BITMAP_TYPE_ICO)
        icon2 = wx.Icon('images/videocours2.ico', wx.BITMAP_TYPE_ICO)
        tbicon = wx.TaskBarIcon()
        tbicon.SetIcon(icon1, "VideoCours en attente")
    
    if standalone==True:
        showVuMeter()
    
    print "remoteControl =",remoteControl
    if remoteControl==False and standalone==True:
        print "remote Control: False"
        hosts="127.0.0.1"
    else:
        hosts="0.0.0.0"
    if remotePort==80 and standalone==True:
        remotePort=8081
        print 'switching remote port to '+str(remotePort)+' for standalone usage'
    print "Launching integrated server with port", remotePort, "for hosts", hosts
    start_new_thread(goAVCremote,(remotePort,pathData,hosts))
    app.MainLoop()
