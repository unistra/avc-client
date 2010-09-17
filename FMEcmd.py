###############################################################################
#  Developper: Francois Schnell - ULP Multimedia 
#  GPL v2
#
#  A script to automate FlashMediaEnocder v2(FMEcmd.exe -  commnande line) 
#  from Python without needing to open the FlashMediaEncoder GUI first
#
# The script will generate its own profile file "flv_startup.xml" in the same
# folder
#
# Note: Since version 2.5 of Flash Media Encoder, videoDeviceName,audioDeviceName
#       can be the full name or the input number
# 
# Flash Media Ecoder URL
# http://www.adobe.com/products/flashmediaserver/flashmediaencoder/
###############################################################################

import os,subprocess, codecs, time,wx
import  winsound #for tests
from pywinauto import application,findwindows

class FMEcmd(object):
    """Command FlashMediaEncoder FMDcmd.exe from Python"""
    
    def __init__(self,videoDeviceName,audioDeviceName,flvPath,liveParams,externalProfile,usage="video",live=False,pathData="C:\\"):
        print "### Now in FMEcmd\nreceived videoDeviceName",videoDeviceName,"audioDeviceName",audioDeviceName
        print "externalProfile is ",externalProfile
        print "flvPath is ", flvPath
        self.flvPath=flvPath
        self.usage=usage
        #self.logsDir=os.environ["USERPROFILE"]+"\\audiovideocours"
        self.pathData=pathData
        self.logsDir=pathData
        print "Flash Media Live Encoder logs will be here: ", self.logsDir
        
        if usage=="video":
            
            videoSource=u"""
<video>
<device>"""+videoDeviceName+u"""</device>
<crossbar_input>0</crossbar_input>
<frame_rate>15.00</frame_rate>
<size>
<width>320</width>
<height>240</height>
</size>
</video>"""

            videoEncode=u"""
<video>
<format>VP6</format>
<datarate>500;</datarate>
<outputsize>320x240;</outputsize>
<advanced>
    <keyframe_frequency>5 Seconds</keyframe_frequency>
    <quality>Good Quality - Good Framerate</quality>
    <noise_reduction>None</noise_reduction>
    <datarate_window>Medium</datarate_window>
    <cpu_usage>Dedicated</cpu_usage>
</advanced>
<autoadjust>
    <enable>false</enable>
    <maxbuffersize>1</maxbuffersize>
    <dropframes>
    <enable>false</enable>
    </dropframes>
    <degradequality>
    <enable>false</enable>
    <minvideobitrate></minvideobitrate>
    <preservepfq>false</preservepfq>
    </degradequality>
</autoadjust>
</video>"""
            
        elif usage=="audio":           
            videoSource=""
            videoEncode=""
        
        if live==True and usage=="audio":
            outputFile=""
        else:
            outputFile="""<file>
<path>"""+flvPath+u"""</path>
</file>"""
            
        self.profileHead=u"""<?xml version="1.0" encoding="UTF-16"?>
<flashmedialiveencoder_profile>
<preset>
<name>Medium Bandwidth (300 Kbps)</name>
<description></description>
</preset>
<capture>"""+\
videoSource+"""
<audio>
<device>""" +audioDeviceName+u"""</device>
<crossbar_input>0</crossbar_input>
<sample_rate>22050</sample_rate>
<channels>1</channels>
<input_volume>75</input_volume>
</audio>
</capture>
<encode>"""\
+videoEncode +\
"""
<audio>
<format>Mp3</format>
<datarate>48</datarate>
</audio>
</encode>
<restartinterval>
<days></days>
<hours></hours>
<minutes></minutes>
</restartinterval>
<reconnectinterval>
<attempts></attempts>
<interval></interval>
</reconnectinterval>"""

        self.profileOutput=u"""<output>
"""+liveParams+outputFile+"""
</output>"""

        self.profileTail=u"""<metadata>
<entry>
<key>author</key>
<value></value>
</entry>
<entry>
<key>copyright</key>
<value></value>
</entry>
<entry>
<key>description</key>
<value></value>
</entry>
<entry>
<key>keywords</key>
<value></value>
</entry>
<entry>
<key>rating</key>
<value></value>
</entry>
<entry>
<key>title</key>
<value></value>
</entry>
</metadata>
<preview>
<video>
<input>
<zoom>100%</zoom>
</input>
<output>
<zoom>100%</zoom>
</output>
</video>
<audio></audio>
</preview>
<log>
<level>100</level>
<directory>"""+self.logsDir+"""</directory>
</log>
</flashmedialiveencoder_profile>
"""

        # check if an external profile exist and take profileHead in this case
        if externalProfile== True:
            print "Reading external profile"
            fP=codecs.open("startup.xml",encoding="utf-16-le")
            #fP=open("startup.xml","r")
            exProfile=u""
            for line in fP:
                exProfile+=line
            #print repr(exProfile)
            self.profileHead=exProfile.split(u"<output>")[0]
            #print self.profileHead
            fP.close()
        self.profile=self.profileHead+self.profileOutput+self.profileTail
        fileOut=open(self.pathData+"/flv_startup.xml","wb")
        fileOut.write(self.profile.encode("UTF-16"))
        fileOut.close

    def record(self):
        """ Launch FMEcmd.exe with the given profile. """
        winsound.Beep(500,50)
        FME='C:/Program Files/Adobe/Flash Media Live Encoder 3.1/FMLEcmd.exe'
        FMEwin7='C:/Program Files (x86)/Adobe/Flash Media Live Encoder 3.1/FMLEcmd.exe'
        try:
            subprocess.Popen(["%s"%FME,"/d","/P",self.pathData+"/flv_startup.xml"])
            print "Ordered sent to FMLE to begin recording:",FME 
        except:
            try:
                subprocess.Popen(["%s"%FMEwin7,"/d","/P",self.pathData+"/flv_startup.xml"])
                print "Ordered sent to FMLE to begin recording: ",FMEwin7
            except:
                try:
                    subprocess.Popen(["FMLEcmd.exe","/d","/P",self.pathData+"/flv_startup.xml"])
                    print "!!! after record second Try !!!"
                except:
                    print "Couldn't find C:\Program Files\Adobe\Flash Media Live Encoder 3.1\FMLEcmd.exe"
                    caption="Audiovideocours Error Message"
                    text="Problem while launching Flash Media Encoder.\n\n Is C:\Program Files\Adobe\Flash Media Live Encoder 3.1\FMLEcmd.exe exists?"+\
                    "\n If not install Flash Media Live Encoder 3.1" 
                    dialog=wx.MessageDialog(None,message=text,caption=caption,
                    style=wx.OK|wx.ICON_INFORMATION)
                    dialog.ShowModal()
        time.sleep(4)
        print "trying to minimize FMLEcmd.exe DOS window in task bar"
        try:
            appA = application.Application()
            appA.connect_(title_re = r".*FMLEcmd.exe")
            appA.window_(title_re = r".*FMLEcmd.exe").Minimize()
        except:
            for i in range(3):
                winsound.Beep(500,100)
                time.sleep(0.2)
            print "Couldn't find and minimize DOS window"
        
    def stop(self,FMLEpid):
        """Kill the FlashMediaEncoder"""
        print 'Ordering: FMLEcmd.exe /s "%s" ' % FMLEpid
        FME='C:/Program Files/Adobe/Flash Media Live Encoder 3.1/FMLEcmd.exe'
        FMEwin7='C:/Program Files (x86)/Adobe/Flash Media Live Encoder 3.1/FMLEcmd.exe'
        try:
            subprocess.Popen(["%s"%FME,"/s","%s" % FMLEpid])
        except:
            try:
                subprocess.Popen(["%s"%FMEwin7,"/s","%s" % FMLEpid])
            except:
                try:
                    subprocess.Popen(["FMLEcmd.exe","/s","%s" % FMLEpid])
                except:
                    print "Problem while stopping Flash Media Encoder"
                    caption="Audiovideocours Error Message"
                    text="Problem while stopping Flash Media Encoder.\n\nYou may have to stop 'FMEcmd' process manually."
                    dialog=wx.MessageDialog(None,message=text,caption=caption,
                    style=wx.OK|wx.ICON_INFORMATION)
                    dialog.ShowModal()
     
if __name__=="__main__":
    
    import time
    #You must give the exact name of the device by looking either in Windows or 
    # in the GUI version of Flash Media Encoder
    videoDeviceName="Philips ToUcam Pro Camera; Video"
    audioDeviceName="Appareil photo Philips ToUcam F"
    #FMEcmd doesn't take relative filename path
    #if so the video is saved by default in the video foler of the OS "My videos" 
    flvPath=r"C:\Documents and Settings\franz\Bureau\newsample.flv"
    
    # Example: record a 30 seconds video
    flv=FMEcmd(videoDeviceName,audioDeviceName,flvPath,liveParams="",externalProfile=False)
    flv.record()
    time.sleep(30)
    flv.stop()
    
    


    
    
    
    