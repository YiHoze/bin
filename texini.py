import os, sys, glob, argparse, configparser
import subprocess

# Read the initiation file to get the data required for configuration of the environment for latex.
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
else:
    print('Docenv.ini is not found. Set the DOCENV environment variable to the directory containing docenv.ini.')
    sys.exit()

# Get arguments
parser = argparse.ArgumentParser(
    description ='Configure your environment for LaTeX.'
)
parser.add_argument(
    '-s',
    dest = 'store_to_local',
    action = 'store_true',
    default = False,
    help = 'Copy the provided latex style files into the local TeXMF directory.'
)
parser.add_argument(
    '-d',
    dest = 'docenv',
    action = 'store_true',
    default = False,
    help = 'Specify the directory where executable files and relevant files of this documentation system are located to set the path as an environment variable.'
)
parser.add_argument(
    '-p',
    dest = 'sumatrapdf',
    action = 'store_true',
    default = False,
    help = 'Set SumatraPDF to enable inverse search. (jumping back to the corresponding point in the source tex file)'
)
parser.add_argument(
    '-e',
    dest = 'texedit',
    action = 'store_true',
    default = False,
    help = 'Set TEXEDIT as an environment variable.'
)
parser.add_argument(
    '-home',
    dest = 'texmfhome',
    action = 'store_true',
    default = False,
    help = 'Set TEXMFHOME as an environment variable.'
)
parser.add_argument(
    '-cnf',
    dest = 'texmf_cnf',
    action = 'store_true',
    default = False,
    help = "Add user's local font directory to texmf.cnf."
)
parser.add_argument(
    '-local',
    dest = 'local_conf',
    action = 'store_true',
    default = False,
    help = "Create local.conf that contains user's local font directory."
)
parser.add_argument(
    '-c',
    dest = 'cache_font',
    action = 'store_true',
    default = False,
    help = 'Cache fonts for XeLaTeX.'
)
parser.add_argument(
    '-l',
    dest = 'luaotfload',
    action = 'store_true',
    default = False,
    help = 'Update the font database for LuaLaTeX.'
)
parser.add_argument(
    '-u',
    dest = 'update_texlive',
    action = 'store_true',
    default = False,
    help = 'Update TeX Live.'
)
args = parser.parse_args()

def store_to_local():
    print('\n[Copying latex style files]')   
    try:
        latex_style = config.get('Sphinx Style', 'latex')
        texmf_local = config.get('TeX Live', 'texmflocal')
    except:
        print('Make sure to have docenv.ini set properly.')
        return
    answer = input('These files are going to be copied into <%s>\n%s\nEnter Y to proceed, N to abandon, or another directory: ' %(texmf_local, latex_style.replace(', ', '\n')))
    if (answer.lower() == 'n'):
        return
    if not (answer.lower() == 'y' or answer == ''):
        texmf_local = answer
    files = latex_style.split()
    for afile in files:        
        src = os.path.join(inipath, afile)
        cmd = 'copy %s %s' %(src, texmf_local) 
        os.system(cmd)        
    dst = os.path.join(texmf_local, '*.*')
    for afile in glob.glob(dst):
        print(afile)
    os.system('mktexlsr')

def set_docenv():
    print('\n[Setting DOCENV]')    
    try:
        docenv = config.get('DocEnv', 'path')
    except:
        print('Make sure to have docenv.ini set properly.')
        return
    answer = input('Are you sure to set the DOCENV environment variable to <%s>?\nEnter [Y] to proceed, [n] to abandon, or another directory: ' %(docenv))
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        docenv = answer
    cmd = "powershell \"set-itemproperty -path HKCU:\\Environment -name DOCENV -value '%s'\"" % (docenv)
    os.system(cmd)
    cmd = "powershell \"(get-itemproperty -path HKCU:\\Environment).'DOCENV'\""
    os.system(cmd)

def set_texedit():
    print('\n[Setting TEXEDIT]')    
    try:    
        texedit = config.get('TeX Live', 'TEXEDIT')
    except:
        print('Make sure to have docenv.ini set properly.')
        return
    answer = input('Are you sure to set the TEXEDIT environment variable to  <%s>?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: ' %(texedit))
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        texedit = answer
    cmd = "powershell \"set-itemproperty -path HKCU:\\Environment -name TEXEDIT -value '%s'\"" % (texedit)
    os.system(cmd)
    cmd = "powershell \"(get-itemproperty -path HKCU:\\Environment).'TEXEDIT'\""
    os.system(cmd)

