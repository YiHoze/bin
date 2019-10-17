import argparse

parser = argparse.ArgumentParser(
    description = 'Calculate monthly savings.'
)
parser.add_argument(
    'deposit',
    nargs = '?',
    type = int,
    help = 'Specify an amount of money to deposit monthly.'
)
parser.add_argument(
    '-m',
    dest = 'months',
    type = int,
    default = 12,
    help = 'Specify months to invest. The default is 12.'
)
parser.add_argument(
    '-r',
    dest = 'rate',
    type = int,
    default = 3,
    help = 'Specify the annual interest rate. The default is 3(%%).'
)
args = parser.parse_args()

def installment():
    D = args.deposit
    M = args.months
    # simple interest rate
    SR = args.rate / 100
    # compoound interest rate
    CR = 1 + args.rate / 100
    # total deposits
    TD = D * M 
    # future savings with simple interest 
    FSS = (D * M) + (D * M * (M+1)/2 * SR/12) 
    # future savings with compound interest 
    FSC = D * (CR**((M+1)/12) - CR**(1/12)) / (CR**(1/12)-1)
    # simple interest earned
    SI = FSS - TD
    # compound interest earned
    CI = FSC - TD
    TD = '{:,}'.format(TD)
    FSS = '{:,}'.format(int(FSS))
    FSC = '{:,}'.format(int(FSC))
    SI = '{:,}'.format(int(SI))
    CI = '{:,}'.format(int(CI))
    output = """INSTALLMENT
    Future savings with simple interest: %s = %s + %s
    Future savings with compound interest: %s = %s + %s
    """ %(FSS, TD, SI, FSC, TD, CI)
    print(output)

def deposit():
    D = args.deposit
    M = args.months
    # annual rate
    AR = args.rate / 100
    # monthly rate
    MR = args.rate / 100 / 12
    # future savings with simple interest
    FSS = D * (1 + AR * M / 12)
    # future savings with monthly compound interest
    FSAC = D * (1 + AR) ** (M / 12)
    # future savings with annual compound interest
    FSMC = D * (1 + MR) ** M
    FSS = '{:,}'.format(int(FSS))
    FSAC = '{:,}'.format(int(FSAC))
    FSMC = '{:,}'.format(int(FSMC))
    output = """DEPOSIT
    Future savings with simple interest: %s 
    Future savings with monthly compound interest: %s 
    Future savings with annual compound interest: %s 
    """ %(FSS, FSAC, FSMC)
    print(output)


if args.deposit is None:
    parser.print_help()
else:
    installment()
    deposit()