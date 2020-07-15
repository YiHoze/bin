import os
import sys
import glob
import argparse

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from ltx import LatexCompiler

exclude = ['colophone.tex']

parser = argparse.ArgumentParser(
    description = 'Find a tex file to compile it with ltx.py.'
)
args, compile_option = parser.parse_known_args()

for i in glob.glob("*.tex"):
    for j in exclude:
        if i != j:
            tex = i
            break

texer = LatexCompiler(tex)
texer.parse_args(compile_option)
texer.compile()