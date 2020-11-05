import argparse
from datetime import datetime, date, timedelta
import calendar
import pytz
from dateutil.relativedelta import relativedelta

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

        self.timezones = {
            'London':'Europe/London',
            'Los Angeles':'America/Los_Angeles',
            'New York':'America/New_York',
            'Paris':'Europe/Paris',
            'Rome':'Europe/Rome',
            'Seoul':'Asia/Seoul',
            'Sydney':'Australia/Sydney',
            'Toronto':'America/Toronto'
        }

    def parse_args(self):

        example = '''examples:
    datecal.py -20 -10 10 20
        shows dates 20 and 10 days before and after today.
    datecal.py -b 2010-07-07 10
        These show the date 10 days after 2010-07-07.
    datecal.py -w 10
        shows the date 10 weeks after today.
    datecal.py 2021-01-01
        shows the number of days between tody and 2021-01-01.
    datecal.py -W 2021-01-01
        shows the day of week on 2021-01-01.
    datecal.py -c 2021-01
        displays a monthly calendar for January 2021.
    datecal.py -c 2021
        displays a yearly calendar for 2021.
    datecal.py -z Toronto
        shows Toronto's current local time.
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
        parser.add_argument(
            '-z',
            dest = 'timezone',
            action = 'store_true',
            default = False,
            help = "Display a given city's current local time."
        )
       
        args = parser.parse_args()

        self.daydate = args.daydate
        self.basis = self.validate(args.basis)
        self.week_bool = args.week
        self.weekday_bool = args.weekday
        self.calendar_bool = args.calendar
        self.timezone_bool = args.timezone

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


    def print_local_time(self):

        # for i in pytz.all_timezones:
        #     print(i)

        utcnow = pytz.timezone('utc').localize(datetime.utcnow())        
        here_time = utcnow.astimezone(pytz.timezone('Asia/Seoul')).replace(tzinfo=None)

        for city in self.daydate:
            city = ' '.join([word.capitalize() for word in city.split(" ")])
            try:
                city_timezone = self.timezones[city]
                there_time = utcnow.astimezone(pytz.timezone(city_timezone)).replace(tzinfo=None)
                offset = relativedelta(there_time, here_time) 
                output = 'The current local time at {} is {}, {} hours from Seoul.'.format(city, there_time.strftime('%H:%M on %Y-%m-%d'), offset.hours)
            except:
                output = '{} is not in the list of time zones.'.format(city)
            print(output)

        # for city in self.timezones:
        #     city_timezone = self.timezones[city]
        #     there_time = utcnow.astimezone(pytz.timezone(city_timezone)).replace(tzinfo=None)
        #     offset = relativedelta(there_time, here_time) 
        #     output = 'The current local time at {} is {}, {} hours from Seoul.'.format(city, there_time.strftime('%H:%M on %Y-%m-%d'), offset.hours)
        #     print(output)


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


    def determine_task(self):

        if self.timezone_bool:
            self.print_local_time()
        else:
            self.calculate()


if __name__ == '__main__':
    datecal = DateCalculator()
    datecal.parse_args()
    datecal.determine_task()