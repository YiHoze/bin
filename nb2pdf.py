import os, sys, glob, argparse, configparser, subprocess

dirCalled = os.path.dirname(sys.argv[0])

# Read the initiation file to get Jupyter templates.
try:
    inipath = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    inipath = False
if inipath is False:
    inipath = os.path.dirname(sys.argv[0])
ini = os.path.join(inipath, 'docenv.ini')
if os.path.exists(ini):
    config = configparser.ConfigParser()
    config.read(ini)
    try:
        latex_template = config.get('Jupyter Template', 'latex')
        latex_template = os.path.join(inipath, latex_template)
    except:
        print('Make sure to have docenv.ini set properly.')
        sys.exit()
else:
    print('Docenv.ini is not found. Set the DOCENV environment variable to the directory containing docenv.ini.')
    sys.exit()    

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
    dest = 'latex_template',
    default = latex_template,
    help = 'To use another latex template, specify the path to it.'
)
parser.add_argument(
    '-n',
    dest = 'passover',
    action = 'store_true',
    default = False,
    help = 'Pass over latex compilation.'
)
parser.add_argument(
    '-v',
    dest = 'view',
    action = 'store_true',
    default = False,
    help = 'Open the resulting PDF file to view.'
)

args = parser.parse_args()

if not os.path.exists(args.latex_template):
    print('%s is not found.' %(args.latex_template))
    sys.exit()

def notebook_convert(afile):
    if afile.endswith('.ipynb'):    
        filename = os.path.splitext(afile)[0]
        filename = os.path.basename(afile)
        basename = os.path.splitext(filename)[0]
        tex = basename + '.tex'
        pdf = basename + '.pdf'
        # Convert to tex
        cmd = 'jupyter nbconvert --to=latex --template=%s --SVG2PDFPreprocessor.enabled=True %s' %(args.latex_template, afile)
        os.system(cmd)        
        # Compile tex
        if not args.passover:
            if os.path.exists(tex):
                cmd = 'xelatex -interaction=batchmode %s' %(tex)
                os.system(cmd)
                os.system(cmd)
                processor = os.path.join(dirCalled, 'ltx.py')
                subprocess.call(['python', processor, '-c'])
                if args.view:
                    if os.path.exists(pdf):        
                        processor = os.path.join(dirCalled, 'open.py')    
                        subprocess.call(['python', processor, pdf])
    else:
        print('%s is not a Jupyter notebook.' %(afile))

for fnpattern in args.ipynb:
    for afile in glob.glob(fnpattern):
        notebook_convert(afile)

