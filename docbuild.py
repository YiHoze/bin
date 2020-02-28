import os, sys, glob, argparse, subprocess

# the directory where this script is called out
dirCalled = os.path.dirname(sys.argv[0])

# Get arugments.
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
    '-tf',
    dest = 'tex_filename',
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
parser.add_argument(
    '-x',
    dest = 'noImage',
    action = 'store_true',
    default = False,
    help = 'Pass over image processing.'
)
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
    '-cl',
    dest = 'clear',
    action = 'store_true',
    default = False,
    help = 'Clear the build directory.'
)
# args = parser.parse_args()
args, unknown_args = parser.parse_known_args()

def build_html():
    if args.renew:
        cmd = 'sphinx-build -b html -a -E . _build/html' 
    else:
        cmd = 'sphinx-build -M html . _build'     
    os.system(cmd)

def build_latex():  
    # curDir = os.getcwd() 
    for afile in glob.glob('_build/latex/blockdiag-*.pdf'):
        os.remove(afile)

    if args.renew:
        cmd = 'sphinx-build -b latex -a -E . _build/latex'
    else:
        cmd = 'sphinx-build -M latex . _build'         
    os.system(cmd)

    os.chdir('_build/latex')
    # Remove unnecessary files
    if not args.keep_collateral:
        files = ['sphinxhowto.cls', 'sphinxmanual.cls', 'python.ist', 'make.bat', 'Makefile', 'LatinRules.xdy', 'LICRcyr2utf8.xdy', 'LICRlatin2utf8.xdy', 'sphinx.xdy', 'latexmkjarc', 'latexmkrc', 'Makefile']
        for afile in files:
            if os.path.exists(afile):
                os.remove(afile)
    # Replace '을' with '\을'
    if args.AutoJosa:
        processor = os.path.join(dirCalled, 'autojosa.py')
        subprocess.call(['python', processor, args.tex_filename])
    # Covert SVG images to PDF and crop PDF images
    if not args.noImage:
        processor = os.path.join(dirCalled, 'iu.py')
        subprocess.call('python %s -t pdf -rec *.svg' %(processor)) 
        for afile in glob.glob('blockdiag-*.pdf'):
            cmd = 'pdfcrop.exe %s %s' %(afile, afile)
            os.system(cmd)    
    # Run xelatex to make PDF
    if not args.noCompile:
        processor = os.path.join(dirCalled, 'ltx.py')
        options = ' '.join(unknown_args)
        subprocess.call('python %s %s %s' %(processor, options, args.tex_filename))     
    # os.chdir('../..')

def clear_build():
    cmd = 'sphinx-build -M clean . _build'
    os.system(cmd)

if args.clear:
    clear_build()      
elif args.format == 'html':
    build_html()
elif args.format == 'latex':
    build_latex()

