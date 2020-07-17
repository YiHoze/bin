import os
import sys
import glob
import argparse

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from ltx import LatexCompiler

exclude = ['colophone', '_kor', '_eng']

parser = argparse.ArgumentParser(
    description = 'Find a tex file to compile it with ltx.py.'
)
parser.add_argument(
    '-x',
    dest = 'list_bool',
    action = 'store_true',
    default = False,
    help = 'Enumerate every tex file for choice.'
)
args, compile_option = parser.parse_known_args()

def excluded(tex):
    for i in exclude:
        if i in tex:
            return True
    return False

if args.list_bool:
    files = []
    for i in glob.glob("*.tex"):
        files.append(i)
    for i, v in enumerate(files):
        print('{}:{}'.format(i+1, v))
    choice = input('Choose a file by entering its number: ')
    try:
        choice = int(choice)
    except:
        print('Wrong selection.')
        sys.exit()
    choice = choice - 1 
    if choice >= 0 and choice < len(files):
        tex = files[choice]        
    else:
        print('Wrong selection.')
        sys.exit()
else:
    for i in glob.glob("*.tex"):
        if not excluded(i):
            tex = i
            break
     
texer = LatexCompiler(tex)
texer.parse_args(compile_option)
texer.compile()