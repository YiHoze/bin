import argparse, math

parser = argparse.ArgumentParser(
    description = 'Calculate slope gradients.'
)
parser.add_argument(
    'level',
    nargs = '*',
    help = 'Enter one or more numbers.'
)
parser.add_argument(
    '-p',
    dest = 'p2d',
    action = 'store_true',
    default = False,
    help = 'Show the percent-to-degree table.'
)
parser.add_argument(
    '-d',
    dest = 'd2p',
    action = 'store_true',
    default = False,
    help = 'Show the degree-to-percent table.'
)
args = parser.parse_args()

# 1° = π/180 radian
# 1 radian = 180/π

def percent_to_degree(percent):
    percent = round(float(percent))
    degree = math.degrees(math.atan(percent/100))
    print('%d%% = %.1f°' %(percent, degree))

def degree_to_percent(degree):
    degree = float(degree)
    percent = math.tan(math.radians(degree)) * 100
    percent = round(percent, 1)
    print('%.1f° = %.1f%%' %(degree, percent))

if args.p2d:
    for i in range(101):
        percent_to_degree(i)
if args.d2p:
    for i in range(46):
        degree_to_percent(i)

for i in args.level:
    percent_to_degree(i)
    degree_to_percent(i)
