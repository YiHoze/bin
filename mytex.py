#>mytex.py template -s foo1 foo2 foo3 

import os
import sys
import glob
import argparse
import configparser

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from open import FileOpener
from ltx import LatexCompiler

class LatexTemplate(object):

    def __init__(self, template='hzguide', substitutes=None, output=None, defy=False):

        self.template = template
        self.substitutes = substitutes
        self.output = output
        self.defy_bool = defy
        self.list_bool = False
        self.cmd = None
        self.ini_bool = self.initialize() 
        self.generated_files = []   


    def initialize(self):

        tpl = os.path.join(dirCalled, 'latex.tpl')
        if os.path.exists(tpl):
            self.templates = configparser.ConfigParser()
            self.templates.read(tpl, encoding='utf-8')
            return True
        else:
            print('latex.tpl is not found.')
            return False


    def parse_args(self):

        example = '''examples:
    mytex.py
        makes mydoc.tex out of the default template, article.
    mytex.py -l
        enumerates templates
    mytex.py metapost -d
        gives a brief description of the metapost template.
    mytex.py memoir -o foo 
        makes "foo.tex" out of the memoir template.
    mytex.py lotto -s 20 10 
        makes and compiles lotto.tex, of which two placeholders are replaced with "20" and "10".
    mytex.py lotto -n
        makes lotto.tex but doesn't compile though this template has some compilation options.
    mytex.py glyph -f
        makes and compiles myfont.tex though this template has no comilation options.
        '''
        parser = argparse.ArgumentParser(
            epilog = example,  
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = 'Create a LaTeX file from several templates and compile it using ltx.py.'
        )
        parser.add_argument(
            'template',
            type = str,
            nargs = '?',
            default = 'article',
            help = 'Choose a template.'
        )
        parser.add_argument(
            '-s',
            dest = 'substitutes',
            nargs = '*',
            help = 'Specify strings which to replace the tex file with.'
        )
        parser.add_argument(
            '-o',
            dest = 'output',
            help = 'Specify a filename for output.'
        )
        parser.add_argument(
            '-n',
            dest = 'defy',
            action = 'store_true',
            default = False,
            help = 'Do not compile even if some compilation options are prescribed.'
        )
        parser.add_argument(
            '-f',
            dest = 'force',
            action = 'store_true',
            default = False,
            help = 'Compile without opening the tex file even if no compilation option is prescribed .'
        )
        parser.add_argument(
            '-r',
            dest = 'remove',
            action = 'store_true',
            default = False,
            help = 'Remove the tex and its subsidiary files after compilation.'
        )
        parser.add_argument(
            '-l',
            dest = 'list',
            action = 'store_true',
            default = False,
            help = 'Show the list of templates.'
        )
        parser.add_argument(
            '-d',
            dest = 'detail',
            action = 'store_true',
            default = False,
            help = 'Show the details about the specified template.'            
        )
        args = parser.parse_args()
        self.template = args.template
        self.substitutes = args.substitutes
        self.output = args.output
        self.list_bool = args.list
        self.detail_bool = args.detail
        self.defy_bool = args.defy
        self.force_bool = args.force
        self.remove_bool = args.remove


    def confirm_to_remove(self, afile):

        if os.path.exists(afile):
            answer = input('%s alread exists. Are you sure to overwrite it? [y/N] ' %(afile))
            if answer.lower() == 'y':
                os.remove(afile)
                return True
            else:
                return False
        else:
            return True


    def determine_filename(self):

        if self.output is None:
            self.filename = self.templates.get(self.template, 'output', fallback='mydoc')
        else:
            filename = self.output
            self.filename = os.path.splitext(filename)[0]        
        self.tex = self.filename + '.tex'        


    def make_image_list(self):

        image_list_file = self.templates.get('album', 'image_list', fallback='im@ges.txt')
        if os.path.exists(image_list_file):
            os.remove(image_list_file)
        pdf = self.filename + '.pdf'
        if os.path.exists(pdf):
            os.remove(pdf)

        # Make a file to contain a list of image files
        images = []
        image_type = ['pdf', 'jpg', 'jpeg', 'png']
        for img in image_type:
            for afile in glob.glob('*.' + img):
                images.append(afile)
        if len(images) == 0:
            print('No image files are found.')
            return False
        images.sort()
        images = '\n'.join(images)        
        with open(image_list_file, mode='w', encoding='utf-8') as f:
            f.write(images)

        if self.remove_bool:
            self.generated_files.append(image_list_file)

        return True


    def fill_placeholders(self, content):       

        content = content.replace('`', '')
        try:
            placeholders = int(self.templates.get(self.template, 'placeholders'))
            defaults = self.templates.get(self.template, 'defaults')
            defaults = defaults.split(', ')
        except:
            return content
        if self.substitutes is not None:
            for index, value in enumerate(self.substitutes):
                if index < placeholders:
                    defaults[index] = value
                else:
                    break
        cnt = 1
        for i in defaults:
            content = content.replace('\\' + str(cnt), i)
            cnt += 1
        return content

    def write_relatives(self, extension):

        content = self.templates.get(self.template, extension, fallback=None)
        ext = self.filename + '.' + extension
        if content is not None:
            if extension == 'cmd':
                self.cmd = ext
                content = content.replace('\\TEX', self.tex)
                content = content.replace('\\PDF', self.filename + '.pdf')
                content = content.replace('\\DVI', self.filename + '.dvi')
                content = content.replace('\\PS', self.filename + '.ps')
            else:
                content = content.replace('`', '')            
            if self.confirm_to_remove(ext):
                with open(ext, mode='w', encoding='utf-8') as f:
                    f.write(content) 
                if self.remove_bool:
                    self.generated_files.append(ext)
            

    def write_from_template(self):

        self.write_relatives('cmd')
        self.write_relatives('sty')
        self.write_relatives('bib')
        self.write_relatives('xdy')
        self.write_relatives('css')
        self.write_relatives('map')
        if not self.confirm_to_remove(self.tex):
            return False
        try:
            content = self.templates.get(self.template, 'tex')
            content = self.fill_placeholders(content)
        except:
            print('Make sure to have latex.tpl set properly.')
            return False
        with open(self.tex, mode='w', encoding='utf-8') as f:
            f.write(content)
        if self.remove_bool:
            self.generated_files.append(self.tex)

        opener = FileOpener()
        if not self.force_bool:
            opener.OpenTxt(self.tex)
        return True


    def compile(self):

        compiler = self.templates.get(self.template, 'compiler', fallback=None)
        if compiler is None:
            if self.force_bool:
                texer = LatexCompiler(self.tex)
                texer.parse_args(['-v'])
                texer.compile()  
            else:                
                if self.cmd is not None:
                    answer = input('Do you want to run %s? [Y/n] ' %(self.cmd))
                    if answer.lower() != 'n':
                        os.system(self.cmd)
        else:       
            compiler = compiler.split(', ')
            compiler.append('-v')            
            texer = LatexCompiler(self.tex)
            texer.parse_args(compiler)        
            texer.compile()

        if self.remove_bool:
            for i in self.generated_files:
                os.remove(i)


    def make(self):

        if not self.templates.has_section(self.template):
            print('"{}" is not defined.'.format(self.template))
            return False
        self.determine_filename()
        if self.template == 'album':            
            if self.make_image_list() is False:
                return 
        if self.write_from_template(): 
            if not self.defy_bool:           
                self.compile()                


    def show_templates(self, columns=4):  

        """Print the list of template names."""  
        templates = sorted(self.templates.sections(), key=str.casefold)
        width = 0
        for i in templates:
            width = max(width, len(i))
        width += 4
        i = 0
        while i < len(templates):
            line = ''
            for j in range(columns):
                k = i + j
                if k < len(templates):
                    line += '{:{w}}'.format(templates[k], w=width)
                else:
                    break
            i += columns
            print(line)


    def show_details(self):

        if not self.templates.has_section(self.template):
            print('"{}" is not defined.'.format(self.template))
            return 
        usage = self.templates.get(self.template, 'description', fallback=None)
        if usage == None:
            print('"{}" has no decription'.format(self.template))
        else: 
            print('\n{}\n'.format(usage))


if __name__ == '__main__':
    mytex = LatexTemplate()
    if mytex.ini_bool:
        mytex.parse_args()
        if mytex.list_bool:
            mytex.show_templates()
        elif mytex.detail_bool:
            mytex.show_details()
        else:
            mytex.make()