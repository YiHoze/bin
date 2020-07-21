# wordutil.py -b -u 가①⑴⒜ⓐⅰⅠㄱ㉠㉮㈀㈎
import os
import sys
import argparse
import glob 
import subprocess
import re
import unicodedata

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from open import FileOpener

class WordUtility(object):
    def __init__(self):
        self.tex_picked = 'tex_picked.txt'
        self.tortoise = r"""~~~FindAsIs
~~~WriteAsIs
~~~WC-OFF
\이 이
\가 가
\을 을
\를 를
\은 은
\는 는
\와 와
\과 과
\로 로
\으로 으로
\라 라
\이라 이라
~~~FindAsIs
~~~WriteInternal
~~~WC-ON
~~~FindAsIs
~~~WriteInternal
~~~WC-OFF
{
}
[
]
&"""

    def parse_args(self):

        example = '''examples:
    wordutil.py foo.txt
        Word and character counts are displayed.
    wordutil.py foo.txt
        This also counts words and characters. This option requires TeX Live.
    wordutil.py -U foo.txt
        foo_unicode.txt is created to show Unicode code points 
        except space, tab and line feed.
    wordutil.py -e -k foo.tex
        Words are extracted into foo_extracted.txt
        With "-k", numbers and TeX macros are also extracted.
    wordutil.py -t -g -tor foo.tex goo.tex
        TeX macros are extracted into foo_picked.txt and goo_picked.txt.
        With "-g", TeX macros are gathered into tex_picked.txt
        with "-tor", a brief description of the syntax of Tortoise Tagger 
            is added to the output. 
            Be aware that the output file is encoded in EUC-KR.'
    wordutil.py -b -u aZ가힣
        For the given characters, their UTF-8 bytes are analyzed.
        With "-u", uppercase letters are used for hexadecimal numbers.
    '''
        parser = argparse.ArgumentParser(
            epilog = example,  
            formatter_class = argparse.RawDescriptionHelpFormatter            
        )

        parser.add_argument(
            'files',
            type=str,
            nargs='+',
            help='Specify one or more text files, or characters to analyze their UTF-8 bytes.'
        )
        parser.add_argument(
            '-U',
            dest = 'unicode',
            action = 'store_true',
            default = False,
            help = 'View Unicode code points.'
        )
        parser.add_argument(
            '-e',
            dest = 'extract',
            action = 'store_true',
            default = False,
            help = 'Extract words.'
        )
        parser.add_argument(
            '-k',
            dest = 'keep',
            action = 'store_true',
            default = False,
            help = 'Keep numbers and TeX macros when extracting words.'
        )
        parser.add_argument(
            '-t',
            dest = 'tex',
            action = 'store_true',
            default = False,
            help = 'Extract TeX macros.'
        )
        parser.add_argument(
            '-g',
            dest = 'gather_tex',
            action ='store_true',
            default = False,
            help = 'Gather TeX macros from multiple files into one file. This is available only with "-t".'
        )
        parser.add_argument(
            '-tor',
            dest = 'tortoise',
            action = 'store_true',
            default = False,
            help = 'Add description of Tortoise Tagger to the output for reference. This is available only with "-t".'
        )
        parser.add_argument(
            '-s',
            dest = 'suffix',    
            help = 'Specify a suffix for output. The default varies by options.'
        )
        parser.add_argument(
            '-b',
            dest = 'utf_byte',
            action = 'store_true',
            default = False,
            help = 'Analyze UTF-8 bytes of given characters.',
        )
        parser.add_argument(
            '-u',
            dest='upper',
            action='store_true',
            default=False,
            help='Use uppercase for hexadecimal. This is available only with "-b".'
        )
        args = parser.parse_args()
        self.files = args.files
        self.unicode_bool = args.unicode
        self.extract_bool = args.extract
        self.with_tex_bool = args.keep
        self.tex_bool = args.tex
        self.gather_tex_bool = args.gather_tex
        self.tortoise_bool = args.tortoise
        self.suffix = args.suffix
        self.utf_byte_bool = args.utf_byte
        self.upper_bool = args.upper

    def check_TeXLive(self):
        try:
            subprocess.check_call('pdftotext -v')
            return True
        except OSError:
            print('pdftotext.exe is needed to deal with PDF files but not found')
            return False

    def determine_suffix(self):
        if self.suffix is None:
            if self.unicode_bool:
                self.suffix = 'unicode'
            elif self.tex_bool:
                self.suffix = 'picked'
            else:
                self.suffix = 'extracted'
        if self.tex_bool and self.gather_tex_bool:            
            return self.check_to_remove(self.tex_picked)
        else:
            return True                

    def determine_tex_patterns(self):
        # Extract TeX macros
        if self.tex_bool:
            self.tex_patterns = [
                r'\\[^a-zA-Z]', 
                r'\\[a-zA-Z*^|+]+',
                r'\\begin(\{.+?\}[*^|+]*)', 
                r'\s(\w+=)'
            ]
        # Extract words with TeX macros
        else:
            self.tex_patterns = [        
                r'\\begin(\{.+?\}[*^|+]*)',
                r'\\end\{.+?\}',
                r'\\[a-zA-Z*^|+]+',
                r'\\[^a-zA-Z]',         
                r'\w+=',
                r'\w*\d\w*'
            ]

    def check_to_remove(self, afile):
        if os.path.exists(afile):
            answer = input('%s alread exists. Are you sure to overwrite it? [y/N] ' %(afile))
            if answer.lower() == 'y':
                os.remove(afile)
                return True
            else:
                return False
        else:
            return True

    # Spaces are not counted as a character.
    def count_words(self, afile):
        lines, chars, words = 0, 0, 0
        f = open(afile, mode='r', encoding='utf-8')
        for line in f.readlines():
            lines += 1
            chars += len(line.replace(' ', '')) 
            this = line.split(None)
            words += len(this)
        f.close()
        msg = '%s\n Lines: %d\n Words: %d\n Characters: %d\n' % (afile, lines, words, chars)
        print(msg) 

    def extract_words(self, afile):    
        basename = os.path.splitext(afile)[0]
        output = '%s_%s.txt' %(basename, self.suffix)
        if self.check_to_remove(output) is False:
            return    
        with open(afile, mode='r', encoding='utf-8') as f:
            content = f.read()
        # remove numbers and tex macros
        if not self.with_tex_bool: 
            for i in range(len(self.tex_patterns)):            
                content = re.sub(self.tex_patterns[i], '', content)    
        p = re.compile('\\w+')
        extracted = p.findall(content)
        extracted = set(extracted)
        content = '\n'.join(sorted(extracted))
        with open(output, mode='w', encoding='utf-8') as f:
            f.write(content)
        opener = FileOpener()
        opener.OpenTxt(output) 

    def display_unicode(self, string):
        codes = ''
        for s in enumerate(string):
            c = s[1]
            if (c != '\n') and (c != ' ') and ( c != '\t'):
                codes += '%s\tU+%04X\t%s\n' %(c, ord(c), unicodedata.name(c).lower())
        return codes

    def get_unicode(self, afile):
        basename = os.path.splitext(afile)[0]
        output = '%s_%s.txt' %(basename, self.suffix)
        if self.check_to_remove(output) is False:
            return    
        with open(afile, mode='r', encoding='utf-8') as infile, open(output, mode='w', encoding='utf-8') as outfile:
            for line in infile.readlines():
                codes = self.display_unicode(line)
                outfile.write(codes)
        opener = FileOpener()
        opener.OpenTxt(output) 

    def check_if_pdf(self, afile):
        basename = os.path.basename(afile)
        filename, ext = os.path.splitext(basename)    
        if ext.lower() == '.pdf':
            if self.check_TeXLive():
                txt = filename + '.txt'
                if self.check_to_remove(txt) is False:
                    return None
                else:
                    cmd = 'pdftotext -nopgbrk -raw -enc UTF-8 %s' % (afile)
                    os.system(cmd)            
                    return txt
            else:
                return None
        else:
            return afile

    def pick_tex_macro(self, afile):
        found = []
        # read previously found macros
        if self.gather_tex_bool:
            output = self.tex_picked            
            if os.path.exists(output):
                if self.tortoise_bool:
                    with open(output, mode='r', encoding='euc-kr') as f:
                        found = f.read().split('\n')
                else:
                    with open(output, mode='r', encoding='utf-8') as f:
                        found = f.read().split('\n')
        else:
            basename = os.path.splitext(afile)[0]
            output = '%s_%s.txt' %(basename, self.suffix)
            if self.check_to_remove(output) is False:
                return        
        with open(afile, mode='r', encoding='utf-8') as f:
            content = f.read()
        # pick tex macros and keys
        for i in range(len(self.tex_patterns)):
            p = re.compile(self.tex_patterns[i])
            found += p.findall(content)            
        # remove duplicates and sort
        found = set(found)
        macros = '\n'.join(sorted(found, key=str.lower))
        if self.tortoise_bool:
            macros = self.tortoise + macros
            with open(output, mode='w', encoding='euc-kr') as f:
                f.write(macros)
        else:
            with open(output, mode='w', encoding='utf-8') as f:
                f.write(macros)
        opener = FileOpener()
        opener.OpenTxt(output) 

    def determine_task(self):
        if self.utf_byte_bool:
            utf = UTFanalyzer(chars=self.files[0], upper=self.upper_bool)
            utf.show()
        else:
            if not self.determine_suffix():
                return
            self.determine_tex_patterns()
            for fnpattern in self.files:
                for afile in glob.glob(fnpattern):
                    afile = self.check_if_pdf(afile)
                    if afile is not None:
                        if self.extract_bool:
                            self.extract_words(afile)
                        elif self.unicode_bool:
                            self.get_unicode(afile)
                        elif self.tex_bool:                
                            self.pick_tex_macro(afile)
                        else:
                            self.count_words(afile)

