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

    def __init__(self, argv=None):    

        self.cmd = None
        self.generated_files = []

        tpl = os.path.join(dirCalled, 'latex.tpl')
        if os.path.exists(tpl):
            self.templates = configparser.ConfigParser()
            self.templates.read(tpl, encoding='utf-8')
        else:
            print('latex.tpl is not found.')
            sys.exit()

        self.parse_args(argv)
        self.determine_task()


    def parse_args(self, argv=None):

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
            dest = 'defy_bool',
            action = 'store_true',
            default = False,
            help = 'Do not compile even if some compilation options are prescribed.'
        )
        parser.add_argument(
            '-f',
            dest = 'force_bool',
            action = 'store_true',
            default = False,
            help = 'Compile without opening the tex file even if no compilation option is prescribed .'
        )
        parser.add_argument(
            '-r',
            dest = 'remove_bool',
            action = 'store_true',
            default = False,
            help = 'Remove the tex and its subsidiary files after compilation.'
        )
        parser.add_argument(
            '-l',
            dest = 'list_bool',
            action = 'store_true',
            default = False,
            help = 'Enumerate templates'
        )
        parser.add_argument(
            '-L',
            dest = 'List_bool',
            action = 'store_true',
            default = False,
            help = 'Enumerate tempaltes with description.'
        )
        parser.add_argument(
            '-d',
            dest = 'detail_bool',
            action = 'store_true',
            default = False,
            help = 'Show the details about the specified template.'            
        )

        self.args = parser.parse_args(argv)

    def confirm_to_remove(self, afile):

        if os.path.exists(afile):
            answer = input('%s already exists. Are you sure to overwrite it? [y/N] ' %(afile))
            if answer.lower() == 'y':
                os.remove(afile)
                return True
            else:
                return False
        else:
            return True


    def determine_filename(self):

        if self.args.output is None:
            self.filename = self.templates.get(self.args.template, 'output', fallback='mydoc')
        else:
            filename = self.args.output
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
        images.sort(key=str.lower)
        images = '\n'.join(images)        
        with open(image_list_file, mode='w', encoding='utf-8') as f:
            f.write(images)

        if self.args.remove_bool:
            self.generated_files.append(image_list_file)

        return True


    def fill_placeholders(self, content):       

        content = content.replace('`', '')
        try:
            placeholders = int(self.templates.get(self.args.template, 'placeholders'))
            defaults = self.templates.get(self.args.template, 'defaults')
            defaults = defaults.split(', ')
        except:
            return content
        if self.args.substitutes is not None:
            for index, value in enumerate(self.args.substitutes):
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

        content = self.templates.get(self.args.template, extension, fallback=None)
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
                if self.args.remove_bool:
                    self.generated_files.append(ext)
            

    def write_from_template(self):

        self.write_relatives('bib')
        self.write_relatives('cmd')
        self.write_relatives('css')
        self.write_relatives('gv')
        self.write_relatives('map')
        self.write_relatives('sty')
        self.write_relatives('xdy')
        # self.confirm_to_remove(self.tex)
        
        if self.confirm_to_remove(self.tex):        
            try:
                content = self.templates.get(self.args.template, 'tex')
                content = self.fill_placeholders(content)
                with open(self.tex, mode='w', encoding='utf-8') as f:
                    f.write(content)
            except:
                print('Make sure to have latex.tpl set properly.')
                return False

        if self.args.remove_bool:
            self.generated_files.append(self.tex)

        if not self.args.force_bool:
            opener = FileOpener()
            opener.open_txt(self.tex)
        return True


    def compile(self):

        compiler_option = self.templates.get(self.args.template, 'compiler', fallback=None)
        if compiler_option is None:
            if self.args.force_bool:
                LatexCompiler(self.tex, ['-v'])                
            else:                
                if self.cmd is not None:
                    answer = input('Do you want to run %s? [Y/n] ' %(self.cmd))
                    if answer.lower() != 'n':
                        os.system(self.cmd)
        else:       
            compiler_option = compiler_option.split(', ')
            compiler_option.append('-v')            
            LatexCompiler(self.tex, compiler_option)

        if self.args.remove_bool:
            for i in self.generated_files:
                os.remove(i)


    def make(self):

        if not self.templates.has_section(self.args.template):
            print('"{}" is not defined.'.format(self.args.template))
            return False
        self.determine_filename()
        if self.args.template == 'album':            
            if self.make_image_list() is False:
                return 
        if self.write_from_template(): 
            if not self.args.defy_bool:           
                self.compile()                


    def enumerate_with_description(self):

        templates = sorted(self.templates.sections(), key=str.casefold)
        for i in templates:
            description = self.templates.get(i, 'description', fallback=None)
            if description is None:
                description = ''
            else:
                description = description.split('\n')[0]
            print('{:20} {}'.format(i, description))


    def enumerate_without_description(self, columns=4):  

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

        if not self.templates.has_section(self.args.template):
            print('"{}" is not defined.'.format(self.args.template))
            return 
        usage = self.templates.get(self.args.template, 'description', fallback=None)
        if usage == None:
            print('"{}" has no decription'.format(self.args.template))
        else: 
            print('\n{}\n'.format(usage))


    def determine_task(self):

        if self.args.List_bool:
            self.enumerate_with_description()
        elif self.args.list_bool:
            self.enumerate_without_description()
        elif self.args.detail_bool:
            self.show_details()
        else:
            self.make()

if __name__ == '__main__':
    LatexTemplate()
