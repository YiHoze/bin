import urllib.request
from bs4 import BeautifulSoup
import argparse
import re

class ExchangeRate(object):
    def __init__(self, amount=1.0, currency='USD', list=False):
        self.amount = amount
        self.currency = currency
        self.list_bool = list
        
        URL = 'https://finance.naver.com/marketindex/exchangeDetail.nhn?marketindexCd=FX_USDKRW'
        page = urllib.request.urlopen(URL)
        self.soup = BeautifulSoup(page, 'html.parser')  

        # getting currencies from <select>
        lines = ''        
        for i in self.soup.find_all('option'):              
            lines = lines + str(i) + '\n'        
        p = re.compile('>(.+?)<')
        found = p.findall(lines)
        i = 0
        while i < len(found):
            found[i] = found[i].strip()
            i += 1
        found = set(found)
        self.currencies = {}
        for i in found:
            words = i.split()
            self.currencies[words[-1]] = i      

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'View exchage rates.'
        )
        parser.add_argument(
            'amount',
            nargs = '?',
            type = float,
            default = 1.0,
            help = 'Specify an amount.'
        )
        parser.add_argument(
            dest = 'currency',
            nargs = '?',
            default = 'USD',
            help = 'specify a currency. (default: USD) '
        )
        parser.add_argument(
            '-l',
            dest = 'list',
            action = 'store_true',
            default = False,
            help = 'Show the ist of currencies.'
        )        
        args = parser.parse_args()
        self.amount = args.amount
        self.currency = args.currency
        self.list_bool = args.list

    def show_currencies(self):
        for i in sorted(self.currencies.values()):
            print(i)

    def calcurate(self):
        self.currency = self.currency.upper()
        try:
            exchange_rate = self.soup.find('option', text=self.currencies[self.currency]).attrs['value']
        except:
            print('Make sure the currency abbreviation is correct.')
            return
        basis = self.soup.find('option', text=self.currencies[self.currency]).attrs['label']
        # foreign : KRW for the basis
        exchange_rate = float(exchange_rate)
        basis = float(basis)
        won = basis * exchange_rate
        won = '{:,.2f}'.format(won)
        basis = '{:,.2f}'.format(basis)
        print('%s %s = %s KRW' %(basis, self.currency, won))
        # foreign : KRW for the given
        won_amount = self.amount * exchange_rate
        foreign_amount = self.amount
        won_amount = '{:,.2f}'.format(won_amount)
        foreign_amount = '{:,.2f}'.format(foreign_amount)
        print('%s %s = %s KRW' %(foreign_amount, self.currency, won_amount))
        # KRW : foreign for the given
        won_amount = self.amount
        foreign_amount = self.amount / exchange_rate
        won_amount = '{:,.2f}'.format(won_amount)
        foreign_amount = '{:,.2f}'.format(foreign_amount)
        print('%s KRW = %s %s' %(won_amount, foreign_amount, self.currency))

if __name__ == '__main__':
    exrate = ExchangeRate()
    exrate.parse_args()
    if exrate.list_bool:
        exrate.show_currencies()
    else:
        exrate.calcurate()
