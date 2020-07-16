import argparse
from datetime import datetime, date, timedelta

class DateCalculator(object):

    def __init__(self, difference=None, basis=None, week=False):

        self.difference = difference
        self.basis = self.validate(basis)
        self.week_bool = week
    
    def parse_args(self):

        example = '''examples:
    datecal.py -20 -10 10 20
        This shows dates 20 and 10 days before and after today.
    datecal.py -b 2010-07-07 10
    datecal.py -b 2010-7-7 10
    datecal.py -b 2010.07.07 10
    datecal.py -b 2010.7.7 10
        These show the date 10 days after 2010-07-07.
    datecal.py -w 10
        This shows the date 10 weeks after today.
    datecal.py 2022-01-01
        This shows the number of days between today and 2020-01-01
    ''' 

        parser = argparse.ArgumentParser(
            epilog = example,
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = 'Find out the date certain days before or after a given date.'
        )

        parser.add_argument(
            'difference',
            nargs = '+',
            help = 'Specify a time difference. Unless specified otherwise, the unit is day.'
        )
        parser.add_argument(
            '-w',
            dest = 'week',
            action = 'store_true',
            default = False,
            help = 'Use week as the unit of time.'
        )
        parser.add_argument(
            '-b',
            dest = 'basis',
            default = None,
            help = 'Specify a date in the yyyy-mm-dd format.'
        )
        args = parser.parse_args()

        self.difference = args.difference
        self.week_bool = args.week
        self.basis = self.validate(args.basis)        

    def validate(self, basis:str):

        if basis is None:
            return date.today()

        try:
            basis = datetime.strptime(basis, '%Y-%m-%d')
        except:
            try: 
                basis = datetime.strptime(basis, '%Y.%m.%d')
            except:                
                print('This date is wrong so today is used as the basis.')
                basis = date.today()

        return basis

    def days_or_date(self, daydate):

        try:
            days = int(daydate)
            self.print_date(days)
        except:
            self.print_days(daydate)
            
    def print_days(self, target_date):

        target_date = self.validate(target_date)
        date1 = self.basis.strftime('%Y-%m-%d')
        date2 = target_date.strftime('%Y-%m-%d')
        result = datetime.strptime(date1, '%Y-%m-%d') - \
            datetime.strptime(date2, '%Y-%m-%d')
        output = '{} days between {} and {}'.format(abs(result.days), date1, date2)
        print(output)
        
    def print_date(self, days: int):

        if self.week_bool:
            days = days * 7
        diff = timedelta(days = days)  
        result = self.basis + diff
        output = '{} days from {}: {}'.format(days, self.basis.strftime('%Y-%m-%d'), result.strftime('%Y-%m-%d'))
        print(output)

    def calculate(self): 
        for i in self.difference:
            self.days_or_date(i)            
        
if __name__ == '__main__':
    datecal = DateCalculator()
    datecal.parse_args()
    datecal.calculate()
    # import datetime
    # from datetime import timedelta
 
    # datetimeFormat = '%Y-%m-%d'
    # date1 = '2016-04-16'
    # date2 = '2016-03-10'
    # diff = datetime.datetime.strptime(date1, datetimeFormat)\
    #     - datetime.datetime.strptime(date2, datetimeFormat)
    
    # print("Difference:", diff)
    # print("Days:", diff.days)
    # print("Microseconds:", diff.microseconds)
    # print("Seconds:", diff.seconds)