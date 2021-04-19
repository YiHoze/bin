import os
import sys
import glob
import argparse
import configparser
import subprocess

class FileOpener(object):

    def __init__(self):

        self.force_bool = False
        self.Adobe_bool = False
        self.texlive_bool = False
        self.web_bool = False
        self.application = ''
        self.app_option = ''
        self.initialize()

    def initialize(self):

        inipath = os.path.dirname(__file__)
        ini = os.path.join(inipath, 'docenv.ini')
        if os.path.exists(ini):
            config = configparser.ConfigParser()
            config.read(ini)
            try:
                self.editor = config.get('Text Editor', 'path')
                self.associations = config.get('Text Editor', 'associations')
                self.pdf_viewer = config.get('SumatraPDF', 'path')
                self.AdobeReader = config.get('Adobe Reader', 'path')
                self.WebBrowser = config.get('Web Browser', 'path')
            except:
                print('Make sure to have docenv.ini set properly.')
                sys.exit()
        else:
            print('Docenv.ini is not found in {}.'.format(inipath))
            sys.exit()


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
            '-a',
            dest = 'application',
            default = None,
            help = 'Specify an application program to use.'
        )
        parser.add_argument(
            '-o',
            dest = 'app_option',
            default = '',
            help = 'Specify options for the application.'
        )
        parser.add_argument(
            '-A',
            dest = 'Adobe_bool',
            action = 'store_true',
            default = False,
            help = 'Use Adobe Reader to view PDF.'
        )
        parser.add_argument(
            '-s',
            dest = 'texlive_bool',
            action = 'store_true',
            default = False,
            help = 'Search TeX Live for the specified file to find and open.'
        )
        parser.add_argument(
            '-f',
            dest = 'force_bool',
            action = 'store_true',
            default = False,
            help = 'Force to open as text.'
        )
        parser.add_argument(
            '-w',
            dest = 'web_bool',
            action = 'store_true',
            default = False,
            help = 'Access the given website.'
        )

        args = parser.parse_args()

        self.files = args.files
        self.force_bool = args.force_bool
        self.Adobe_bool = args.Adobe_bool
        self.texlive_bool = args.texlive_bool
        self.web_bool = args.web_bool
        self.application = args.application
        self.app_option = args.app_option

    # def check_editor(self):

    #     if os.path.exists(self.editor):
    #         return True
    #     else:
    #         print('Check the path to the text editor.')
    #         return False


    # def check_pdf_viewer(self):

    #     if os.path.exists(self.pdf_viewer):
    #         return True
    #     else:
    #         print('Check the path to the PDF viewer.')
    #         return False


    # def check_AdobeReader(self):

    #     if os.path.exists(self.AdobeReader):
    #         return True
    #     else:
    #         print('Check the path to the Adobe Reader.')
    #         return False

    def determine_file_type(self, afile):

        ext = os.path.splitext(afile)[1]
        if ext.lower() in self.associations:
            return 'txt'
        elif ext.lower() ==  '.pdf':
            return 'pdf'
        else:
            return 'another'


    def open_here(self, files):

        for fnpattern in files:
            for afile in glob.glob(fnpattern):
                if self.application is None:
                    filetype = self.determine_file_type(afile)
                    if filetype == 'txt' or self.force_bool:
                        self.open_txt(afile)
                    elif filetype ==  'pdf':
                        self.open_pdf(afile)
                    else:
                        cmd = 'start \"\" \"{}\"'.format(afile)
                        os.system(cmd)
                else:
                    self.open_app(afile)


    def open_app(self, afile):

        cmd = '\"{}\" {} {}'.format(self.application, self.app_option, afile)
        subprocess.Popen(cmd, stdout=subprocess.PIPE)


    def open_txt(self, afile):

        cmd = '\"{}\" {} {}'.format(self.editor, self.app_option, afile)
        subprocess.Popen(cmd, stdout=subprocess.PIPE)


    def open_pdf(self, afile):

        if self.Adobe_bool:
            cmd = '\"{}\" \"{}\"'.format(self.AdobeReader, afile)
            subprocess.Popen(cmd, stdout=subprocess.PIPE)
        else:
            cmd = '\"{}\" \"{}\"'.format(self.pdf_viewer, afile)
            subprocess.Popen(cmd, stdout=subprocess.PIPE)


    def search_tex_live(self, files):

        for afile in files:
            try:
                result = subprocess.check_output(['kpsewhich', afile], stderr=subprocess.STDOUT)
                found = str(result, 'utf-8')
                found = found.rstrip()
                self.open_txt(found)
            except subprocess.CalledProcessError:
                print('{} is not found in TeX Live.'.format(afile))


    def open_web(self, urls):

        for url in urls:
            cmd = '\"{}\" \"{}\"'.format(self.WebBrowser, url)
            subprocess.Popen(cmd)


    def open(self, files=None):

        if self.texlive_bool:
            self.search_tex_live(files)
        elif self.web_bool:
            self.open_web(files)
        else:
            self.open_here(files)


if __name__ == '__main__':
    opener = FileOpener()
    opener.parse_args()
    opener.open(opener.files)
