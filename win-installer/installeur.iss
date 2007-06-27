; Install file for audiovideocours (mediacours.py)
; (C) ULP Multimedia (University Louis-Pasteur)
;  Developer : francois schnell


[Setup]
AppName=audiovideocours
AppId=audiovideocours
AppVerName=audiovideocours 0.85
AppVersion=0.85
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
;Name: {app}\Cours\local
;Name: {app}\Cours\local\Media
;Name: {app}\Cours\local\Profil
;Name: {app}\Cours\local\Media\Slides
;Name: {app}\Serveur; attribs: hidden

[Files]
;Source: lib\python-2.4.3.msi; DestDir: {tmp}
;Source: lib\PIL-1.1.5.win32-py2.4.exe; DestDir: {tmp}
;Source: lib\pyHook-1.4.win32-py2.4.exe; DestDir: {tmp}
;Source: lib\pywin32-210.win32-py2.4.exe; DestDir: {tmp}
;Source: lib\pymedia-1.3.7.2.win32-py2.4.exe; DestDir: {tmp}
;Source: lib\pyserial-2.2.win32.exe; DestDir: {tmp}
;Source: lib\wxPython2.6-win32-ansi-2.6.3.3-py24.exe; DestDir: {tmp}
;Source: lib\ctypes-1.0.0.win32-py2.4.exe; DestDir: {tmp}
;Source: lib\SendKeys-0.3.win32-py2.4.exe; DestDir: {tmp}
;Source: UnivrAudioCoursPM.pyw; DestDir:{app}
;Source: UnivrAudioCoursPM.pyc; DestDir:{app}
;Source: mediacours.pyc; DestDir:{app}
;Source: ..\mediacours.conf; DestDir:{app}
Source: ..\mediacours.conf; DestDir:{%USERPROFILE}
;Source: lib\pywinauto.exe; DestDir:{app}
;Source: univraudiocours.conf; DestDir:{app}
Source: ..\audiocours1.ico; DestDir:{app}
Source: ..\audiocours2.ico; DestDir:{app}
Source: ..\videocours1.ico; DestDir:{app}
Source: ..\videocours2.ico; DestDir:{app}
Source: ..\ban1.jpg; DestDir:{app}
Source: ..\readme.txt; DestDir:{app}
Source: ..\changelog.txt; DestDir:{app}
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

;Source: lib\ijl11.dll; DestDir: {sys}; Flags: onlyifdoesntexist
;Source: lib\ijl15.dll; DestDir: {sys}; Flags: onlyifdoesntexist
;Source: lib\VB6FR.DLL; DestDir: {sys}; Flags: onlyifdoesntexist
;Source: lib\MSVCRTD.DLL; DestDir: {sys}; Flags: onlyifdoesntexist
;Source: lib\MSVCP60D.DLL; DestDir: {sys}; Flags: onlyifdoesntexist
;Source: lib\xerces-c_1_7_0D.dll; DestDir: {sys}; Flags: onlyifdoesntexist
;Source: lib\jre-1_5_0-windows-i586.exe; DestDir: {tmp}
;Source: lib\WMEDist.exe; DestDir: {tmp}
;Source: oth\append_client_config.exe; DestDir: {tmp}
;Source: oth\append_server_config.exe; DestDir: {tmp}
;Source: oth\SetACL.exe; DestDir: {tmp}
;Source: oth\config_maker.exe; DestDir: {tmp}
;Source: oth\script_maker.exe; DestDir: {tmp}
;Source: src\server.exe; DestDir: {app}\Serveur; Flags: ignoreversion
;Source: src\archivage.exe; DestDir: {app}\Serveur; Flags: ignoreversion
;Source: src\wmv2xml.exe; DestDir: {app}\Serveur; Flags: ignoreversion
;Source: src\wmvcopy.exe; DestDir: {app}\Serveur; Flags: ignoreversion
;Source: src\ScriptToHeader.exe; DestDir: {app}\Serveur; Flags: ignoreversion
;Source: src\local.wme; DestDir: {app}\Cours\local\Profil; Flags: ignoreversion
;Source: src\clients.txt; DestDir: {app}; Flags: ignoreversion
;Source: src\config.txt; DestDir: {app}; Flags: ignoreversion
;Source: src\server.txt; DestDir: {app}; Flags: ignoreversion
;Source: src\archivage.log; DestDir: {app}\Serveur; Flags: ignoreversion
;Source: src\server.log; DestDir: {app}; Flags: ignoreversion
;Source: src\audio.ico; DestDir: {app}
;Source: src\dinput.pyw; DestDir: {app}; Attribs: hidden
;Source: src\photo.wav; DestDir: {app}; Attribs: hidden
;Source: src\ClientEncodage.jar; DestDir: {app}

