' Run bot silently in background
Set objShell = CreateObject("WScript.Shell")
strPath = WScript.ScriptFullName
Set objFile = CreateObject("Scripting.FileSystemObject")
strFolder = objFile.GetParentFolderName(strPath)
objShell.Run "python bot.py", 0, False
