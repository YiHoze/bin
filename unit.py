import argparse

class ConvertUnit(object):
    # def __init__(self):

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Convert a unit to another.'
        )
        parser.add_argument(
            'numeral',
            help = 'Enter a numeric value.'
        )
        parser.add_argument(
            '-t',
            dest = 'temperature',
            action = 'store_true',
            default = False,
            help = 'Celcius / Fahrenheit'
        )
        parser.add_argument(
            '-m',
            dest = 'mile',
            action = 'store_true',
            default = False,
            help = 'mile / kilometer'
        )
        parser.add_argument(
            '-y',
            dest = 'yard',
            action = 'store_true',
            default = False,
            help = 'yard / meter'
        )
        parser.add_argument(
            '-f',
            dest = 'foot',
            action = 'store_true',
            default = False,
            help = 'foot / meter'
        )
        parser.add_argument(
            '-i',
            dest = 'inch',
            action = 'store_true',
            default = False,
            help = 'inch / millimeter'
        )
        parser.add_argument(
            '-pt',
            dest = 'point',
            action = 'store_true',
            default = False,
            help = 'point / millimeter'
        )
        parser.add_argument(
            '-p',
            dest = 'pound',
            action = 'store_true',
            default = False,
            help = 'pound / kilogram'
        )
        parser.add_argument(
            '-py',
            dest = 'pyeong',
            action = 'store_true',
            default = False,
            help = 'pyeong / square meter'
        )
        parser.add_argument(
            '-a',
            dest = 'acre',
            action = 'store_true',
            default = False,
            help = 'acre / square meter'
        )
        self.args = parser.parse_args()

    def celsius_fahrenheit(self, temperature): 
        fahrenheit = float(temperature)
        celsius = (fahrenheit - 32) * 5 / 9
        print('\n%3.2f Fahrenheit = %3.2f Celsius' %(fahrenheit, celsius))
        celsius = float(temperature)
        fahrenheit = celsius * 9 / 5 + 32
        print('%3.2f Celsius = %3.2f Fahrenheit\n' %(celsius, fahrenheit))

    def kilometer_mile(self, distance): 
        mile = float(distance)
        kilometer = mile * 1.60934
        print('\n%3.2f miles = %3.2f kilometers' %(mile, kilometer))
        kilometer = float(distance)
        mile = kilometer * 0.621371
        print('%3.2f kilometers = %3.2f miles\n' %(kilometer, mile))

    def meter_yard(self, distance): 
        yard = float(distance)
        meter = yard * 0.9144
        print('\n%3.2f yards = %3.2f meters' %(yard, meter))
        meter = float(distance)
        yard = meter * 1.09361
        print('%3.2f meters = %3.2f yards\n' %(meter, yard))

    def meter_foot(self, distance): 
        foot = float(distance)
        meter = foot * 0.3048
        print('\n%3.2f feet = %3.2f meters' %(foot, meter))
        meter = float(distance)
        foot = meter * 3.28084
        print('%3.2f meters = %3.2f feet\n' %(meter, foot))

    def millimeter_inch(self, distance): 
        inch = float(distance)
        millimeter = inch * 25.4
        centimeter = millimeter / 10
        print('\n%3.2f inches = %3.2f millmeters (%3.2f centimeters)' %(inch, millimeter, centimeter))
        millimeter = float(distance)
        centimeter = millimeter / 10
        inch = millimeter * 0.0393701
        print('%3.2f millimeters (%3.2f centimeters) = %3.2f inches\n' %(millimeter, centimeter, inch))

    def millimeter_point(self, distance): 
        point = float(distance)
        millimeter = point * 0.352778
        print('\n%3.2f points = %3.2f millmeters' %(point, millimeter))
        millimeter = float(distance)
        point = millimeter * 2.83465
        print('%3.2f millimeters = %3.2f points\n' %(millimeter, point))

    def kilogram_pound(self, mass): 
        pound = float(mass)
        kilogram = pound * 0.453592
        print('\n%3.2f pounds = %3.2f kilograms' %(pound, kilogram))
        kilogram = float(mass)
        pound = kilogram * 2.20462
        print('%3.2f kilograms = %3.2f pounds\n' %(kilogram, pound))

    def square_meter_pyeong(self, area): 
        pyeong = float(area)
        squaremeter = pyeong * 3.30579
        print('\n%3.2f pyeongs = %3.2f square meters' %(pyeong, squaremeter))
        squaremeter = float(area)
        pyeong = squaremeter * 0.3025
        print('%3.2f square meters = %3.2f pyeongs\n' %(squaremeter, pyeong))

    def square_meter_acre(self, area): 
        acre = float(area)
        squaremeter = acre * 4046.86
        print('\n%3.2f acres = %3.2f square meters' %(acre, squaremeter))
        squaremeter = float(area)
        acre = squaremeter * 0.000247105
        print('%3.2f square meters = %3.2f acres\n' %(squaremeter, acre))

    def determine_unit_type(self):
        if self.args.temperature: 
            self.celsius_fahrenheit(self.args.numeral)
        elif self.args.mile: 
            self.kilometer_mile(self.args.numeral)
        elif self.args.yard: 
            self.meter_yard(self.args.numeral)
        elif self.args.foot: 
            self.meter_foot(self.args.numeral)
        elif self.args.inch: 
            self.millimeter_inch(self.args.numeral)
        elif self.args.point: 
            self.millimeter_point(self.args.numeral)
        elif self.args.pound: 
            self.kilogram_pound(self.args.numeral)
        elif self.args.pyeong: 
            self.square_meter_pyeong(self.args.numeral)
        elif self.args.acre: 
            self.square_meter_acre(self.args.numeral)

if __name__ == '__main__':
    unit = ConvertUnit()
    unit.parse_args()
    unit.determine_unit_type()