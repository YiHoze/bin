import os, sys, glob, argparse, configparser, subprocess

# Read the initiation file to get the path to a text editor and its option.
try:
    inipath = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    inipath = False
if inipath is False:
    inipath = os.path.dirname(sys.argv[0]) # the directory where this script exists.
ini = os.path.join(inipath, 'docenv.ini')
if os.path.exists(ini):
    config = configparser.ConfigParser()
    config.read(ini)
    try:
        TextEditorPath = config.get('Text Editor', 'path')
        TextEditorOption = config.get('Text Editor', 'option')
        associations = config.get('Text Editor', 'associations')
        AdobeReaderPath = config.get('Adobe Reader', 'path')
    except:
        print('Make sure to have docenv.ini set properly.')
        sys.exit()
else:
    print('Docenv.ini is not found. Set the DOCENV environment variable to the directory containing docenv.ini.')
    sys.exit() 

# Get arguments
parser = argparse.ArgumentParser(
    description='Open text files and others with an appropriate application.'
)
parser.add_argument(
    'files',
    nargs='+',
    help='Specify files to open.'
)
parser.add_argument(
    '-s',
    dest='texlive',
    action='store_true',
    default=False,
    help='Search TeX Live for the specified file to find and open.'
)
parser.add_argument(
    '-e',
    dest='editor',
    default=TextEditorPath,
    help='Specify a different text editor to use it.'
)
parser.add_argument(
    '-o',
    dest='option',
    default=TextEditorOption,
    help='Specify options for the text editor.'
)
parser.add_argument(
    '-a',
    dest = 'Adobe',
    action = 'store_true',
    help = 'Use Adobe Reader to view PDF.'
)
args = parser.parse_args()

def DetermineFileType(afile):
    ext = os.path.splitext(afile)[1]        
    if ext.lower() in associations:
        return('txt')
    elif ext.lower() == '.pdf':
        return('pdf')
    else:
        return('another')

def OpenHere():
    for fnpattern in args.files:
        for afile in glob.glob(fnpattern):
            filetype = DetermineFileType(afile)
            if filetype == 'txt':
                cmd = '\"%s\" %s %s' % (args.editor, args.option, afile)
                os.system(cmd)                
            elif filetype == 'pdf':
                if args.Adobe:
                    cmd = '\"%s\" %s' % (AdobeReaderPath, afile)                                 
                    subprocess.Popen(cmd, stdout=subprocess.PIPE)
                else:
                    cmd = 'start %s' % (afile)
                    os.system(cmd)
            else:
                cmd = 'start %s' % (afile)
                os.system(cmd)

def SearchTeXLive():
    for afile in args.files:
        try:
            result = subprocess.check_output(['kpsewhich', afile], stderr=subprocess.STDOUT)
            gist = str(result, 'utf-8')
            cmd = '\"%s\" %s %s' % (args.editor, args.option, gist)            
            os.system(cmd)
        except subprocess.CalledProcessError:
                print('%s is not found in TeX Live.' % (afile))

if args.texlive:
    SearchTeXLive()
else:
    OpenHere()