; Install file for audiovideocast - formely audiovideocours (mediacours.py)
; (C) Universtiy of Strasbourg - UDS
;  Developer : f. schnell


[Setup]
AppName=audiovideocast
AppId=audiovideocast
AppVerName=audiovideocast 2.5
AppVersion=2.5
AppPublisher=(C) University of Strasbourg 2006-2014
AppPublisherURL=http://www.unistra.fr
AppSupportURL=http://www.unistra.fr
AppUpdatesURL=http://www.unistra.fr
DefaultDirName={pf}\AudioCours
DefaultGroupName=AudioVideoCast
LicenseFile=..\readme.txt
OutputDir=Output
;PrivilegesRequired=admin
;AppendDefaultDirName=false

[Dirs]
;Name: {app}\pywinauto
Name: {app}\locale
Name: {app}\locale\fr
Name: {app}\locale\fr\LC_MESSAGES
Name: {%USERPROFILE}\audiovideocours
Name: {%ALLUSERSPROFILE}\audiovideocours ; Permissions: everyone-modify
Name: {app}\thirdparty

[Files]
;Source: ..\mediacours.conf.default; DestDir:{%USERPROFILE}
;Source: ..\mediacours.conf; DestDir:{%USERPROFILE}
Source: ..\mediacours.conf; DestDir:{%ALLUSERSPROFILE}\audiovideocours ; Permissions: everyone-modify
Source: ..\images\audiocours1.ico; DestDir:{app}\images
Source: ..\images\audiocours2.ico; DestDir:{app}\images
Source: ..\images\videocours1.ico; DestDir:{app}\images
Source: ..\images\videocours2.ico; DestDir:{app}\images
Source: ..\images\ban1.jpg; DestDir:{app}\images
Source: ..\readme.txt; DestDir:{app}
Source: ..\Aide_AudioCours_StandAlone.url; DestDir:{%USERPROFILE}\audiovideocours
;Source: ..\changelog.txt; DestDir:{app}
Source: ..\AudioVideoCours.url; DestDir:{app}

; Translations
Source: ..\mediacours.pot; DestDir:{app}
Source: ..\locale\fr\LC_MESSAGES\mediacours.mo; DestDir:{app}\locale\fr\LC_MESSAGES
Source: ..\locale\fr\LC_MESSAGES\mediacours.po; DestDir:{app}\locale\fr\LC_MESSAGES

; Third party
Source: ..\ffmpeg.exe; DestDir:{app}
Source: ..\thirdparty\player.swf; DestDir:{app}\thirdparty
Source: ..\thirdparty\swfobject.js; DestDir:{app}\thirdparty
Source: ..\thirdparty\README.txt; DestDir:{app}\thirdparty
Source: ..\thirdparty\mp3splt.exe; DestDir:{app}\thirdparty
;Source: ..\thirdparty\JSFX_ImageZoom.js; DestDir:{app}\thirdparty

; Import files from py2exe build
Source: ..\dist\_ctypes.pyd; DestDir:{app}
Source: ..\dist\_elementtree.pyd; DestDir:{app}
Source: ..\dist\_hashlib.pyd; DestDir:{app}
Source: ..\dist\_imaging.pyd; DestDir:{app}
Source: ..\dist\_socket.pyd; DestDir:{app}
Source: ..\dist\_ssl.pyd; DestDir:{app}
Source: ..\dist\_tkinter.pyd; DestDir:{app}
Source: ..\dist\_win32sysloader.pyd; DestDir:{app}
Source: ..\dist\bz2.pyd; DestDir:{app}
Source: ..\dist\library.zip; DestDir:{app}
Source: ..\dist\mediacours.exe; DestDir:{app}
Source: ..\dist\perfmon.pyd; DestDir:{app}
Source: ..\dist\PIL._imaging.pyd; DestDir:{app}
Source: ..\dist\pyexpat.pyd; DestDir:{app}
Source: ..\dist\pyHook._cpyHook.pyd; DestDir:{app}
Source: ..\dist\pymedia.audio.acodec.pyd; DestDir:{app}
Source: ..\dist\pymedia.audio.sound.pyd; DestDir:{app}
Source: ..\dist\pymedia.muxer.pyd; DestDir:{app}
Source: ..\dist\pymedia.removable.cd.pyd; DestDir:{app}
Source: ..\dist\pymedia.video.vcodec.pyd; DestDir:{app}
Source: ..\dist\python27.dll; DestDir:{app}
Source: ..\dist\pythoncom27.dll; DestDir:{app}
Source: ..\dist\pywintypes27.dll; DestDir:{app}
Source: ..\dist\select.pyd; DestDir:{app}
Source: ..\dist\servicemanager.pyd; DestDir:{app}
Source: ..\dist\tcl85.dll; DestDir:{app}
Source: ..\dist\tk85.dll; DestDir:{app}
Source: ..\dist\unicodedata.pyd; DestDir:{app}
Source: ..\dist\w9xpopen.exe; DestDir:{app}
Source: ..\dist\win32api.pyd; DestDir:{app}
Source: ..\dist\win32event.pyd; DestDir:{app}
Source: ..\dist\win32evtlog.pyd; DestDir:{app}
Source: ..\dist\win32service.pyd; DestDir:{app}
Source: ..\dist\winsound.pyd; DestDir:{app}
Source: ..\dist\wx._controls_.pyd; DestDir:{app}
Source: ..\dist\wx._core_.pyd; DestDir:{app}
Source: ..\dist\wx._gdi_.pyd; DestDir:{app}
Source: ..\dist\wx._misc_.pyd; DestDir:{app}
Source: ..\dist\wx._windows_.pyd; DestDir:{app}
Source: ..\dist\wxbase30u_net_vc90.dll; DestDir:{app}
Source: ..\dist\wxbase30u_vc90.dll; DestDir:{app}
Source: ..\dist\wxmsw30u_adv_vc90.dll; DestDir:{app}
Source: ..\dist\wxmsw30u_core_vc90.dll; DestDir:{app}
Source: ..\dist\wxmsw30u_html_vc90.dll; DestDir:{app}
;Source: ..\dist\; DestDir:{app}
;Source: ..\dist\; DestDir:{app}
;Source: ..\dist\; DestDir:{app}
;Source: ..\dist\; DestDir:{app}
;Source: ..\dist\; DestDir:{app}
;Source: ..\dist\; DestDir:{app}
;Source: ..\dist\; DestDir:{app}
;Source: ..\dist\; DestDir:{app}
;Source: ..\dist\; DestDir:{app}
;Source: ..\dist\; DestDir:{app}