[Run]
;Filename: {sys}\msiexec.exe; Parameters: "/i ""{tmp}\python-2.4.3.msi"""; Check: TestPython24; StatusMsg: Installation de l'environnemenent Python 2.4.3 ...
;Filename: {tmp}\PIL-1.1.5.win32-py2.4.exe; StatusMsg: Installation de la libriarie PIL (Pyhton)...
;Filename: {tmp}\pyHook-1.4.win32-py2.4.exe; StatusMsg: Installation de la libriarie PyHook (Pyhton)...
;Filename: {tmp}\pywin32-210.win32-py2.4.exe; StatusMsg: Installation de la libriarie pywin32 (Pyhton)...
;Filename: {tmp}\pymedia-1.3.7.2.win32-py2.4.exe; StatusMsg: Installation de la libriarie pymedia (Pyhton)...
;Filename: {tmp}\pyserial-2.2.win32.exe; StatusMsg: Installation de la libriarie pyserial (Pyhton)...
;Filename: {tmp}\ctypes-1.0.0.win32-py2.4.exe; StatusMsg: Installation de la libriarie ctypes (Pyhton)...
;Filename: {tmp}\SendKeys-0.3.win32-py2.4.exe; StatusMsg: Installation de la libriarie SendKeys (Pyhton)...
;Filename: {tmp}\wxPython2.6-win32-ansi-2.6.3.3-py24.exe; StatusMsg: Installation de la libriarie wxpython (Pyhton)...
;Filename: {app}\pywinauto.exe; StatusMsg: Installation de la libriarie pywinauto (Pyhton)...
;Filename: {tmp}\jre-1_5_0-windows-i586.exe; Check: TestPresenceLessJRE1_5; StatusMsg: Installation de Java Runtime Environment 1.5...
;Filename: {tmp}\WMEncoder.exe; StatusMsg: Installation de Windows Media Encoder 9 ...; Check: TestWME9
;Filename: {tmp}\append_client_config.exe; Parameters: """{app}\config.txt"" ""{app}\Cours\local\Media\Slides\\"""; StatusMsg: Configuration ...; Flags: runhidden
;Filename: {tmp}\append_server_config.exe; Parameters: """{app}\server.txt"" ""{app}\\"""; StatusMsg: Configuration ...; Flags: runhidden
;Filename: {tmp}\SetACL.exe; Parameters: "-on ""{app}"" -ot file -actn ace -ace ""n:S-1-1-0;p:full;s:y;"" -rec cont_obj"; StatusMsg: Configuration serveur...; Flags: runhidden
;Filename: {tmp}\SetACL.exe; Parameters: "-on ""{app}\Cours\local"" -ot file -actn ace -ace ""n:S-1-1-0;p:full;s:y;"" -rec cont_obj"; StatusMsg: Configuration des fichiers...; Flags: runhidden
;Filename: {tmp}\script_maker.exe; Parameters: """{code:pathJRE1_5}"" ""{app}"" ""{code:pathPython24}"""; StatusMsg: Configuration ...; Flags: runhidden; WorkingDir: {app}
;Filename: {tmp}\config_maker.exe; Parameters: """{app}"""; StatusMsg: Configuration ...; Flags: runhidden; WorkingDir: {app}

