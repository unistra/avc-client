###############################################################################
 This is a README file for the "client" and "standalone" part of the audiovideocours project
 
Audiovideocours is released under the Free Software GPL license
 ###############################################################################
 
This README describes the main files of this folder mainly for an audio usage under a Windows platform (Linux version will come soon).
 
1) mediacours.conf.default
 
Is a template configuration file for  audiovideocours.  You can custom it and save it as "mediacours.conf" (if you use MediaCours.py script) or "mediacoursExt.conf" (if you use MediaCoursEX.py script). Read the comments in the configuration file to see what you can set.
 
2) MediaCours.py
 
Is the main file of the application. It will automatically take a screenshot of the PC at each mouse event and relevant keyboard events.
 You can find a build of this version here:
 http://audiovideocours.u-strasbg.fr/telechargement/index.jsp
 
3) MediaCoursEX.py
 
Has the same features as audiovideocours but in a none intrusive "EXternal" way. It means you don't need to install the software on the PC or laptops of the users but it requires a video  acquisition card feed by a  VGA converter.

It is useful for example for teacher's coming with their laptops whatever their operating system.
 
4) videolog.py
 
Is a script developed for the external version of audiovideocours but which can also be used as a standalone script. 
It compares the video input and automatically detect when the picture sufficiently change to save a new screenshot.
http://ulpmm-projets.u-strasbg.fr/projets/videocours/browser/trunk/client_and_standalone/videolog.py

4) Windows build

setup.py is the py2exe script to produce a Windows executable. The installer is done using Inno Setup 
(see win-installer build)
