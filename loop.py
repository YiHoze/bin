import argparse, re, os, glob

parser = argparse.ArgumentParser(
    description = 'Repeat a command to process multiple files that contain serial numbers.'
)
parser.add_argument(
    'command',
    type = str,
    nargs = 1,
    help = 'Type a command in quotation marks.'
)
parser.add_argument(
    '-b',
    dest = 'begin',
    default = 1,
    help = 'Specify the beginning number.'
)
parser.add_argument(
    '-e',
    dest = 'end',
    default = 0,
    help = 'Specify the ending number.'
)

parser.add_argument(
    '-l',
    dest = 'leading',
    action = 'store_true',
    default = False,
    help = 'Do add a leading zero to single-digit numbers.'
)
args = parser.parse_args()

if args.end == 0:
    p = re.compile(r'\s.*\*.*\s')
    result = p.search(args.command[0])
    fnpattern = result.group()
    fnpattern = fnpattern.replace(' ', '')    
    files = glob.glob(fnpattern)
    args.end = len(files)
    
cnt = args.begin
while cnt <= args.end:
    if args.leading:
        cntstr = "{:02d}".format(cnt)
    else:
        cntstr = str(cnt)
    cmd = re.sub(r'\*', cntstr, args.command[0])
    os.system(cmd)    
    cnt += 1