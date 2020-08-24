import argparse
from datetime import datetime, date, timedelta
import calendar
calendar.setfirstweekday(calendar.SUNDAY)

class DateCalculator(object):

    def __init__(self, daydate=None, basis=None, week=False, weekday=False, calendar=False):

        self.daydate = daydate
        self.basis = basis
        self.week_bool = week
        self.weekday_bool = weekday
        self.calendar_bool = calendar

        self.weekdays = { 
            0:'Monday',
            1:'Tuesday',
            2:'Wednesday',
            3:'Thursday',
            4:'Friday',
            5:'Saturday',
            6:'Sunday'
        }

    def parse_args(self):

        example = '''examples:
    datecal.py -20 -10 10 20
        This shows dates 20 and 10 days before and after today.
    datecal.py -b 2010-07-07 10
        These show the date 10 days after 2010-07-07.
    datecal.py -w 10
        This shows the date 10 weeks after today.
    datecal.py 2021-01-01
        This shows the number of days between tody and 2021-01-01.
    datecal.py -W 2021-01-01
        This shows the day of week on 2021-01-01.
    datecal.py -c 2021-01
        This displays a monthly calendar for January 2021.
    datecal.py -c 2021
        This displays a yearly calendar for 2021.
    ''' 

        parser = argparse.ArgumentParser(
            epilog = example,
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = 'Find out the date certain days before or after a given date.'
        )

        parser.add_argument(
            'daydate',
            nargs = '+',
            help = 'Specify one or more days or dates.'
        )
        parser.add_argument(
            '-b',
            dest = 'basis',
            default = None,
            help = 'Specify a date in the yyyy-mm-dd format.'
        )
        parser.add_argument(
            '-w',
            dest = 'week',
            action = 'store_true',
            default = False,
            help = 'Use week as the unit of time.'
        )
        parser.add_argument(
            '-W',
            dest = 'weekday',
            action = 'store_true',
            default = False,
            help = 'Find days of week.'
        )
        parser.add_argument(
            '-c',
            dest = 'calendar',
            action = 'store_true',
            default = False,
            help = 'Display calendars.'
        )
       
        args = parser.parse_args()

        self.daydate = args.daydate
        self.basis = self.validate(args.basis)
        self.week_bool = args.week
        self.weekday_bool = args.weekday
        self.calendar_bool = args.calendar


    def validate(self, basis:str):

        if basis is None:
            return date.today()

        try:
            basis = datetime.strptime(basis, '%Y-%m-%d')
        except:
            try: 
                basis = datetime.strptime(basis, '%Y-%m')
            except: 
                print('This date is wrong so today is used as the basis.')
                basis = date.today()

        return basis


    def days_or_date(self, daydate):

        try:
            daydate = int(daydate)
            return daydate
        except:
            daydate = self.validate(daydate)
            return daydate


    def print_date(self, days: int):

        if self.week_bool:
            days = days * 7
        diff = timedelta(days = days)  
        result = self.basis + diff
        output = '{}: {} days from {}'.format(result.strftime('%Y-%m-%d'), days, self.basis.strftime('%Y-%m-%d'))
        print(output)


    def print_days(self, target_date):

        date1 = self.basis.strftime('%Y-%m-%d')
        date2 = target_date.strftime('%Y-%m-%d')
        result = datetime.strptime(date1, '%Y-%m-%d') - \
            datetime.strptime(date2, '%Y-%m-%d')
        output = '{} days between {} and {}'.format(abs(result.days), date1, date2)
        print(output)


    def print_weekday(self, target_date):

        weekday = self.weekdays[target_date.weekday()]
        output = '{} on {}'.format(weekday, target_date.strftime('%Y-%m-%d'))
        print(output)        


    def print_calendar(self, target_date):

        if type(target_date) is int:
            print(calendar.calendar(target_date))
        else:
            print(calendar.month(target_date.year, target_date.month))

    def calculate(self):

        for i in self.daydate:
            daydate = self.days_or_date(i)
            if type(daydate) is int:
                if self.calendar_bool:
                    self.print_calendar(daydate)
                else:
                    self.print_date(daydate)
            else:
                if self.weekday_bool:
                    self.print_weekday(daydate)
                elif self.calendar_bool:
                    self.print_calendar(daydate)
                else:
                    self.print_days(daydate)


if __name__ == '__main__':
    datecal = DateCalculator()
    datecal.parse_args()
    datecal.calculate()