[Languages]
Name: Francais; MessagesFile: compiler:Languages\French.isl
Name: Anglais; MessagesFile: compiler:Default.isl
Name: Allemand; MessagesFile: compiler:Languages\German.isl

[Icons]
Name: {group}\AudioCours; Filename: {app}\mediacours.exe; WorkingDir: {app}; IconFilename: {app}\audiocours2.ico
Name: {commondesktop}\AudioCours; Filename: {app}\mediacours.exe; WorkingDir: {app}; IconFilename: {app}\audiocours1.ico
;Name: {group}\Dossier Cours; Filename: {app}\Cours\local\Media
Name: {group}\Site web audiovideocours; Filename: {app}\AudioVideoCours.url; WorkingDir: {app}
Name: {group}\Desinstaller AudioVideoCours; Filename: {uninstallexe}; IconFilename: {app}\unins000.exe; WorkingDir: {app}

[Registry]
;Root: HKLM; Subkey: Software\ULP Multimedia; Flags: uninsdeletekeyifempty
;Root: HKLM; Subkey: Software\ULP Multimedia\Audiocours; Flags: uninsdeletekey
;Root: HKLM; Subkey: Software\ULP Multimedia\Audiocours; ValueType: string; ValueName: Path; ValueData: {app}; Flags: uninsdeletevalue
;Root: HKLM; Subkey: Software\ULP Multimedia\Audiocours; ValueType: string; ValueName: Version; ValueData: 1.2.5; Flags: uninsdeletevalue

[InstallDelete]
Name: {tmp}; Type: filesandordirs

[UninstallDelete]
;Name: {app}\ClientEncodage.cmd; Type: files
;Name: {app}\dinput.log; Type: files
;Name: {app}\Cours\local\Profil; Type: filesandordirs
;Name: {app}\Cours\local\Visu; Type: dirifempty
;Name: {app}\Cours\local\Media\Slides; Type: dirifempty
;Name: {app}\Cours\local\Media; Type: dirifempty
;Name: {app}\Cours\local; Type: dirifempty
;Name: {app}\Cours; Type: dirifempty
;Name: {app}\Icons; Type: filesandordirs
;Name: {app}\Samples; Type: filesandordirs
;Name: {app}\Serveur; Type: filesandordirs
;Name: {app}\camera.ico; Type: files
;Name: {app}\clients.txt; Type: files
;Name: {app}\config.txt; Type: files
;Name: {app}\dinput.pyw; Type: files
;Name: {app}\EcouteServeur.class; Type: files
;Name: {app}\killer.exe; Type: files
;Name: {app}\photo.wav; Type: files
;Name: {app}\player_play.png; Type: files
;Name: {app}\player_stop.png; Type: files
;Name: {app}\Plop.class; Type: files
;Name: {app}\server.log; Type: files
;Name: {app}\server.txt; Type: files
;Name: {app}\audio.ico; Type: files

[Code]


function TestPython24: Boolean;
begin
if (RegKeyExists(HKLM, 'SOFTWARE\Python\PythonCore\2.4')) then
	begin
		Result := False;
	end
else
	begin
		Result := True;
	end;
end;

function TestDirectX9: Boolean;
var
	index: Byte;
	key: String;
begin
	RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\DirectX', 'Version', key);
	index := Pos('.09.', key);
	if(index = 0) then
		begin
			Result := True;
		end
	else
		begin
			Result := False;
		end;
end;

function TestWME9: Boolean;
begin
if (RegKeyExists(HKLM, 'SOFTWARE\Microsoft\Windows Media\Encoder\9.0')) then
	begin
		Result := False;
	end
else
	begin
		Result := True;
	end;
end;

function pathJRE1_5(Param: String): String;
begin
	RegQueryStringValue(HKLM, 'SOFTWARE\JavaSoft\Java Runtime Environment\1.5', 'JavaHome', Result);
end ;

function pathPython24(Param: String): String;
begin
	RegQueryStringValue(HKLM, 'SOFTWARE\Python\PythonCore\2.4\InstallPath', '', Result);
end ;
