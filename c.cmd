if .%1. == .m. goto FINAL

:DRAFT
strfind.py -t "\\documentclass\[pairquote, minted\]{hzguide}" -s "\\documentclass[pairquote]{hzguide}" hzguide.tex
ltx.py hzguide.tex %1 %2
goto EOF

:FINAL
strfind.py -t "\\documentclass\[pairquote\]{hzguide}" -s "\\documentclass[pairquote, minted]{hzguide}" hzguide.tex
ltx.py -s hzguide.tex %2 %3

:EOF
