import os
import sys
import configparser
import argparse
import glob 

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from ltx import LatexCompiler

class ipynb_to_pdf(object):
    def __init__(self, ipynb=None):
        self.ini_bool = self.initialize()
        self.ipynb = ipynb

    def check_template(self):
        if os.path.exists(self.template):
            return True
        else:
            print('%s is not found.' %(self.template))
            return False

    def initialize(self):
        inipath = os.path.dirname(__file__) 
        ini = os.path.join(inipath, 'docenv.ini')
        if os.path.exists(ini):
            config = configparser.ConfigParser()
            config.read(ini)
            try:
                self.template = config.get('Jupyter Template', 'latex')
                self.template = os.path.join(inipath, self.template)
                return self.check_template()
            except:
                print('Make sure to have docenv.ini set properly.')
                return False
        else:
            print('Docenv.ini is not found.')
            return False

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Convert Jupyter notebook files (.ipynb) to PDF using nbconvert and XeLaTeX.'
        )
        parser.add_argument(
            'ipynb',
            nargs = '+',
            help = 'Specify one or more Jupyter notebook files.'
        )
        parser.add_argument(
            '-t',
            dest = 'template',
            help = 'To use another latex template, specify the path to it.'
        )
        args, self.compile_option = parser.parse_known_args()
        self.ipynb = args.ipynb
        if args.template is not None:
            self.template = args.template
            self.ini_bool = self.check_template()

    def convert_each(self, afile):
        basename, ext = os.path.splitext(afile)
        if ext == '.ipynb':
            tex = basename + '.tex'
            # Convert to tex
            cmd = 'jupyter-nbconvert --to=latex --template=%s --SVG2PDFPreprocessor.enabled=True %s' %(self.template, afile)
            os.system(cmd)        
            # Compile tex
            if os.path.exists(tex):                
                texer = LatexCompiler(tex)                
                if len(self.compile_option) == 0:
                     self.compile_option.append('-w')                
                texer.parse_args(self.compile_option)
                texer.compile()         
        else:            
            print('%s is not a Jupyter notebook.' %(afile))

    def convert(self):
        if self.ini_bool:
            for fnpattern in self.ipynb:
                for afile in glob.glob(fnpattern):
                    self.convert_each(afile)

if __name__ == '__main__':
    nb2pdf = ipynb_to_pdf()
    nb2pdf.parse_args()
    nb2pdf.convert()