class UTFanalyzer(object):

    def __init__(self, chars=None, upper=False):
        self.chars = chars
        self.upper_bool = upper

    def highlight_Bcode(self, dec, byte):
        # 31:red, 32:green, 33:yellow, 34:blue, 35:magenta, 36:cyan, 37: white
        head = '\x1b[37m'
        tail = '\x1b[36m'
        normal = '\x1b[0m'

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

    def highlight_Bbyte(self, byte_number, byte_index, byte):
        head = '\x1b[32m'
        tail = '\x1b[33m'
        normal = '\x1b[0m'
        if byte_index > 0: 
            return head + byte[:2] + tail + byte[2:] + normal
        else:
            if byte_number == 2:
                return head + byte[:3] + tail + byte[3:] + normal
            elif byte_number == 3:
                return head + byte[:4] + tail + byte[4:] + normal
            elif byte_number == 4:
                return head + byte[:5] + tail + byte[5:] + normal

    def show(self):
        for char in self.chars:
            # decimal code points
            Dcode = ord(char)
            # hexadecimal code points
            Hcode = hex(Dcode).replace('0x', '')
            if self.upper_bool:
                Hcode = Hcode.upper()
            # binary code points
            Bcode = bin(Dcode).replace('0b', '')
            # Bcode = Bcode.zfill(8)
            Bcode = self.highlight_Bcode(Dcode, Bcode)
            # hexadecimal UTF-8 bytes
            if Dcode > 127:
                Hbyte = str(char.encode('utf-8'))
                Hbyte = Hbyte.replace("b'\\x", "")
                Hbyte = Hbyte.replace("'", "")
                Hbyte = Hbyte.split('\\x')
                # binary UTF-8 bytes
                Bbyte = []
                for i, val in enumerate(Hbyte):
                    if self.upper_bool:
                        Hbyte[i] = val.upper()
                    bbyte = bin(int(val, 16)).replace('0b', '')
                    bbyte = self.highlight_Bbyte(len(Hbyte), i, bbyte)
                    Bbyte.append(bbyte)
                Hbyte = ' '.join(Hbyte)
                Bbyte = ' '.join(Bbyte)
                print(char, Dcode, Hcode, Bcode, Hbyte, Bbyte)
            else:
                print(char, Hcode, Bcode)

if __name__ == '__main__':
    wordutil = WordUtility()
    wordutil.parse_args()
    wordutil.determine_task()
