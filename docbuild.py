import os
import sys
import glob
import argparse
# import subprocess

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from ltx import LatexCompiler
from iu import ImageUtility
from autojosa import AutoJosa

class DocBuilder(object):
    def __init__(self):
        return
        
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Let Sphinx produce HTML or PDF with XeLaTeX.'
        )
        parser.add_argument(
            'format',
            nargs = '?',
            default = 'html',
            help = 'Choose between html and latex. The default is html.'
        )
        parser.add_argument(
            '-t',
            dest = 'tex',
            help = 'Specify the tex filename.'
        )
        parser.add_argument(
            '-n', 
            dest = 'noCompile',
            action = 'store_true',
            default = False,
            help = 'Pass over latex compilation.'
        )
        parser.add_argument(
            '-j',
            dest = 'AutoJosa',
            action = 'store_true',
            default = False,
            help = 'Replace with 자동조사 macros.'
        )
        # parser.add_argument(
        #     '-x',
        #     dest = 'noImage',
        #     action = 'store_true',
        #     default = False,
        #     help = 'Pass over image processing.'
        # )
        parser.add_argument(
            '-r',
            dest = 'renew',
            action = 'store_true',
            default = False,
            help = 'Read and write all files anew.'
        )
        parser.add_argument(
            '-k',
            dest = 'keep_collateral',
            action = 'store_true',
            default = False,
            help = "Do not remove unnecessary collateral files, including sphinxmanual.cls."
        )
        parser.add_argument(
            '-C',
            dest = 'clear',
            action = 'store_true',
            default = False,
            help = 'Clear the build directory.'
        )
        self.args, self.compile_option = parser.parse_known_args()        

    def build_html(self):
        if self.args.renew:
            cmd = 'sphinx-build -b html -a -E . _build/html' 
        else:
            cmd = 'sphinx-build -M html . _build'     
        os.system(cmd)

    def build_latex(self):          
        for afile in glob.glob('_build/latex/blockdiag-*.pdf'):
            os.remove(afile)

        if self.args.renew:
            cmd = 'sphinx-build -b latex -a -E . _build/latex'
        else:
            cmd = 'sphinx-build -M latex . _build'         
        os.system(cmd)

        os.chdir('_build/latex')
        # Remove unnecessary files
        if not self.args.keep_collateral:
            files = ['sphinxhowto.cls', 'sphinxmanual.cls', 'python.ist', 'make.bat', 'Makefile', 'LatinRules.xdy', 'LICRcyr2utf8.xdy', 'LICRlatin2utf8.xdy', 'sphinx.xdy', 'latexmkjarc', 'latexmkrc', 'Makefile']
            for afile in files:
                if os.path.exists(afile):
                    os.remove(afile)
        # Replace '을' with '\을'
        if self.args.AutoJosa:
            autojosa = AutoJosa([self.args.tex])
            autojosa.replace()
        # Covert SVG images to PDF and crop PDF images
        # if not self.args.noImage:        
        #     iu = ImageUtility(['*.svg'], target='pdf', recursive=True)
        #     iu.convert()
        #     for afile in glob.glob('blockdiag-*.pdf'):
        #         cmd = 'pdfcrop.exe %s %s' %(afile, afile)
        #         os.system(cmd)    
        # Run xelatex to make PDF
        if not self.args.noCompile:
            texer = LatexCompiler(self.args.tex)
            texer.parse_args(self.compile_option)
            texer.compile()
        os.chdir('../..')

    def clear_build(self):
        cmd = 'sphinx-build -M clean . _build'
        os.system(cmd)

    def run(self):
        if self.args.clear:
            self.clear_build()      
        elif self.args.format == 'html':
            self.build_html()
        elif self.args.format == 'latex':
            self.build_latex()

if __name__ == '__main__':
    docbuild = DocBuilder()
    docbuild.parse_args()
    docbuild.run()
