[Cmdletbinding()]
param
(  
    [alias("w")][switch] $WinPython = $false,
    [alias("a")][switch] $assoc = $false
)

if ($WinPython) 
{
    if ($assoc) { 
        $curPython = cmd /c ftype Python.File 
        if ( -not ($curPython -eq "Python.File=C:\WinPython-64bit-3.5.4.1Qt5\python-3.5.4.amd64\python.exe %1 %*") ) 
        {
            start-process powershell -Verb runAS "cmd /c ftype Python.File=`"C:\WinPython-64bit-3.5.4.1Qt5\python-3.5.4.amd64\python.exe`" `"%1`" %*"
        }
    }
    C:\WinPython-64bit-3.5.4.1Qt5\scripts\WinPython_PS_Prompt.ps1
} 
else 
{
    if ($assoc) {
        $curPython = cmd /c ftype Python.File 
        # cmd /c ftype Python.File=C:\Windows\py.exe `"%1`" %*
        if ( -not ($curPython -eq "Python.File=C:\Users\yihoze\AppData\Local\Programs\Python\Python38\python.exe %1 %*") )
        {
            start-process powershell -Verb runAS "cmd /c ftype Python.File=`"C:\Users\yihoze\AppData\Local\Programs\Python\Python38\python.exe`" `"%1`" %*"
        }
  }
  $env:path = "C:\Users\yihoze\AppData\Local\Programs\Python\Python38;C:\Users\yihoze\AppData\Local\Programs\Python\Python38\Scripts;C:\home\bin\pandoc;$env:path"
}
chcp 65001
$env:path.split(";")
python -V
