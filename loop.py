import os
import sys
import glob
import argparse
import re

example = '''examples:
loop.py "cpdf -pages *.pdf"
    cpdf will display the number of pages in each PDF file.
loop.py -c "pdfcrop foo_*.pdf goo_*.pdf" 
    This is the same as
        pdfcrop foo_1.pdf goo_1.pdf
        pdfcrop foo_2.pdf goo_2.pdf        
loop.py -c "magick -rotate 90 foo_*.png foo_*.png"
    This is the same as
        magick -rotate 90 foo_1.png foo_1.png
        magick -rotate 90 foo_2.png foo_2.png
'''

parser = argparse.ArgumentParser(
    epilog = example,
    formatter_class = argparse.RawDescriptionHelpFormatter,
    description = 'A given command will be repeated with each one matching wildcard characters.'
)
parser.add_argument(
    'cmd',
    nargs = 1,
    help = 'Type a command with arguments including wildcard characters.'
)
parser.add_argument(
    '-c',
    dest = 'consecutive_bool',
    action = 'store_true',
    default = False,
    help = 'Change wildcard characters to consecutive numbers and check if matching files exist.'
)
args = parser.parse_args()

# find the argument that contains '*'
cmd = args.cmd[0].split(' ')
for i in cmd:
    if i.count('*') > 0:
        selection = i
        break

cmd = ' '.join(cmd)
if args.consecutive_bool:
    for i in glob.glob(selection):
        num = re.findall(r'\d+', i)
        if len(num) > 0:
            real_cmd = cmd.replace('*', num[0])
            os.system(real_cmd)            
        else:
            print('No numbered files are found.')
            break
else:   
    ext =  os.path.splitext(os.path.basename(selection))[1]
    for i in glob.glob(selection):  
        filename = os.path.splitext(os.path.basename(i))[0] + ext
        real_cmd = cmd.replace(selection, filename)
        os.system(real_cmd)        