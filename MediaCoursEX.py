#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#*****************************************************************************
#
#     MediaCours (Windows audio/video client and 'standalone' version)
#
#    (c) ULP Multimedia 2006 - 2007 
#     Developer : francois.schnell [AT ulpmm.u-strasbg.fr]
#
#     For this version a serial keyboard and a videocard aquisition
#     or a frame grabber is necessary. See this URL for more informations:
#     http://ulpmm-projets.u-strasbg.fr/projets/videocours/wiki/ExternalVersion
#
#---
#
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

# Import modules
import wx, wx.lib.colourdb,zipfile
import wx.lib.hyperlink as hl
import gettext
import sys,os,time,datetime,tarfile,ConfigParser,threading
import socket
import msvcrt,Image,ImageGrab,pythoncom,serial,subprocess
## Static imports from PIL for py2exe
from PIL import GifImagePlugin
from PIL import JpegImagePlugin
#import ImageTk
import pymedia.audio.sound as sound
import pymedia.audio.acodec as acodec
import pymedia.muxer as muxer
from VideoCapture import Device
from thread import start_new_thread, exit
from urllib2 import urlopen
from PIL import Image
from os import chdir
from ftplib import FTP
from pywinauto import *
from pywinauto import application
from optparse import OptionParser # this for videolog.exe
import fnmatch #this is for videolog.exe (library going in library.zip)

## Defautl global variables before config file reading
#------------------------------------------------------------
univr_order=False # Is the recording order comes from Univr ?
standalone=False
# Publishing form variables
title=""
description=""
name=""
firstname=""
login=""
genre=""
ue=""
" To use the app without a  webserver to publish to"
recording = False
" To know if we are recording now" 
workDirectory="" 
"The working/current directory"
dirName=""
"The data directory"
pathData=""
"Name of the last recording folder"
id= ""
"An id which could be received and send from the socket"
urlserver= ""
"Default URL of the audiovideocours server containing the submit form"
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
           'bitrate': 128000,
           'sample_rate': 48000 ,
           'channels': 1 } 
"Set of parameters for the pymedia audio Encoder"
nameRecord="enregistrement-micro.mp3"
"Dafault name of the audio recording"        
tryFocus=False
"A boolean var to inform when the app is trying to get focus back on a frame"
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
ftpUrl=''
"FTP URL server for online publication"
eventDelay=1.5
"Number of seconds before allowing a new screenshot"
recordingPlace= "not given"
"Optional location indication for the log file and the server" 
maxRecordingLength=18000
"Maximum recording length in seconds(1h=3600s,5h=18000s)"
usage="audio"
"Usage ='audio' for audio and 'video' for video recording "
genre=""
"A generic access code"
videoEncoder="wmv"
"""Choice of the videoencoder to use if usage=video
'wmv' = Windows Media Encoder ; 'real'= Real producer """

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
login=""
genre=""
live=False
language="French"
ftpLogin=""
ftpPass=""
videoinput="0"

#------ i18n settings -------

gettext.install("mediacours","locale")

#------------------------------------------------------------------------------

