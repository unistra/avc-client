; Install file for audiovideocours (mediacours.py)
; (C) ULP Multimedia (University Louis-Pasteur)
;  Developer : francois schnell


[Setup]
AppName=audiovideocours
AppId=audiovideocours
AppVerName=audiovideocours 0.93
AppVersion=0.93
AppPublisher=(C) ULP Multimedia 2007
AppPublisherURL=http://audiovideocours.u-strasbg.fr/
AppSupportURL=http://audiovideocours.u-strasbg.fr/
AppUpdatesURL=http://audiovideocours.u-strasbg.fr/
DefaultDirName={pf}\AudioCours
DefaultGroupName=AudioCours
LicenseFile=..\readme.txt
OutputDir=Output
;PrivilegesRequired=admin
;AppendDefaultDirName=false

[Dirs]
Name: {app}\pywinauto
Name: {app}\locale
Name: {app}\locale\fr
Name: {app}\locale\fr\LC_MESSAGES

[Files]
;Source: ..\mediacours.conf.default; DestDir:{%USERPROFILE}
;Source: ..\mediacours.conf; DestDir:{%USERPROFILE}
Source: ..\mediacours.conf; DestDir:{app}
Source: ..\images\audiocours1.ico; DestDir:{app}\images
Source: ..\images\audiocours2.ico; DestDir:{app}\images
Source: ..\images\videocours1.ico; DestDir:{app}\images
Source: ..\images\videocours2.ico; DestDir:{app}\images
Source: ..\images\ban1.jpg; DestDir:{app}\images
Source: ..\readme.txt; DestDir:{app}
;Source: ..\changelog.txt; DestDir:{app}
Source: ..\AudioVideoCours.url; DestDir:{app}

; Import files from py2exe build
Source: ..\dist\_controls_.pyd; DestDir:{app}
Source: ..\dist\_core_.pyd; DestDir:{app}
Source: ..\dist\_cpyHook.pyd; DestDir:{app}
Source: ..\dist\_ctypes.pyd; DestDir:{app}
Source: ..\dist\_gdi_.pyd; DestDir:{app}
Source: ..\dist\_imaging.pyd; DestDir:{app}
Source: ..\dist\_misc_.pyd; DestDir:{app}
Source: ..\dist\_sendkeys.pyd; DestDir:{app}
Source: ..\dist\_socket.pyd; DestDir:{app}
Source: ..\dist\_ssl.pyd; DestDir:{app}
Source: ..\dist\_win32sysloader.pyd; DestDir:{app}
Source: ..\dist\_windows_.pyd; DestDir:{app}
Source: ..\dist\acodec.pyd; DestDir:{app}
Source: ..\dist\bz2.pyd; DestDir:{app}
Source: ..\dist\cd.pyd; DestDir:{app}
Source: ..\dist\library.zip; DestDir:{app}
Source: ..\dist\mediacours.exe; DestDir:{app}
Source: ..\dist\MSVCR71.dll; DestDir:{app}
Source: ..\dist\muxer.pyd; DestDir:{app}
Source: ..\dist\pyexpat.pyd; DestDir:{app}
Source: ..\dist\python24.dll; DestDir:{app}
Source: ..\dist\pythoncom24.dll; DestDir:{app}
Source: ..\dist\pywintypes24.dll; DestDir:{app}
Source: ..\dist\select.pyd; DestDir:{app}
Source: ..\dist\sound.pyd; DestDir:{app}
Source: ..\dist\unicodedata.pyd; DestDir:{app}
Source: ..\dist\vcodec.pyd; DestDir:{app}
Source: ..\dist\w9xpopen.exe; DestDir:{app}
Source: ..\dist\win32event.pyd; DestDir:{app}
Source: ..\dist\win32file.pyd; DestDir:{app}
Source: ..\dist\wxmsw26h_vc.dll; DestDir:{app}
Source: ..\dist\zlib.pyd; DestDir:{app}

; Translations
Source: ..\mediacours.pot; DestDir:{app}
Source: ..\locale\fr\LC_MESSAGES\mediacours.mo; DestDir:{app}\locale\fr\LC_MESSAGES
Source: ..\locale\fr\LC_MESSAGES\mediacours.po; DestDir:{app}\locale\fr\LC_MESSAGES

[Run]

[Languages]
Name: Francais; MessagesFile: compiler:Languages\French.isl
Name: Anglais; MessagesFile: compiler:Default.isl
Name: Allemand; MessagesFile: compiler:Languages\German.isl

[Icons]
Name: {group}\AudioCours; Filename: {app}\mediacours.exe; WorkingDir: {app}; IconFilename: {app}\images\audiocours2.ico
Name: {commondesktop}\AudioCours; Filename: {app}\mediacours.exe; WorkingDir: {app}; IconFilename: {app}\images\audiocours1.ico
;Name: {group}\Dossier Cours; Filename: {app}\Cours\local\Media
Name: {group}\Site web audiovideocours; Filename: {app}\AudioVideoCours.url; WorkingDir: {app}
Name: {group}\Desinstaller AudioVideoCours; Filename: {uninstallexe}; IconFilename: {app}\unins000.exe; WorkingDir: {app}

[Registry]

[InstallDelete]
Name: {tmp}; Type: filesandordirs

[UninstallDelete]

[Code]

