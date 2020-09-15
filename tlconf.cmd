@echo off

if /i .%1. == .. goto help
if /i .%1. == .cnf. goto cnf
if /i .%1. == .texedit. goto texedit
if /i .%1. == .texmfhome. goto texmfhome
if /i .%1. == .sumatrapdf. goto SumatraPDF
if /i .%1. NEQ .batch. goto eof

:cnf
rem checking if TeX Live is found
kpsewhich -var-value=TEXMFROOT >nul 2>&1
if errorlevel 1 (
echo TeX Live not on searchpath. Aborting.
exit /b
)

for /f "usebackq delims=" %%p in (`kpsewhich -var-value=TEXMFROOT`) do set tlroot=%%p
set tlroot=%tlroot:/=\%

rem updating texmf.cnf
set cnf=%tlroot%\texmf.cnf
set org=%tlroot%\texmf.org
dir %org% >nul 2>&1
if errorlevel == 1 copy %cnf% %org%
echo OSFONTDIR=$SystemRoot/fonts//;$localappdata/Microsoft/Windows/Fonts// > %cnf%
echo TEXLIVE_WINDOWS_TRY_EXTERNAL_PERL = 0 >> %cnf%
echo %cnf%:
type %cnf%

rem creating local.conf
set localconf=%tlroot%\texmf-var\fonts\conf\local.conf
set content=%LOCALAPPDATA%/Microsoft/Windows/Fonts
set content=%content:\=/%
set "content=^<dir^>%content%^</dir^>"
echo %content% > %localconf%
echo %localconf%:
type %localconf%
if /i .%1. NEQ .batch. goto eof

:texedit
if .%2. == .. (
setx TEXEDIT "\"%LOCALAPPDATA%\Programs\Microsoft VS Code\code.exe\" -r -g \"%%s\":%%d"
) else (
setx TEXEDIT "%2"
)
reg query HKEY_CURRENT_USER\Environment /v TEXEDIT
if /i .%1. NEQ .batch. goto eof

:texmfhome
if .%2. == .. (
setx TEXMFHOME "C:\home\texmf"
) else (
setx TEXMFHOME "%2"
)
reg query HKEY_CURRENT_USER\Environment /v TEXMFHOME
if /i .%1. NEQ .batch. goto eof

:SumatraPDF
reg query HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Applications\SumatraPDF.exe\DefaultIcon >nul 2>&1
if errorlevel 1 (
echo SumatraPDF is not found.
goto eof
) else (
for /f "usebackq tokens=3-4 delims=, " %%x in (`reg query HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Applications\SumatraPDF.exe\DefaultIcon`) do set sumatra="%%x %%y"
)
set sumatra=start "" %sumatra% -inverse-search
if .%2. == .. (
%sumatra% "\"%LOCALAPPDATA%\Programs\Microsoft VS Code\code.exe\" -r -g \"%%f\":%%l"
) else (
%sumatra% %2
)
goto eof

:help
echo tlconf cnf              : Add the user's font folder to texmf.cnf and to local.cnf.
echo tlconf texedit [...]    : Set the TEXEIDT environment variable. The default is 
echo                           "%LOCALAPPDATA%\Programs\Microsoft VS Code\code.exe" -r -g "%%s":%%d
echo tlconf texmfhome [...]  : Set the TEXMFHOME environment variable. The default is 
echo                           C:\home\texmf
echo tlconf sumatrapdf [...] : Set the inverse search command-line option of SumatraPDF. The defualt is
echo                           "%LOCALAPPDATA%\Programs\Microsoft VS Code\code.exe" -r -g "%%f":%%l
echo tlconf batch            : Proceed with all options.

:eof