def readConfFile():
    """ Reads the config file and get those values """
    print "> Search configuration file and use the values if they exist :\n"
    global id,urlserver,samplingFrequency,createMp3,stopKey,portNumber,pathData\
    ,serialKeyboard,startKey,videoprojectorInstalled,videoprojectorPort,keyboardPort\
    ,videoProjON,videoProjOFF,ftpUrl,eventDelay,maxRecordingLength,recordingPlace\
    ,usage,cparams,bitrate,socketEnabled,standalone,videoEncoder,amxKeyboard\
    ,live,language,ftpLogin,ftpPass,videoinput
    
    section="mediacours"

    def readParam(param):
        param=str(param)
        if config.has_option(section,param) == True:
            paramValue= config.get(section,param)
            if param not in ["ftpPass","ftpLogin"]:
                print "... "+param+" = ", paramValue
                writeInLogs("\n\t:"+param+"+= "+paramValue)
            if paramValue=="True" or paramValue=="False":
                paramValue=eval(paramValue)
            return paramValue
        else:
            return "None"
    try:
        fconf=open("mediacoursExt.conf","r")
        config= ConfigParser.ConfigParser() 
        config.readfp(fconf)
        language=readParam("language")
        usage=readParam("usage")
        pathData=readParam("pathData")
        standalone=readParam("standalone")
        videoEncoder=readParam("videoEncoder")
        id=readParam("id")
        urlserver=readParam("urlserver")
        samplingFrequency=readParam("samplingFrequency")
        bitrate=readParam("bitrate")
        stopKey=readParam("stopKey")
        socketEnabled=readParam("socketEnabled")
        portNumber=readParam("portNumber")
        serialKeyboard=readParam("serialKeyboard")
        amxKeyboard=readParam("amxKeyboard")
        keyboardPort=readParam("keyboardPort")
        videoprojectorInstalled=readParam("videoprojectorInstalled")
        videoprojectorPort=readParam("videoprojectorPort")
        videoProjON=readParam("videoProjON")
        videoProjOFF=readParam("videoProjOFF")
        ftpUrl=readParam("ftpUrl")
        eventDelay=readParam("eventDelay")
        maxRecordingLength=readParam("maxRecordingLength")
        recordingPlace=readParam("recordingPlace")
        ftpLogin=readParam("ftpLogin")
        ftpPass=readParam("ftpPass")
        videoinput=readParam("videoinput")
        print "\n"; fconf.close()
        writeInLogs("\n")
    except:
        print "Something went wrong while reading the configuration file\n"
    
        
def recordNow():
    "Record the audio input now with pymedia "
    global recording, diaId, timecodeFile, t0, dateTime0, dirName, workDirectory
    global snd,ac,cparams, nameRecord,usage,smil,pathData,t1,pathData
    recording= True
    print "Trying to open video device"
    tbicon.SetIcon(icon2, "Enregistrement en cours")
    diaId = 0 # initialize screenshot number and time
    t0 = time.time() 
    t1 = time.time()
    dateTime0 = datetime.datetime.now()
    print "- Begin recording now ! ...(We're in recordNow function) \n"
    dirName = str(dateTime0)
    dirName = dirName[0:10]+'-'+ dirName[11:13] +"h-"+dirName[14:16] +"m-" +dirName[17:19]+"s"#+ "-"+ dirName[20:22]
    
    if pathData=="" or pathData=="None":
        pathData=os.getcwd()
        
    workDirectory=pathData+"\\"+dirName
    os.mkdir(workDirectory)
    writeInLogs("- Begin recording at "+ str(datetime.datetime.now())+"\n")

    def screenshotThread():
        """ Launch videolog tool"""
        global recording,videolog_pid
        order= 'python videolog.py -v %s -p "%s"'% (videoinput,workDirectory)
        videolog_pid = subprocess.Popen(order).pid

    ## Engage videlog tool
    start_new_thread(screenshotThread,())    
    def record():
        """ Record audio only - mp3 - with pymedia"""
        global recording, cparams,t1,diaId        #diaId=0 #added for videocapture
        f= open( workDirectory+'\\'+nameRecord, 'wb' )
        ac= acodec.Encoder( cparams )
        snd= sound.Input(cparams["sample_rate"],cparams["channels"], sound.AFMT_S16_LE)
        snd.start()
        while recording==True:
            time.sleep(0.1)
            #t=time.time()        
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
                print "-- stopped recording --"
        
    def windowsMediaEncoderRecord():
        """ Record Video with Windows Media Encoder Series 9""" 
        scriptPath=r' cscript.exe C:\"Program Files\Windows Media Components\Encoder\WMCmd.vbs"'
        arguments=" -adevice 1 -vdevice 1 -output "+\
        dirName+"\enregistrement-video.wmv -duration "+str(maxRecordingLength)
        os.system(scriptPath+arguments)
        
    def realProducerRecord():
        """ Record video with Real Producer basic """
        """os.system("producer -vc 0 -ac 0 -o "+dirName+\
        "\enregistrement-video.rm -d "+str(maxRecordingLength))
        """
        #producerPath=r'C:\"Program Files\Real\RealProducer Plus 11\producer.exe"'
        os.system("producer.exe -vc 0 -ac 0 -pid pid.txt -o "+dirName+\
        "\enregistrement-video.rm -d "+str(maxRecordingLength))
        #order="producer.exe -vc 0 -ac 0 -pid pid.txt -o "+dirName+"/enregistrement-video.rm -d "+str(maxRecordingLength)
        #print "order: ",order
        #os.spawnl(os.P_NOWAIT,order)
        
    def liveStream():
        global vlcPid
        time.sleep(2)
        print "Going live ..."
        command=r'C:\"Program Files"\VideoLAN\VLC\vlc.exe -vvvv '
        file=dirName+ '\enregistrement-micro.mp3'
        argument =' --sout "#standard{access=http,mux=asf}" '
        argument2 =' --sout \"\#standard{access=http,mux=asf}\" '
        todo=command + file+ argument
        todo2=command + file+ argument2
        print "todo= ", todo
        os.system(todo)
    if usage=="audio":
        start_new_thread(record,())
        
    if usage=="video" and videoEncoder=="wmv":
        print "searching Windows Media Encoder ..."   
        start_new_thread(windowsMediaEncoderRecord,())
    if usage=="video" and videoEncoder=="real":
        print "searching Real media encoder"    
        start_new_thread(realProducerRecord,())
    if live==True:
        start_new_thread(liveStream,())
 
