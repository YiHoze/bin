import argparse

parser = argparse.ArgumentParser(
    description = 'Sum numbers in a range with an increase.'
)
parser.add_argument(
    'ending_number',
    type = int,
    nargs = 1,
    help = 'Enter an ending number.'
)
parser.add_argument(
    '-s',
    dest = 'starting_number',
    type = int,
    default = 1,
    help = 'Specify a starting number. (default: 1)'
)
parser.add_argument(
    '-i',
    dest = 'increase',
    type = int,
    default = 1,
    help = 'Specify an increase. (default: 1)'
)
args = parser.parse_args()

last = args.ending_number[0] + 1
sum = 0
print('Count Increased Sum')
for n in range(last):
    if n >= args.starting_number:
        increase = n * args.increase
        sum = sum + increase
        print(n, increase, sum)