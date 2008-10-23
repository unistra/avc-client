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

import os,subprocess, codecs

class FMEcmd(object):
    """Command FlashMediaEncoder FMDcmd.exe from Python"""
    
    def __init__(self,videoDeviceName,audioDeviceName,flvPath,liveParams,externalProfile,usage="video",live=False):
        print "in FMEcmd, received videoDeviceName",videoDeviceName,"audioDeviceName",audioDeviceName
        print "externalProfile=",externalProfile
        print "### flvPath is ", flvPath
        self.flvPath=flvPath
        self.usage=usage
        
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
<codec>VP6</codec>
<datarate>200</datarate>
<advanced>
<keyframe_frequency>5 seconds</keyframe_frequency>
<quality>Good Quality - Good Framerate</quality>
<noise_reduction>None</noise_reduction>
<datarate_window>Medium</datarate_window>
<cpu_usage>Dedicated</cpu_usage>
</advanced>
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
            
        self.profileHead=u"""
<?xml version="1.0" encoding="UTF-16"?>
<flashmediaencoder_profile>
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
<directory>C:\</directory>
</log>
</flashmediaencoder_profile>
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
        fileOut=open("flv_startup.xml","wb")
        fileOut.write(self.profile.encode("UTF-16"))
        fileOut.close

    def record(self):
        """Record the flv video using the FMEcmd.exe"""
        subprocess.Popen(["FMEcmd.exe", "/P","flv_startup.xml"])
        
    def stop(self,FMEpid):
        """Kill the FlashMediaEncoder"""
        #os.popen("taskkill /F /IM FMEcmd.exe")
        print 'Ordering: FMEcmd.exe /s "%s" ' % FMEpid
        os.popen('FMEcmd.exe /s "%s"' % FMEpid)
        if 0:
            # Checking for an artefact "enregistrement-micro.flv" file to erase in live audio mode
            artefact=self.flvPath.split(".mp3")[0]+".flv"
            print "Trying to delete ", artefact
            if self.usage=="audio" and os.path.isfile(artefact):
                os.system('del "%s"' % artefact)


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
    
    


    
    
    
    