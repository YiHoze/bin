import os, sys, glob, argparse, subprocess

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
    '-X', 
    dest = 'noCompile',
    action = 'store_true',
    default = False,
    help = 'Disable latex compilation.'
)
parser.add_argument(
    '-j',
    dest = 'AutoJosa',
    action = 'store_true',
    default = False,
    help = 'Replace with 자동조사.'
)
parser.add_argument(
    '-N',
    dest = 'noImage',
    action = 'store_true',
    default = False,
    help = 'Disable image processing.'
)
parser.add_argument(
    '-r',
    dest = 'renew',
    action = 'store_true',
    default = False,
    help = 'Read and write all files anew.'
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
        cmd = 'sphinx-build -a -E . _build/html' 
    else:
        cmd = 'sphinx-build -M html . _build'     
    os.system(cmd)

def build_latex():  
    # curDir = os.getcwd() 
    for afile in glob.glob('_build/latex/blockdiag-*.pdf'):
        os.remove(afile)

    if args.renew:
        cmd = 'sphinx-build -a -E . _build/latex'
    else:
        cmd = 'sphinx-build -M latex . _build'         
    os.system(cmd)

    os.chdir('_build/latex')
    tex = glob.glob('*.tex')[0]
    if args.AutoJosa:
        # cmd = 'powershell -command autojosa.py %s' %(tex)
        # os.system(cmd)
        processor = os.path.join(dirCalled, 'autojosa.py')
        subprocess.call(['python', processor, tex])

    if not args.noImage:
        # if os.path.exists('images'):
        #     cmd = 'svg2pdf.exe images/*.svg'    
        # os.system(cmd)
        processor = os.path.join(dirCalled, 'iu.py')
        subprocess.call(['python', processor, '*.svg'])
        for afile in glob.glob('blockdiag-*.pdf'):
            cmd = 'pdfcrop.exe %s %s' %(afile, afile)
            os.system(cmd)    

    if not args.noCompile:
        processor = os.path.join(dirCalled, 'ltx.py')
        options = ' '.join(unknown_args)
        subprocess.call(['python', processor, tex, options])
    
    # os.chdir('../..')

def clear_build():
    cmd = 'sphinx-build -M clean . _build'
    os.system(cmd)

# def compile_fully():
#     os.system(cmd_tex)
#     os.system(cmd_tex)
#     if os.path.exists(idx):
#         cmd = 'texindy -M ' + ind_mod + idx
#         os.system(cmd)        
#         if args.BookmarkPython:
#             cmd = 'powershell -command bmind.py -p ' + ind
#             os.system(cmd)
#         os.system(cmd_tex)
#     os.system(cmd_tex)
#     if not args.KeepAux:
#         os.system('texclean.py')
#         files = ['sphinxhowto.cls', 'sphinxmanual.cls', 'sphinx.sty', 'python.ist', 'Makefile', 'latexmkrc', 'latexmkjarc']        
#         for afile in files:
#             if os.path.exists(afile):
#                 os.remove(afile)



if args.clear:
    clear_build()      
elif args.format == 'html':
    build_html()
elif args.format == 'latex':
    build_latex()

