import argparse, csv, os

parser = argparse.ArgumentParser(
    description = 'Calculate room rates for Bongsua.'
)
parser.add_argument(
    'nights',
    nargs = '?',
    type = int,
    help = 'Specify how many nights to stay.'
)
parser.add_argument(
    '-p',
    dest = 'price',
    type = int,
    default = 50000,
    help = 'Specify the unit price for one night. The default is 50000 KRW.'
)
parser.add_argument(
    '-d',
    dest = 'discount_rate',
    type = int,
    default = 20,
    help = 'Specify the discount rate for two or more nights. The default is 20(%%).'
) 
parser.add_argument(
    '-m',
    dest = 'matrix',
    action = 'store_true',
    default = False,
    help = 'Show the matrix of room rates.'
)
args = parser.parse_args()

def room_rate(nights):
    price = '{:,}'.format(args.price)    
    print('Price per night: %s\nDiscount rate: %d%%' %(price, args.discount_rate))
    for n in range(1, nights+1):
        roomrate = n * args.price - (n - 1) * args.price * args.discount_rate / 100
        roomrate = '{:,}'.format(int(roomrate))
        print('%2d nights: %7s' %(n, roomrate))

def room_rate_matrix(price):    
    m = []
    m.append([])
    m[0].append('')
    for d in range (5, 55, 5):
        d = "%d%%" %(d)
        m[0].append(d)
    # print(m[0])
    for n in range (1, 11):
        m.append([])
        m[n].append(n)
        for d in range (5, 55, 5):
            r = n * price - (n - 1) * price * d / 100
            r = '{:,}'.format(int(r))
            m[n].append(r)
        # print(m[n])
    
    with open(output_file, mode='a', encoding='utf-8') as result:
        writer = csv.writer(result, delimiter='\t', lineterminator='\n')
        for i in range(len(m)):
            writer.writerow(m[i])  

if args.matrix:
    output_file = 'roomrate.tsv'
    if os.path.exists(output_file):
        os.remove(output_file)
    for p in range (30000, 65000, 5000):
        room_rate_matrix(p)
elif args.nights is None:
    room_rate(10)
else:
    room_rate(args.nights)