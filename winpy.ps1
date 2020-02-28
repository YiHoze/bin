# With the -a option, this script must be run as admin.
[Cmdletbinding()]
param
(  
  [alias("c")][switch] $cPython = $false,
  [alias("a")][switch] $assoc = $false
)

if ($cPython) {
    if($assoc) {
      cmd /c ftype Python.File=`"C:\Program Files\Python37\python.exe`" `"%1`" %*
    }
    $env:path = "C:\Program Files\Python37;C:\Program Files\Python37\Scripts;C:\home\bin\pandoc;$env:path"
    userpath.ps1
} else {
    if($assoc) { 
      cmd /c ftype Python.File=`"C:\WinPython-64bit-3.5.4.1Qt5\python-3.5.4.amd64\python.exe`" `"%1`" %*
    }
    powershell -noexit "C:\WinPython-64bit-3.5.4.1Qt5\scripts\WinPython_PS_Prompt.ps1"    
}