def set_texmfhome():
    print('\n[Setting TEXMFHOME]')    
    try:
        texmfhome = config.get('TeX Live', 'TEXMFHOME')
    except:
        print('Make sure to have docenv.ini set properly.')
        return
    answer = input('Are you sure to set the TEXMFHOME environment variable to  <%s>?\nEnter [Y] to proceed, [n] to abandon, or another path: ' %(texmfhome))
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        texmfhome = answer
    cmd = "powershell \"set-itemproperty -path HKCU:\\Environment -name TEXMFHOME -value '%s'\"" % (texmfhome)
    os.system(cmd)
    cmd = "powershell \"(get-itemproperty -path HKCU:\\Environment).'TEXMFHOME'\""
    os.system(cmd)

def update_texlive():
    print('\n[Updating TeX Live]')    
    try:
        repository = config.get('TeX Live', 'repository')
    except:
        print('Make sure to have docenv.ini set properly.')
        return
    answer = input('Are you sure to use the <%s> repository to update the TeX Live?\nEnter [Y] to proceed, [n] to abandon, or another repository: ' %(repository))
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        repository = answer
    cmd = 'tlmgr option repository %s' %(repository)
    os.system(cmd)
    cmd = 'tlmgr update --self --all'
    os.system(cmd)

def set_sumatrapdf():
    print('\n[Setting SumatraPDF')
    try:
        sumatra = config.get('SumatraPDF', 'path')
        editor = config.get('SumatraPDF', 'inverse-search')
    except:
        print('Make sure to have docenv.ini set properly.')
        return
    answer = input('Are you sure to use <%s> to enable the inverse search feature of SumatraPDF?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: ' %(editor))
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        editor = answer    
    cmd = []
    cmd.append(sumatra)
    cmd.append('-inverse-search')
    cmd.append(editor)    
    subprocess.Popen(cmd)

def modify_texmf_cnf():
    print('\n[texmf.cnf]')
    try:
        texmf_cnf = config.get('TEXMF.CNF', 'path')
        target = config.get('TEXMF.CNF', 'target')
        substitute = config.get('TEXMF.CNF', 'substitute')
    except:
        print('Make sure to have docenv.ini set properly')
        return
    answer = input("'%s' will be replaced with '%s' in <%s>\nEnter [Y] to proceed, [n] to abandon." %(target, substitute, texmf_cnf))
    if (answer.lower() == 'n'):
        return
    with open(texmf_cnf, mode='r') as f:
        content = f.read()
        content = content.replace(target, substitute)
    with open(texmf_cnf, mode='w') as f:
        f.write(content)

def create_local_conf():
    print('\n[local.conf]')
    try:
        local_conf = config.get('LOCAL.CONF', 'path')
        content = config.get('LOCAL.CONF', 'content')
    except:
        print('Make sure to have docenv.ini set properly')
        return
    if os.path.exists(local_conf):
        print('<%s> already exists' %(local_conf))
        return
    answer = input("<%s> will be created to include %s\nEnter [Y] to proceed, [n] to abandon." %(local_conf, content))
    if (answer.lower() == 'n'):
        return
    with open(local_conf, mode='w') as f:
        f.write(content)

def cache_font():
    print('\n[Caching fonts]')
    answer = input('Are you sure to cache fonts?\nEnter [Y] to proceed or [n] to abandon: ')
    if (answer.lower() == 'y' or answer == ''):
        cmd = 'fc-cache -v -r'
        os.system(cmd)     

def luaotfload():    
    answer = input('Are you sure to update the font database?\nEnter [Y] to proceed or [n] to abandon: ')
    if (answer.lower() == 'y' or answer == ''):
        cmd = 'luaotfload-tool --update --force --verbose=3'
        os.system(cmd)     

if args.store_to_local:
    store_to_local()
if args.docenv:
    set_docenv()
if args.update_texlive:
    update_texlive()
if args.texedit:
    set_texedit()
if args.texmfhome:
    set_texmfhome()
if args.sumatrapdf:
    set_sumatrapdf()
if args.texmf_cnf:
    modify_texmf_cnf()
if args.local_conf:
    create_local_conf()
if args.cache_font:
    cache_font()
if args.luaotfload:
    luaotfload()