def recordStop():
    "Stop recording the audio input now"
    global recording,timecodeFile,videolog_pid
    #screenshot()
    lastEvent=time.time()
    recording= False
    tbicon.SetIcon(icon1, usage+"cours en attente")
    print "from recordStop, recording= ", recording 
    print "Received order to stop recording => stopping recording \n"
    #timecodeFile.close()
    ## Kill videolog
    print "Trying to kill videolog with pid=",str(videolog_pid)
    os.popen("taskkill /F /PID "+str(videolog_pid))#stop videolog
    
    #    smilFile.write('<audio src="enregistrement-micro.mp3" /></par></body></smil>')
    if usage=="video" and videoEncoder=="wmv":
        #smilFile.write('<audio src="enregistrement-video.wmv" /></par></body></smil>')
        os.popen("taskkill /F /IM  cscript.exe")#stop MWE !!!
        #smilFile.write('<audio src="enregistrement-video.rm" /></par></body></smil>')
    if usage=="video" and videoEncoder=="real":
        #killerPath=r'C:\"Program Files\Real\RealProducer Plus 11\samples\utilities\producer_signal_generator\signalproducer.exe"'
        os.popen("signalproducer.exe -P pid.txt")#stop Real producer
    if live==True:
        os.system('tskill vlc')
    #smilFile.close()
    writeInLogs("- Stopped recording at "+ str(datetime.datetime.now())+"\n")
    #smil.smilEnd(usage,videoEncoder)
    ## Create a second smil at the end
    smil=SmilGen(usage,workDirectory)
    f=open(workDirectory+"/timecode.csv")
    diaTime=f.read().split("\n")[:-1]
    #nbDia=len(diaTime)
    diaId=1
    offset=0 # the estimate time it takes to videolog to begin
    for timeStamp in diaTime:
        timeStamp=str(float(timeStamp)+offset)
        smil.smilEvent(timeStamp,diaId)
        diaId+=1
    smil.smilEnd(usage,videoEncoder="real")
        
def playAudio():
    "Play the sound file from the folder selected"
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

