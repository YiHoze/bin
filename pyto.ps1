[Cmdletbinding()]
param
(  
    [alias("w")][switch] $WinPython = $false
)

if ($WinPython) 
{
    C:\WinPython-64bit-3.5.4.1Qt5\scripts\WinPython_PS_Prompt.ps1
} 
else 
{
    $env:path = "C:\Users\yihoze\AppData\Local\Programs\Python\Python38;C:\Users\yihoze\AppData\Local\Programs\Python\Python38\Scripts;C:\home\bin\pandoc;$env:path"
}
chcp 65001
$env:path.split(";")
python -V
