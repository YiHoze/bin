import os
import sys
import argparse
import glob
import subprocess
import csv
import re
import codecs
import unicodedata
from PyPDF2 import PdfFileReader
from chardet.universaldetector import UniversalDetector

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from open import FileOpener


class WordDigger(object):

    def __init__(self):

        global texlive_bool

        try:
            print("Checking whether pdftotext.exe is available:\n")
            subprocess.check_call('pdftotext -v')
            print()
            texlive_bool = True
        except OSError:
            print('pdftotext.exe is needed to counts words in PDF files but not found.')
            texlive_bool = False

        self.lines = 0
        self.chars = 0
        self.words = 0
        self.pages = 0
        self.found = []

        self.tex_patterns = [
                r'\\[^a-zA-Z]', 
                r'\\[a-zA-Z*^|+]+',
                r'\\begin(\{.+?\}[*^|+]*)', 
                r'\s(\w+=)'
            ]

        self.detex_tsv = r'''(?<!\\)%.+?\n	\n
\\title\{(.+?)\}	\1
\\part\{(.+?)\}	\1
\\chapter\{(.+?)\}	\1
\\section\{(.+?)\}	\1
\\subsection\{(.+?)\}	\1
\\subsubsection\{(.+?)\}	\1
\\caption\{(.+?)\}	\1
\\textbf\{(.+?)\}	\1
\\textsf\{(.+?)\}	\1
\\texttt\{(.+?)\}	\1
\\textit\{(.+?)\}	\1
\\textsl\{(.+?)\}	\1
\\action\{(.+?)\}	\1
\\ui\{(.+?)\}	\1
\\term\{(.+?)\}	\1
\\annotate.?\{(.+?)\}	\1
\\anota.?\{(.+?)\}	\1
\\menu.?\{(.+?)\}\{(.+?)\}	\1 \2
\\item\[(.+?)\]	\1
\\begin\{.+?\}.*?\n	
\\end\{.+?\}\n	
\\CoverSetup\{	
\\.+?Setup\[.+?\](.|\n)+?\}\n	
\\.+?Setup(.|\n)+?\}\n	
\\.+?\{.+?\}\{(.|\n)+?\}\n	 
\\([가-로]{1,2})	\1
\\\\	\n
([#\$%\^&_])	\1
\\node(.|\n)+?\};	
\\.+?\{.+?\}\{.+?\}\{.+?\}	
\\.+?\{.+?\}\{.+?\}	 
\\.+?\{.+?\}\[.+?\]	 
\\.+?\[.+?\]\{.+?\}	 
\\.+?\{.+?\}	 
\\.+?\s	 
\\.+?$	 
\\.+?\n	\n
\|	
\{	
\}	
(\s*\n){3,}	\n'''

        self.ui_txt = r'''\\ui\{.+?}	
\\item\[.+?\]'''

        self.opener = FileOpener()
        self.parse_args()
        self.determine_task()        


    def parse_args(self):

        example = '''examples:
        wordig.py *.txt *.pdf
            Count characters and words. pdftotext.exe is required to count with PDF files.
        wordig.py -p *.pdf
            Count pages in PDF files.
        wordig.py -r -a "foo" *.txt
            Find "foo", searching through all subdirectories.
        wordig.py -b -a "foo" -s "goo" *.txt
            Make backup copies before replacing "foo" with "goo".
        wordig.py -P foo.tsv *.txt
            Find and replace using foo.tsv in which regular expressions are specified.
        wordig.py [-p foo.txt] -e *.tex 
            Extract and collect strings using the given pattern file. 
            If not specified otherwise, UI.txt, an accompanying file, is used.
        wordig.py -w *.txt
            Extract words.
        wordig.py -t *.tex
            Extract and collect macros and option keys from TeX files.
        wordig.py [-p foo.tsv] -d *.tex
            Remove macros from TeX files. 
            If not specified otherwise, detex.tsv, an accompanying file, is used.
        wordig.py -u "unicode 유니코드"
            Get the unicode code points and UTF-8 bytes for the given characters.
            The format of output is:
            Char  Dec  Hex  Bin  Bytes  Bits  Description
        '''

        parser = argparse.ArgumentParser(
            epilog = example,
            formatter_class = argparse.RawDescriptionHelpFormatter,
            # description = ''
        )

        parser.add_argument(
            'targets',
            nargs = '+',
            help = 'Specify one or more text files or characters.'
        )
        parser.add_argument(
            '-a',
            dest = 'aim',
            default = None,
            help = 'Specify a string to find.'
        )
        parser.add_argument(
            '-s',
            dest = 'substitute',
            default = None,
            help = 'Specify a string with which to replace found strings.'
        )
        parser.add_argument(
            '-b',
            dest = 'backup_bool',
            action = 'store_true',
            default = False,
            help = 'Make backup copies.'
        )
        parser.add_argument(
            '-P',
            dest = 'pattern',
            default = None,
            help = 'Specify a TSV or CSV file in which regular expressions are specified as substitution patterns.'
        )
        parser.add_argument(
            '-J',
            dest = 'to_autojosa_bool',
            action = 'store_true',
            default = False,
            help = 'Replace 조사 with 자동조사 macros in TeX files.'
        )
        parser.add_argument(
            '-j',
            dest = 'from_autojosa_bool',
            action = 'store_true',
            default = False,
            help = 'Replace 자동 조사 macros with 조사 in TeX files.'
        )
        parser.add_argument(
            '-e',
            dest = 'extract_string_bool',
            action = 'store_true',
            default = False,
            help = 'Extract specific strings referring to the given pattern file.'
        )  
        parser.add_argument(
            '-w',
            dest = 'extract_word_bool',
            action = 'store_true',
            default = False,
            help = 'Extract words.'
        )
        parser.add_argument(
            '-t',
            dest = 'extract_tex_bool',
            action = 'store_true',
            default = False,
            help = 'Extract macros from TeX files.'
        )              
        parser.add_argument(
            '-d',
            dest = 'detex_bool',
            action = 'store_true',
            default = False,
            help = 'Remove macros from TeX files.'
        )
        parser.add_argument(
            '-o',
            dest = 'output',            
            default = None,
            help = 'Specify a file name or suffix for output. The default varies according to options.'
        )

        parser.add_argument(
            '-r',
            dest = 'recursive_bool',
            action = 'store_true',
            default = False,
            help = 'Search through all subdirectories.'
        )
        parser.add_argument(
            '-p',
            dest = 'page_count_bool',
            action = 'store_true',
            default = False,
            help = 'Count PDF pages.'
        )
        parser.add_argument(
            '-U',
            dest = 'unicode_bool',
            action = 'store_true',
            default = False,
            help = 'Get the uncode information.',
        )        
        parser.add_argument(
            '-C',
            dest = 'convert_UTF_bool',
            action = 'store_true',
            default = False,
            help = 'Covert CP949-encoded files to UTF-8.'
        )
        parser.add_argument(
            '-D',
            dest = 'detect_UTF_bool',
            action = 'store_true',
            default = False,
            help = 'Detect if files are encoded in UTF-8 or not.'
        )

        self.args = parser.parse_args()

        if self.args.detex_bool and self.args.pattern is None:
            self.args.pattern = os.path.join(dirCalled, 'detex.tsv')
            if not os.path.exists(self.args.pattern):
                with open(self.args.pattern, mode='w', encoding='utf-8') as f:
                    f.write(self.detex_tsv)

        if self.args.extract_string_bool and self.args.pattern is None:
            self.args.pattern = os.path.join(dirCalled, 'UI.txt')
            if not os.path.exists(self.args.pattern):
                with open(self.args.pattern, mode='w', encoding='utf-8') as f:
                    f.write(self.ui_txt)

        if self.args.detect_UTF_bool:
            self.detector = UniversalDetector()


    def run_recursive(self, func):

        if self.args.recursive_bool:
            subdirs = [x[0] for x in os.walk('.')]
            for subdir in subdirs:
                for fnpattern in self.args.targets:
                    fnpattern = os.path.join(subdir, fnpattern)
                    for filename in glob.glob(fnpattern):
                        func(filename)
        else:
            for fnpattern in self.args.targets:
                for filename in glob.glob(fnpattern):
                    func(filename)


    def find(self, filename):

        print(filename)    
        try:
            with open(filename, mode='r', encoding='utf-8') as f:        
                for num, line in enumerate(f):                
                    if re.search(self.args.aim, line):
                        print('%5d:\t%s' %(num, line.replace('\n', ' ')))
        except:
            print('is not encoded in UTF-8.')


    def replace(self, filename):

        tmp = 't@mp.@@@'

        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                content = f.read() 
        except:
            print('%s is not encoded in UTF-8.' %(filename))
            return

        if self.args.pattern is None:
            content = re.sub(self.args.aim, self.args.substitute, content, flags=re.MULTILINE)
        else:
            ptrn_ext = os.path.splitext(self.args.pattern)[1].lower()
            with open(self.args.pattern, mode='r', encoding='utf-8') as ptrn:
                if ptrn_ext == '.tsv':
                    reader = csv.reader(ptrn, delimiter='\t')
                else:
                    reader = csv.reader(ptrn)
                for row in reader:  
                    if not row[0].startswith('`#'):
                        content = re.sub(row[0], row[1], content, flags=re.MULTILINE)
        
        with open(tmp, mode='w', encoding='utf-8') as f:
            f.write(content)
        
        if self.args.detex_bool:            
            base_name = os.path.splitext(filename)[0]
            if self.args.output is None:
                output = base_name + '_cleaned.txt'
            else:
                output = base_name + '_' + self.args.output + '.txt'
            if os.path.exists(output):
                os.remove(output)
            os.rename(tmp, output)
            self.opener.open_txt(output)                
        elif self.args.backup_bool:
            base_name, ext = os.path.splitext(filename)
            backup = base_name + '_bak' + ext
            if os.path.exists(backup):
                os.remove(backup)
            os.rename(filename, backup)
            os.rename(tmp, filename)
        else:
            if os.path.exists(filename):
                os.remove(filename)
            os.rename(tmp, filename)


    def extract_strings(self, filename):

        with open(self.args.pattern, mode='r', encoding='utf-8') as ptrn:
            macros = [line.rstrip() for line in ptrn]

        with open(filename, mode='r', encoding='utf-8') as f:
            content = f.read()

        for i in range(len(macros)):
            p = re.compile(macros[i])
            self.found += p.findall(content)


    def extract_words(self, filename):

        base_name, ext = os.path.splitext(filename)
        if self.args.output is None:
            output = base_name + '_words_extracted' +  ext
        else:
            output = base_name + '_' + self.args.output + ext

        with open(filename, mode='r', encoding='utf-8') as f:
            content = f.read()

        # remove numbers and tex macros
        for i in range(len(self.tex_patterns)):            
            content = re.sub(self.tex_patterns[i], '', content)    

        p = re.compile('\\w+')
        extracted = p.findall(content)
        extracted = set(extracted)
        content = '\n'.join(sorted(extracted))
        
        with open(output, mode='w', encoding='utf-8') as f:
            f.write(content)
        self.opener.open_txt(output)


    def extract_tex_macros(self, filename):

        with open(filename, mode='r', encoding='utf-8') as f:
            content = f.read()
        for i in range(len(self.tex_patterns)):
            p = re.compile(self.tex_patterns[i])
            self.found += p.findall(content)


    def check_if_pdf(self, filename):

        base_name, ext = os.path.splitext(filename)
        if ext.lower() == '.pdf':
            if texlive_bool:
                cmd = 'pdftotext -nopgbrk -raw -enc UTF-8 {}'.format(filename)
                os.system(cmd)            
                return(base_name + '.txt')
            else:
                return None
        else:
            return filename


    def count_words(self, filename):

        # Spaces are not counted as a character.
        lines, chars, words = 0, 0, 0

        filename = self.check_if_pdf(filename)
        f = open(filename, mode='r', encoding='utf-8')
        for line in f.readlines():
            lines += 1
            chars += len(line.replace(' ', '')) 
            this = line.split(None)
            words += len(this)
        f.close()

        print( '{}\n Lines: {:,}\n Words: {:,}\n Characters: {:,}\n'.format(filename, lines, words, chars) )
        self.lines += lines
        self.words += words
        self.chars += chars


    def count_pdf_pages(self, filename):

        with open(filename, 'rb') as f:
            pdf = PdfFileReader(f)
            pages = pdf.getNumPages()
        print('{}: {}'.format(filename, pages))
        self.pages += pages


    def convert_UTF(self, filename):

        with open(filename, mode='r', encoding='cp949') as f:
            content = f.read()
        output = filename.replace('.', '_UTF8.')
        with open(output, mode='w', encoding='utf-8') as f:
            f.write(content)
        self.opener.open_txt(output) 


    def align_string(self, string: str, width: int):

        nfc_string = unicodedata.normalize('NFC', string)
        wide_chars = [unicodedata.east_asian_width(c) for c in nfc_string]
        num_wide_chars = sum(map(wide_chars.count, ['W', 'F']))
        width = max(width-num_wide_chars, num_wide_chars)
        return '{:{w}}'.format(nfc_string, w=width)


    def detect_UTF(self, filename):

        self.detector.reset()

        with open(filename, 'rb') as f:
            lines = f.readlines()

        for line in lines:
            self.detector.feed(line)
            if self.detector.done: break

        self.detector.close()

        filename = os.path.basename(filename)
        if self.detector.result['encoding'] == 'utf-8':
            encoding = 'UTF-8'
        else:
            encoding = 'Other'
        print('{}: {}'.format(self.align_string(filename, 40), encoding))


    def write_collection(self):

        # remove duplicates and sort
        self.found = list(set(self.found))
        strings = '\n'.join(sorted(self.found, key=str.lower))
        with open(self.args.output, mode='w', encoding='utf-8') as f:
            f.write(strings)
        self.opener.open_txt(self.args.output)  

    def determine_task(self): 

        if self.args.unicode_bool:
            UTF = UnicodeDigger(chars=self.args.targets[0])
            UTF.print()
        elif self.args.to_autojosa_bool:
            self.args.aim = r'''(ref\{.+?\})([은는이가을를와과으로])'''
            self.args.substitute = r'''\1\\\2'''
            self.run_recursive(self.replace)
        elif self.args.from_autojosa_bool:
            self.args.aim = r'''\\([은는이가을를와과으로])'''
            self.args.substitute = r'''\1'''
            self.run_recursive(self.replace)

        elif self.args.pattern or self.args.aim:
            if self.args.pattern is None:
                if self.args.substitute is None:
                    self.run_recursive(self.find)
                else:
                    self.run_recursive(self.replace)
            else:            
                if os.path.exists(self.args.pattern):
                    if self.args.extract_string_bool:
                        if self.args.output is None:
                            self.args.output = 'strings_collected.txt'
                        self.run_recursive(self.extract_strings)
                        self.write_collection()
                        
                    else:
                        self.run_recursive(self.replace)
                else:
                    print('{} is not found.'.format(self.args.pattern))
        else:            
            if self.args.extract_word_bool:
                self.run_recursive(self.extract_words)
            elif self.args.extract_tex_bool:
                if self.args.output is None:
                    self.args.output = 'tex_macros_collected.tex'
                self.run_recursive(self.extract_tex_macros)  
                self.write_collection()
            elif self.args.convert_UTF_bool:
                self.run_recursive(self.convert_UTF)
            elif self.args.detect_UTF_bool:
                self.run_recursive(self.detect_UTF)
            elif self.args.page_count_bool:
                self.run_recursive(self.count_pdf_pages)
                print( 'Total pages: {:,}'.format(self.pages) )
            else:
                self.run_recursive(self.count_words)
                print( 'Total\n Lines: {:,}\n Words: {:,}\n Characters: {:,}\n'.format(self.lines, self.words, self.chars) )



