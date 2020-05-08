[Cmdletbinding()]
param
(  
    [alias("c")][switch] $cPython = $false,
    [alias("w")][switch] $WinPython = $false
)

$curPython = cmd /c ftype Python.File 
if ($cPython) {
    # cmd /c ftype Python.File=C:\Windows\py.exe `"%1`" %*
    if ( -not ($curPython -eq "Python.File=C:\Users\yihoze\AppData\Local\Programs\Python\Python38\python.exe %1 %*") )
    {
        start-process powershell -Verb runAS "cmd /c ftype Python.File=`"C:\Users\yihoze\AppData\Local\Programs\Python\Python38\python.exe`" `"%1`" %*"
    }
} elseif ($WinPython) {    
    if ( -not ($curPython -eq "Python.File=C:\WinPython-64bit-3.5.4.1Qt5\python-3.5.4.amd64\python.exe %1 %*") ) 
    {
        start-process powershell -Verb runAS "cmd /c ftype Python.File=`"C:\WinPython-64bit-3.5.4.1Qt5\python-3.5.4.amd64\python.exe`" `"%1`" %*"
    }
} else {    
    write-host $curPython
}