def confirmPublish(folder=''):
    "Publish the recording when hitting the 'publish' button "
    global id,entry1,entry2,entry25,entry3,entry4
    #print "description = ", description
    frameEnd.statusBar.SetStatusText(" Publication en cours, merci de patienter ...")
    if dirName =="":
        frameEnd.statusBar.SetStatusText("Rien ? publier ...")
    if dirName != "":
        #mediapath= workDirectory+'\\'+dirName
        zip = zipfile.ZipFile(pathData+"\\"+dirName+".zip", 'w')
        for fileName in os.listdir ( workDirectory ):
            if os.path.isfile (workDirectory+"\\"+fileName ):
                zip.write(workDirectory+"\\"+fileName,
                dirName+"/"+fileName,zipfile.ZIP_DEFLATED)
        for fileName in os.listdir ( workDirectory+"\\screenshots"):
            zip.write(workDirectory+"\\screenshots\\"+fileName,
                dirName+"/"+"screenshots\\"+fileName,zipfile.ZIP_DEFLATED)
        zip.close()
        # For the logFile :
        writeInLogs("- Asked for publishing at "+ str(datetime.datetime.now())+\
        " with id="+id+" title="+title+" description="+description+" mediapath="+\
        dirName+".zip"+" prenom "+firstname+" name="+name+" genre="+genre+" ue="+\
        ue+ " To server ="+urlserver+"\n")
        #try:
        print "------ tar ordered------"
        # Send by ftp
        print "Sending an FTP version..."
        ftp = FTP(ftpUrl)
        ftp.login(ftpLogin, ftpPass)
        print "debut de ftp"
        f = open(workDirectory+".zip",'rb')# file to send 
        if folder=="canceled":
            print "Trying to open cancel forlder"
            ftp.cwd("canceled") 
        ftp.storbinary('STOR '+ dirName+".zip", f) # Send the file
        f.close() # Close file and FTP
        ftp.quit()
        print "fin de ftp"
        if standalone == True:
            frameEnd.Hide()
            frameBegin.Show()
        if folder=="":
            
            #Send data to the AudioCours server (submit form)
            page = urlopen(urlserver,\
            "fichier="+dirName+".zip"+"&id="+id+"&title="+title+"&description="+description+\
            "&name="+name+"&firstname="+firstname+"&login="+login+"&genre="+genre+\
            "&ue="+ue+"&timing=n"+"&mediapath="+dirName+".zip")
            print "------ Response from Audiocours : -----"
            serverAnswer= page.read() # Read/Check the result
            print serverAnswer
        # set the id variable to (id:no) again
        print "id is now back to empty" 
        id= ""
        print "setting entry fields back to empty"
        entry1.SetValue("")
        entry2.SetValue("")
        entryNom.SetValue("")
        entryPrenom.SetValue("")
        #entry25.SetValue("")
        #entry3.SetValue("")
        entry4.SetValue("")
        frameEnd.statusBar.SetStatusText("---")
    else:
        print "Pas de publication: pas d'enregistrement effectu?"
    
    
