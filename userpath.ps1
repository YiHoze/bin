# userpath.ps1 -a "C:\Program Files\Python37\Scripts\"
# userpath.ps1 -a "C:\Program Files\Python37\"

[Cmdletbinding()]
param
(
  [alias("a")][switch] $append_bool = $false,
  [alias("r")][switch] $remove_bool = $false,
  [alias("s")][switch] $set_bool = $false,
  [alias("c")][switch] $admin_bool = $false,
  [alias("p")][switch] $system_properties_bool = $false,
  [alias("h")][switch] $help = $false,
  [String] $directory
)

function help()
{
  write-output "
  View the local PATH environment variable.
  Usage:
    userpath.ps1 [option] [directory]
  Options:
    -a: Append to the path
    -r: Remove from the path
    -s: Set to the path
    -p: Open the System Properties window
    -c: Check if running as administrator
    -h: help
  "
}

function CheckLocalAdmin()
{
  $result  = ([security.principal.windowsprincipal][security.principal.windowsidentity]::GetCurrent()).isinrole([Security.Principal.WindowsBuiltInRole] "Administrator")
  If ($result) {
    write-output "`n Running as administrator `n"
  } else {
    write-output "`n NOT Running as administrator `n"
  }
}

function GetLocalPath()
{
  write-output ""
  $env:path.split(";")
  write-output ""
}

function AppendLocalPath()
{
  if (!(TEST-PATH $directory)) {
    write-output "'$directory' does not Exist, cannot be added to the path"
    return
  }
  $PathasArray = ($Env:PATH).split(';')
  if ($PathasArray -contains $directory -or $PathAsArray -contains $directory+'\') {
    write-output "'$Directory' already within the path"
    return
  }
  If (!($directory[-1] -match '\\')) {
    $directory  =  $directory + '\'
  }
  $env:path  =  $directory + ";" + $env:path
  GetLocalPath
}

function RemoveLocalPath()
{
  If ( $env:path.split(';') -contains $directory ) {
    $env:path = $env:path.replace($directory,$NULL)
    $env:path = $env:path.replace(';;',';')
  }
  GetLocalPath
}

function SetLocalPath()
{
  $env:path  =  $directory
  GetLocalPath
}

if ($help) { help; break }
if ($admin_bool) { CheckLocalAdmin; break }
if ($system_properties_bool) { control.exe sysdm.cpl,System,3; break }
if (! $directory) { GetLocalPath; break }
if ($append_bool) { AppendLocalPath; break }
if ($remove_bool) { RemoveLocalPath; break }
if ($set_bool) { SetLocalPath; break }