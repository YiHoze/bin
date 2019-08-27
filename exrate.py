import urllib.request
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(
    description = 'View exchage rates.'
)
parser.add_argument(
    'amount',
    nargs = '?',
    help = 'Specify an amount.'
)
parser.add_argument(
    '-c',
    dest = 'CNY',
    action = 'store_true',
    default = False,
    help = 'Chinese Yuan'
)
parser.add_argument(
    '-e',
    dest = 'EUR',
    action = 'store_true',
    default = False,
    help = 'Euro'
)

parser.add_argument(
    '-j',
    dest = 'JPY',
    action = 'store_true',
    default = False,
    help = 'Japanese yen'
)

args = parser.parse_args()

if args.amount is None:
    amount = 100
else:
    amount = float(args.amount)

if args.CNY:
    country = '중국 위안 CNY'
    currency = 'CNY'
elif args.EUR:
    country = '유럽연합 유로 EUR'
    currency = 'EUR'
elif args.JPY:
    country = '일본 엔 JPY'
    currency = 'JPY'
else:
    country = '미국 달러 USD'
    currency = 'USD'

URL = 'https://finance.naver.com/marketindex/exchangeDetail.nhn?marketindexCd=FX_USDKRW'
page = urllib.request.urlopen(URL)
soup = BeautifulSoup(page, 'html.parser')
exchange_rate = soup.find('option', text=country).attrs['value']

exchange_rate = float(exchange_rate)
won = '{:,.2f}'.format(exchange_rate)
print('1 %s = %s KRW' %(currency, won))

won_amount = amount * exchange_rate
foreign_amount = amount
won_amount = '{:,.2f}'.format(won_amount)
foreign_amount = '{:,.2f}'.format(foreign_amount)
print('%s %s = %s KRW' %(foreign_amount, currency, won_amount))

won_amount = amount
foreign_amount = (1 / exchange_rate) * amount
won_amount = '{:,.2f}'.format(won_amount)
foreign_amount = '{:,.2f}'.format(foreign_amount)
print('%s KRW = %s %s' %(won_amount, foreign_amount, currency))