; OLD WHEN WAS ON XP BOX
; Import files from py2exe build
;Source: ..\dist\avc-win-shutdown.exe; DestDir:{app}
;Source: ..\dist\_controls_.pyd; DestDir:{app}
;Source: ..\dist\_core_.pyd; DestDir:{app}
;Source: ..\dist\_cpyHook.pyd; DestDir:{app}
;Source: ..\dist\_ctypes.pyd; DestDir:{app}
;Source: ..\dist\_gdi_.pyd; DestDir:{app}
;Source: ..\dist\_imaging.pyd; DestDir:{app}
;Source: ..\dist\_misc_.pyd; DestDir:{app}
;Source: ..\dist\_sendkeys.pyd; DestDir:{app}
;Source: ..\dist\_socket.pyd; DestDir:{app}
;Source: ..\dist\_ssl.pyd; DestDir:{app}
;Source: ..\dist\_win32sysloader.pyd; DestDir:{app}
;Source: ..\dist\_windows_.pyd; DestDir:{app}
;Source: ..\dist\acodec.pyd; DestDir:{app}
;Source: ..\dist\bz2.pyd; DestDir:{app}
;Source: ..\dist\cd.pyd; DestDir:{app}
;Source: ..\dist\library.zip; DestDir:{app}
;Source: ..\dist\mediacours.exe; DestDir:{app}
;Source: ..\dist\MSVCR71.dll; DestDir:{app}
;Source: ..\dist\muxer.pyd; DestDir:{app}
;Source: ..\dist\pyexpat.pyd; DestDir:{app}
;Source: ..\dist\python24.dll; DestDir:{app}
;Source: ..\dist\pythoncom24.dll; DestDir:{app}
;Source: ..\dist\pywintypes24.dll; DestDir:{app}
;Source: ..\dist\select.pyd; DestDir:{app}
;Source: ..\dist\sound.pyd; DestDir:{app}
;Source: ..\dist\unicodedata.pyd; DestDir:{app}
;Source: ..\dist\vcodec.pyd; DestDir:{app}
;Source: ..\dist\w9xpopen.exe; DestDir:{app}
;Source: ..\dist\win32event.pyd; DestDir:{app}
;Source: ..\dist\win32file.pyd; DestDir:{app}
;Source: ..\dist\zlib.pyd; DestDir:{app}
;Source: ..\dist\winsound.pyd; DestDir:{app}
;Source: ..\dist\wxbase28h_net_vc.dll; DestDir:{app}
;Source: ..\dist\wxbase28h_vc.dll; DestDir:{app}
;Source: ..\dist\wxmsw28h_adv_vc.dll; DestDir:{app}
;Source: ..\dist\wxmsw28h_core_vc.dll; DestDir:{app}
;Source: ..\dist\wxmsw28h_html_vc.dll; DestDir:{app}
; asked from herve and eric to include msvcp71.dll
;Source: ..\dist\msvcp71.dll; DestDir:{app}



[Run]

[Languages]
Name: Francais; MessagesFile: compiler:Languages\French.isl
Name: Anglais; MessagesFile: compiler:Default.isl
Name: Allemand; MessagesFile: compiler:Languages\German.isl

[Icons]
Name: {group}\AudioVideoCast; Filename: {app}\mediacours.exe; WorkingDir: {app}; IconFilename: {app}\images\audiocours2.ico
Name: {commondesktop}\AudioVideoCast; Filename: {app}\mediacours.exe; WorkingDir: {app}; IconFilename: {app}\images\audiocours1.ico
;Name: {group}\Dossier Cours; Filename: {app}\Cours\local\Media
Name: {group}\Site web Audiovideocast; Filename: {app}\AudioVideoCours.url; WorkingDir: {app}
Name: {group}\Desinstaller AudioVideoCast; Filename: {uninstallexe}; IconFilename: {app}\unins000.exe; WorkingDir: {app}

[Registry]

[InstallDelete]
Name: {tmp}; Type: filesandordirs

[UninstallDelete]

[Code]