class UnicodeDigger(object):

    def __init__(self, chars=None, totex=False):

        self.chars = chars
        self.totex_bool = totex


    def highlight_binary_code(self, dec, byte):
        # 31:red, 32:green, 33:yellow, 34:blue, 35:magenta, 36:cyan, 37: white
        if not self.totex_bool:
            head = '\x1b[37m'
            tail = '\x1b[36m'
            normal = '\x1b[0m'

        if self.totex_bool:
            if dec < int('0x80', 16):        
                byte = byte.zfill(8)
                return '{}\\codetail{{{}}}'.format(byte[:1], byte[1:])
            elif dec < int('0x800', 16):
                byte = byte.zfill(12)
                return '{}\\codetail{{{}}}'.format(byte[0:6], byte[6:])
            elif dec < int('0x10000', 16):
                byte = byte.zfill(16)
                return '{}\\codetail{{{}}}{}'.format(byte[0:4], byte[4:10], byte[10:16])
            else:
                byte = byte.zfill(24)
                return '{}\\codetail{{{}}}{}\\codetail{{{}}}'.format(byte[0:6], byte[6:12], byte[12:18], byte[18:24])
        else:
            if dec < int('0x80', 16):        
                byte = byte.zfill(8)
                return head + byte[:1] + tail + byte[1:] + normal
            elif dec < int('0x800', 16):
                byte = byte.zfill(12)
                return head + byte[0:6] + tail + byte[6:] + normal
            elif dec < int('0x10000', 16):
                byte = byte.zfill(16)
                return head + byte[0:4] + tail + byte[4:10] + head + byte[10:16] + normal
            else:
                byte = byte.zfill(24)
                return head + byte[0:6] + tail + byte[6:12] + head + byte[12:18] + tail + byte[18:24] + normal


    def highlight_binary_byte(self, byte_number, byte_index, byte):

        if self.totex_bool:
            head = '\\bytehead'
            tail = '\\bytetail'
        else:
            head = '\x1b[32m'
            tail = '\x1b[33m'
            normal = '\x1b[0m'

        if byte_index > 0: 
            if self.totex_bool:
                return '\\bytehead{{{}}}\\bytetail{{{}}}'.format(byte[:2], byte[2:])
            else:
                return head + byte[:2] + tail + byte[2:] + normal
        else:
            if self.totex_bool:
                if byte_number == 2:
                    return '\\bytehead{{{}}}\\bytetail{{{}}}'.format(byte[:3], byte[3:])
                elif byte_number == 3:                    
                    return '\\bytehead{{{}}}\\bytetail{{{}}}'.format(byte[:4], byte[4:])
                elif byte_number == 4:                    
                    return '\\bytehead{{{}}}\\bytetail{{{}}}'.format(byte[:5], byte[5:])
            else:
                if byte_number == 2:
                    return head + byte[:3] + tail + byte[3:] + normal
                elif byte_number == 3:
                    return head + byte[:4] + tail + byte[4:] + normal
                elif byte_number == 4:
                    return head + byte[:5] + tail + byte[5:] + normal


    def print(self):

        for char in self.chars:
            charname = unicodedata.name(char).lower()
            # decimal code points
            Dcode = ord(char)
            # hexadecimal code points
            Hcode = hex(Dcode).upper().replace('0X', '0x')
            # binary code points
            Bcode = bin(Dcode).replace('0b', '')
            # Bcode = Bcode.zfill(8)
            Bcode = self.highlight_binary_code(Dcode, Bcode)

            # hexadecimal UTF-8 bytes
            if Dcode > 127:
                Hbyte = str(char.encode('utf-8'))
                Hbyte = Hbyte.replace("b'\\x", "")
                Hbyte = Hbyte.replace("'", "")
                Hbyte = Hbyte.split('\\x')
                # binary UTF-8 bytes
                Bbyte = []
                for i, val in enumerate(Hbyte):
                    Hbyte[i] = val.upper()
                    bbyte = bin(int(val, 16)).replace('0b', '')
                    bbyte = self.highlight_binary_byte(len(Hbyte), i, bbyte)
                    Bbyte.append(bbyte)
                Hbyte = ''.join(Hbyte)
                Bbyte = ' '.join(Bbyte)
                if self.totex_bool:
                    print(char, Dcode, '\\tab', Hcode, Bcode, '\\tab', Hbyte, Bbyte, '\\\\')
                else:
                    print(char, Dcode, Hcode, Bcode, Hbyte, Bbyte, charname)
            else:
                if self.totex_bool:
                    print(char, Dcode, '\\tab', Hcode, Bcode, '\\\\')
                else:
                    print(char, Dcode, Hcode, Bcode, charname)


if __name__ == '__main__':    
    WordDigger()
