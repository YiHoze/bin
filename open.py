import os
import sys
import glob
import argparse
import configparser
import subprocess

class FileOpener(object):
    def __init__(self, files=None, Adobe=False, texlive=False):
        self.ini = self.initialize()
        self.files = files
        self.Adobe = Adobe
        self.texlive = texlive

    def initialize(self):        
        inipath = os.path.dirname(__file__) 
        ini = os.path.join(inipath, 'docenv.ini')
        if os.path.exists(ini):
            config = configparser.ConfigParser()
            config.read(ini)
            try:
                self.editor = config.get('Text Editor', 'path')
                self.associations = config.get('Text Editor', 'associations')
                self.PDFviewer = config.get('SumatraPDF', 'path')
                self.AdobeReader = config.get('Adobe Reader', 'path')
                return True
            except:
                print('Make sure to have docenv.ini set properly.')
                return False
        else:
            print('Docenv.ini is not found in %s.' %(inipath))
            return False

    def check_editor(self):
        if os.path.exists(self.editor):
            return True
        else:
            print('Check the path to the text editor.')
            return False

    def check_PDFviewer(self):
        if os.path.exists(self.PDFviewer):
            return True
        else:
            print('Check the path to the PDF viewer.')
            return False
    
    def check_AdobeReader(self):
        if os.path.exists(self.AdobeReader):
            return True
        else:
            print('Check the path to the Adobe Reader.')
            return False

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Open text files and others with an appropriate application.'
        )
        parser.add_argument(
            'files',
            nargs = '+',
            help = 'Specify files to open.'
        )        
        parser.add_argument(
            '-e',
            dest = 'editor',
            default = self.editor,
            help = 'Specify a different text editor to use it.'
        )
        parser.add_argument(
            '-o',
            dest = 'edopt',
            default = '',
            help = 'Specify options for the text editor.'
        )
        parser.add_argument(
            '-a',
            dest = 'Adobe',
            action = 'store_true',
            help = 'Use Adobe Reader to view PDF.'
        )
        parser.add_argument(
            '-s',
            dest = 'texlive',
            action = 'store_true',
            default = False,
            help = 'Search TeX Live for the specified file to find and open.'
        )
        args = parser.parse_args()
        self.files = args.files
        self.editor = args.editor
        self.edopt = args.edopt
        self.Adobe = args.Adobe
        self.texlive = args.texlive

    def DetermineFileType(self, afile):
        ext = os.path.splitext(afile)[1]        
        if ext.lower() in self.associations:
            return('txt')
        elif ext.lower() ==  '.pdf':
            return('pdf')
        else:
            return('another')

    def OpenHere(self, files):
        for fnpattern in files:
            for afile in glob.glob(fnpattern):
                filetype = self.DetermineFileType(afile)
                if filetype ==  'txt':                    
                    self.OpenTxt(afile)
                elif filetype ==  'pdf':
                    self.OpenPDF(afile)
                else:
                    cmd = 'start \"\" \"%s\"' % (afile)
                    os.system(cmd)

    def OpenTxt(self, afile):
        if self.check_editor():
            cmd = '\"%s\" %s %s' % (self.editor, self.edopt, afile)
            subprocess.Popen(cmd, stdout=subprocess.PIPE)

    def OpenPDF(self, afile):
        if self.Adobe:
            if self.check_AdobeReader():
                cmd = '\"%s\" \"%s\"' % (self.AdobeReader, afile)
                subprocess.Popen(cmd, stdout=subprocess.PIPE)                 
        else:   
            if self.check_PDFviewer():
                cmd = '\"%s\" \"%s\"' % (self.PDFviewer, afile)
                subprocess.Popen(cmd, stdout=subprocess.PIPE)                 

    def SearchTeXLive(self, files):
        if self.check_editor():
            for afile in files:
                try:
                    result = subprocess.check_output(['kpsewhich', afile], stderr=subprocess.STDOUT)
                    found = str(result, 'utf-8')  
                    found = found.rstrip()                
                    self.OpenTxt(found)
                except subprocess.CalledProcessError:
                    print('%s is not found in TeX Live.' %(afile))

    def open(self, files=None):
        if self.ini:           
            if files == None:
                files = self.files
            if self.texlive:
                self.SearchTeXLive(files)
            else:
                self.OpenHere(files)

if __name__ ==  '__main__':
    opener = FileOpener()    
    opener.parse_args()    
    opener.open()