def LaunchSocketServer():
    """ Launch a socket server, listen to eventual orders
    and decide what to do """
    global id,univr_order
    print "Client is listening for socket order ..."
    mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    mySocket.bind ( ( '', int(portNumber) ) )
    mySocket.listen ( 1 )
    while True:
        channel, details = mySocket.accept()
        print 'We have an opened connection with', details
        writeInLogs('- We have an opened connection with '+str(details)+"\n")
        received = channel.recv(100)
        print "===> Received =",received
        writeInLogs("- received = "+str(received)+"\n")
        if received != "":
            if received=="SHOW_AVC":
                frameBegin.Show()
            # search for an (id:xxxxx) pattern
            iDbegin1= received.find("(id:")
            iDbegin2= received.find("(title:")
            iDbegin3= received.find("(description:")
            iDend= received.find(")")
            iDrecord= received.find("(order:record)")
            if (iDbegin1 > -1)and (iDend > -1):
                id=received[(iDbegin1+4):iDend]
                print "received ID number ", id 
                channel.send ( 'Received ID' + str(id))
                #windowBack(frameBegin)
                caption="Enregistrement via Univ-R"
                text="Veulliez appuyer sur le bouton audiovideocours\
                \ndu clavier de commande de la salle."
                dialog=wx.MessageDialog(None,message=text,caption=caption,
                style=wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
                #if the user clicks on "cancel" we should put id back to ""?
                #dialog.ShowModal()
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
        
def windowBack(frame):
    "Show the frame back in wiew"
    global tryFocus, recording
    tryFocus=True
    frame.Show()
    #time.sleep(0.5)
    frame.Show()
    def comeBack():
        print "-",
        appAuto = application.Application()
        appAuto.connect_(handle = findwindows.find_windows(title = "Attention")[0])
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

def writeInLogs(what):
    """Write events in a configuration file (one per month)"""
    global logFile
    yearMonth=str(datetime.datetime.now())
    yearMonth=yearMonth[:7]
    logFile = open ("log-"+yearMonth+".txt","a")
    logFile.write(what)
    logFile.close()
    
##############################################
class SerialHook:
    """ a soft hook to a special RS-232 keyboard used for amphi automation"""
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
        """ Read the state of the Kb at each delta """
        global id
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
                    recordStop()
                    print "id=",id
                    if id=="":
                        windowBack(frameEnd)
                    else:
                        print "Not showing form (because UnivR recording"
                        start_new_thread(confirmPublish,())
                        caption="Fin enregistrement via Univ-R"
                        text="Votre enregistrement a été envoyé."
                        dialog=wx.MessageDialog(None,message=text,caption=caption,
                        style=wx.OK|wx.ICON_INFORMATION)
                        dialog.ShowModal()
                        
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
    A class to read the capture ON/OFF orders from the AMX
    in ULP main amphitheatres and control the recording
    """
    def __init__(self):
        self.ser = serial.Serial(keyboardPort)
        print "AMX keyboard init"
    def listen(self,frameEnd, frameBegin, tryFocus):
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
    """ A class to control a videoprojector through RS232 """
    def __init__(self):
        """ Open the serial port of the videoprojector"""
        print "Opening serial port of the videoprojector"
        print "with serial port number =", videoprojectorPort
        #self.ser = serial.Serial(videoprojectorPort)
        print "Testing videoporjector port"
        self.ser = serial.Serial(int(videoprojectorPort))
        self.ser.close()
    def projOn(self):
        """Send the 'switch on' command to the videoprojector"""
        self.ser = serial.Serial(int(videoprojectorPort))
        self.ser.write(videoProjON)
        print "- sending "+videoProjON+" to port com "+str(videoprojectorPort)
        self.ser.close()
    def projOff(self):
        """Send the 'switch off' command to the videoprojector"""
        self.ser = serial.Serial(int(videoprojectorPort))
        self.ser.write(videoProjOFF)
        print "- sending "+videoProjOFF+" to port com "+str(videoprojectorPort)
        self.ser.close()

class SmilGen:
    """ A class to produce a SMIL file on the fly """
    def __init__(self,usage,workDirectory):
        """ Create the first part of the smil file
        """
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
        self.smilFile.close()

## GUI Definition
app=wx.App(redirect=False)

class BeginFrame(wx.Frame):
    """A begining frame to warn the user he will begin to record"""
    def __init__(self, parent, title):
        global liveFeed
        """Create the warning window"""
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(500, 330),
        style=wx.DEFAULT_FRAME_STYLE ^ (wx.CLOSE_BOX|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))

        panel=wx.Panel(self)
        panel.SetBackgroundColour("white") 
        
        if standalone==True:
            menubar=wx.MenuBar()
            menuInformation=wx.Menu()
            menubar.Append(menuInformation,"Informations")
            help=menuInformation.Append(wx.NewId(),_("Help"))
            conf=menuInformation.Append(wx.NewId(),_("Configuration"))
            version=menuInformation.Append(wx.NewId(),"Version")
            self.Bind(wx.EVT_MENU,self.help,help)
            self.Bind(wx.EVT_MENU,self.about,version)
            self.Bind(wx.EVT_MENU,self.configuration,conf)
            #self.SetMenuBar
            
        im1 = wx.Image('images/ban1.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        text1="\n\t"+_("By pressing the  ' Record ! '  button, the  recording will  ")+"\n\t"+\
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
        
        if  live==True:
            liveFeed=wx.CheckBox(panel,-1,_("Live streaming"),)
        btn = wx.Button(parent=panel, id=-1, label=_("Record!"),size=(200,50))
        if standalone == True:
            btnNext = wx.Button(parent=panel, id=-1, label=_("Other choices"),size=(100,50))
            btnQuit = wx.Button(parent=panel, id=-1, label=_("Quit"),size=(100,50))
        sizerV = wx.BoxSizer(wx.VERTICAL)
        
        sizerH=wx.BoxSizer()
        
        sizerV.Add(wx.StaticBitmap(panel, -1, im1, (5, 5)), 0, wx.ALIGN_CENTER|wx.ALL, 0)
        sizerV.Add(text, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        if  live==True:
            sizerV.Add(liveFeed, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizerV.Add(sizerH, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizerH.Add(btn, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        if standalone == True:
            sizerH.Add(btnNext, 0, wx.ALIGN_CENTER|wx.ALL, 10)
            sizerH.Add(btnQuit, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        """
        sizerFoot = wx.BoxSizer()
        sizerFoot.Add(wx.StaticBitmap(panel, -1, im2, (5, 5)), 0, wx.ALIGN_CENTER|wx.ALL, 0)
        sizerV.Add(sizerFoot, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        """
                
        panel.SetSizer(sizerV)
        
        panel.Layout() # what for ?
        
        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.engageRecording, btn)
        if standalone == True:
            self.Bind(wx.EVT_BUTTON, self.SkiptoEndingFrame, btnNext)
            self.Bind(wx.EVT_BUTTON, self.exitApp, btnQuit)
        if standalone==True:
            self.SetMenuBar(menubar)
    
    def about(self,evt): 
        """An about message dialog"""
        text="AudioVideoCours v 0.84 \n\n"\
        +_("Website:")+"\n\n"+\
        "http://audiovideocours.u-strasbg.fr/"+"\n\n"\
        +"(c) ULP Multimedia 2007"
        dialog=wx.MessageDialog(self,message=text,
        style=wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
        dialog.ShowModal()
        
    def help(self,evt):
        """ A fucntion to provide help on how to use the software"""
        def launch():
            #subprocess.Popen([r'C:\Windows\System32\notepad.exe', "readme.txt"])
            subprocess.Popen(['notepad.exe', pathData+"/redame.txt"])
            
        start_new_thread(launch,())
    
    def configuration(self,evt):
        """ A fucntion to open the configuration file"""
        def launch():
            subprocess.Popen([r'C:\Windows\System32\notepad.exe', "mediacours.conf"])
        start_new_thread(launch,())
        
    def exitApp(self,evt):
        """A function to quit the app"""
        print "exit"
        sys.exit()
        
    def SkiptoEndingFrame(self,evt):
        """Skip to Ending frame without recording"""
        frameBegin.Hide()
        frameEnd.Show()
        
    def engageRecording(self,evt):
        """Confirms and engage recording"""
        global live
        #print "tryFocus dans engageRecording  :::::::::",tryFocus
        if  live==True:
            live=liveFeed.GetValue()
        print  "Live ordered ?  ",live
        if tryFocus==False:
            #start_new_thread(recordNow,())
            recordNow()#try it out of thread for VideoCapture
            self.Hide()

class EndingFrame(wx.Frame):
    """An ending frame which also enable to publish the recordings on a webserver"""
    def __init__(self, parent, title):
        """Create the ending frame"""
        global entry1,entry2,entry25,entry3,entry4,entryNom,entryPrenom,entryCode
        windowXsize=500
        fieldSize=420
        if standalone==True:
            windowXsize=500
            fieldSize=420           
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(windowXsize, 560),
            style=wx.DEFAULT_FRAME_STYLE ^ (wx.CLOSE_BOX|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))
            
        # Status bar
        self.statusBar=self.CreateStatusBar()
        self.statusBar.SetStatusText(_("Status bar"))
        panel=wx.Panel(self)
        #panel.SetBackgroundColour("steel blue")
        #print wx.lib.colourdb.getColourList()
        panel.SetBackgroundColour((244,180,56))
        #panel.SetBackgroundColour((231,138,43))
        im1 = wx.Image('images/ban1.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        
        textTitre = wx.StaticText(panel, -1, _("Title:"),size=(400,-1),style=wx.ALIGN_CENTER)
        entry1 = wx.TextCtrl(panel, -1,"", size=(fieldSize, -1))
        #textTitre.SetBackgroundColour("steel blue") 
        #textTitre.SetForegroundColour("white")
        textDescription = wx.StaticText(panel, -1, _("Eventual description:"),
        size=(400,-1),style=wx.ALIGN_CENTER)
        entry2 = wx.TextCtrl(panel, -1,"", size=(fieldSize, -1))
        textNom= wx.StaticText(panel, -1, _("Name:"),size=(400,-1),style=wx.ALIGN_CENTER)
        entryNom = wx.TextCtrl(panel, -1,"", size=(fieldSize, -1))
        textPrenom= wx.StaticText(panel, -1, _("First name:"),size=(400,-1),style=wx.ALIGN_CENTER)
        entryPrenom = wx.TextCtrl(panel, -1,"", size=(fieldSize, -1))
        text4 = wx.StaticText(panel, -1, _("Degree:"),size=(400,-1),style=wx.ALIGN_CENTER)
        entry4 = wx.TextCtrl(panel,-1,"", size=(fieldSize, -1))
        #text25= wx.StaticText(panel, -1, "Nom et pr?nom : ")
        #text3 = wx.StaticText(panel, -1, "Votre identifiant ENT (si vous en avez un) : ")
        textCode=wx.StaticText(panel,-1, _("Access Code if you wish to set a limited access:"),
        size=(400,-1),style=wx.ALIGN_CENTER)
        entryCode = wx.TextCtrl(panel,-1,"", size=(fieldSize, -1))
        #text.SetSize(text.GetBestSize())
        #entry25 = wx.TextCtrl(panel, -1,"", size=(fieldSize, -1))
        #entry3=wx.TextCtrl(panel,-1,"", size=(fieldSize, -1))
        
        text0=hl.HyperLinkCtrl(panel, wx.ID_ANY, (_("Access to")+" audiovideocours.u-strasbg.fr"),
        URL="http://audiovideocours.u-strasbg.fr/",size=(300,-1),style=wx.ALIGN_CENTER)
        text0.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL,wx.NORMAL, False,'Arial'))
        
        #text0.SetVisitedColour("#0080ff")
        text0.SetForegroundColour("white")
        #text0.SetBackgroundColour("sky blue")
        text0.SetColours("white", "white", "white")
        
        
        for label in [textTitre,textDescription,textNom,textPrenom,text4,textCode]:
            label.SetForegroundColour("white")
            label.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL,wx.BOLD, False,"MS Sans Serif"))
        for entry in [entry1,entry2,entryNom,entryPrenom,entry4,entryCode]:
            #entry.SetBackgroundColour((254,236,170))
            #entry.SetBackgroundColour("light blue")
            pass
        
        btn = wx.Button(panel, -1, _("Publish!"),size=(130,50))
        btnCancel=wx.Button(panel, -1, _("Cancel"),size=(70,50))
        
        if standalone==True :
            btnPreview=wx.Button(panel, -1, _("Read"),size=(70,50))
            btnQuit=wx.Button(panel,-1,_("Quit"),size=(70,50))
            btnOpen=wx.Button(panel,-1,_("Open"),size=(70,50))
            
        hbox=wx.BoxSizer()
        hbox.Add(btn,proportion=0,flag=wx.RIGHT,border=5)
        hbox.Add(btnCancel,proportion=0,flag=wx.RIGHT,border=5)
        
        if standalone==True :
            hbox.Add(btnPreview,proportion=0,flag=wx.RIGHT,border=5)
            hbox.Add(btnOpen,proportion=0,flag=wx.RIGHT,border=5)
            hbox.Add(btnQuit,proportion=0,flag=wx.RIGHT,border=5)
        pad1=4    
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticBitmap(panel, -1, im1, (5, 5)), 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #sizer.Add(nameBox, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        sizer.Add(textTitre, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(entry1, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(textDescription, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(entry2, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        #sizer.Add(text25, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        #sizer.Add(entry25, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizer.Add(textNom, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(entryNom, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(textPrenom, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(entryPrenom, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(text4, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(entry4, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(textCode, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(entryCode, 0, wx.ALIGN_CENTER|wx.ALL, pad1)
        sizer.Add(hbox, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizer.Add(text0, 0, wx.ALIGN_CENTER|wx.ALL, 4)
        panel.SetSizer(sizer)
        panel.Layout() # what for ?
        
        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.publish, btn)
        self.Bind(wx.EVT_BUTTON, self.exitPublish, btnCancel)
        
        if standalone==True :
            self.Bind(wx.EVT_BUTTON, self.readPreview, btnPreview)
            self.Bind(wx.EVT_BUTTON, self.exitApp, btnQuit)
            self.Bind(wx.EVT_BUTTON, self.openOldOne, btnOpen)
            
    def openOldOne(self,evt):
        """
        Open an old recording for latter playing or publishing
        """
        global workDirectory,dirName
        openSmil=wx.FileDialog(self)
        print "pathData=",pathData
        if pathData=="":
            pathData==os.getcwd()
        openSmil.SetDirectory(pathData)
        openSmil.SetWildcard("*.smil")
        openSmil.ShowModal()
        toPlay= openSmil.GetFilenames()
        dirName=os.path.basename(openSmil.GetDirectory())
        print "dirName=",dirName
        workDirectory=openSmil.GetDirectory()
    
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
        writeInLogs("- 'Cancel' button pressed at"+ \
        str(datetime.datetime.now())+"\n")
        folder="canceled"
        if tryFocus==False:
            self.Hide()
            if standalone == True:
                frameBegin.Show()
        if standalone==False:
            global entry1,entry2,entry25,entry3,entry4,entryNom,entryPrenom
            global title,description,firstname,name,ue,login
            title= entry1.GetValue()
            description=entry2.GetValue()
            name=entryNom.GetValue()
            firstname=entryPrenom.GetValue()
            ue=entry4.GetValue()
            genre=entryCode.GetValue()
            #login=entry3.GetValue()
            print "tile: ",title
            print "description: ",description
            print "name: ",name
            print "ue: ",ue
            print "pr?nom: ",firstname
            start_new_thread(confirmPublish,(folder,))
            
        entry1.SetValue("")
        entry2.SetValue("")
        entryNom.SetValue("")
        entryPrenom.SetValue("")
        #genre.SetValue("")
        #entry3.SetValue("")
        entry4.SetValue("")

    def readPreview(self,evt):
        """Read the smil 'recording' file (audio or video + screenshots)"""
        def readSmilNow():
            #realPath=r'C:\"Program Files"\Real\RealPlayer\realplay.exe '
            #arguments=" file://"+workDirectory+"/cours.smil"
            if dirName =="":
                frameEnd.statusBar.SetStatusText(_("Nothing to read."))
            if workDirectory!="":
                #os.system("realplay.exe file://"+workDirectory+"/cours.smil") #works
                subprocess.Popen(["realplay.exe", "file://"+workDirectory+"/cours.smil"])
                
        start_new_thread(readSmilNow,())
        
    def publish(self,evt):
        """Publish the recording on the website"""
        writeInLogs("- 'Publish' button pressed at"+ \
        str(datetime.datetime.now())+"\n")
        if tryFocus==False:
            global title,description,name,firstname, ue,genre
            title= entry1.GetValue()
            description=entry2.GetValue()
            name=entryNom.GetValue()
            firstname=entryPrenom.GetValue()
            ue=entry4.GetValue()
            genre=entryCode.GetValue()
            #login=entry3.GetValue()
            print "tile : ",title
            print "description: ",description
            print "name: ",name
            print "prenom: ",firstname
            print "ue: ",ue
            entry1.SetValue("")
            entry2.SetValue("")
            entryNom.SetValue("")
            entryPrenom.SetValue("")
            entryCode.SetValue("")
            entry4.SetValue("")
            if standalone !=True:
                self.Hide()
            start_new_thread(confirmPublish,())
            #confirmPublish()
    
## Start app

if __name__=="__main__":
    
    # Start-up message
    print "UAudioVideoCours launched at ", datetime.datetime.now(), " ...\n"
    writeInLogs("\n\n>>> UAudioVideoCours launched at "+ \
    str(datetime.datetime.now())+"\n")
    # Read configuration file
    readConfFile()
    # Set-up language
    if language=="French":
        try:
            print "Setting French language..."
            langFr = gettext.translation('mediacours', "locale",languages=['fr'])
            langFr.install()
        except:
            print "something went wrong while setting French language"
        
    # Set-up videoprojector
    if videoprojectorInstalled==True:
        videoprojector=Videoprojector()
    # Start socket server
    if socketEnabled==True:
        start_new_thread(LaunchSocketServer,())
    # Write mediacours PID in a file (for use in the automatic updater) 
    PID_f=open("PID_mediacours.txt",'w')
    PID_f.write(str(os.getpid()))
    PID_f.close()
       
    
    ## GUI launch
    
    frameBegin=BeginFrame(None,title="Attention")
    #frameBegin.Show() # For debug
    frameBegin.Show()
    if standalone != True: frameBegin.Hide()
    frameEnd=EndingFrame(None,title="Attention")
    frameEnd.Show()
    frameEnd.Hide()
    #frameEnd.Show() # For debug
    
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
        
    app.MainLoop()
