import math
import argparse

class ColorModel(object):

    def __init__(self, color=None):
        self.color = color

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description='Convert between RGB and CMYK.'
        )
        parser.add_argument(
            'color',
            nargs='+',
            help='Specify one or more RGB or CMYK values.'
        )
        args = parser.parse_args()
        self.color = args.color   
        for i in args.color:    
            self.identify_color_model(i)     

    def error_message(self):
        print('The value is formatted wrong.')        

    def identify_color_model(self, color: str):   
        color = color.replace(' ', '')
        if color.count(',') >= 3:
            C, M, Y, K = self.parse_CMYK(color)
            if C is False:
                self.error_message()
            else:
                # check if between 0 and 1
                if not all(map(lambda x: x >= 0. and x <= 1., [C, M, Y, K])):
                    self.error_message()
                else:
                    self.CMYK_to_RGB(color, C, M, Y, K)
        else:
            R, G, B = self.parse_RGB(color)
            if R is False:
                self.error_message()
            else:
                # check if between 0 and 255
                if not all(map(lambda x: x in range(256), [R, G, B])):
                    self.error_message()
                else:
                    self.RGB_to_CMYK(color, R, G, B)

    def parse_CMYK(self, color: str):        
        color = color.split(',')
        if len(color) == 4:            
            try:
                C = float(color[0])
                M = float(color[1])
                Y = float(color[2])
                K = float(color[3])                
            except:
                C, M, Y, K = False, False, False, False
        else:
            C, M, Y, K = False, False, False, False

        return C, M, Y, K


    def parse_RGB(self, color: str):
        if color.count(',') == 0:        
            if len(color) == 6:
                try:
                    R = int(color[0:2], 16)
                    G = int(color[2:4], 16)
                    B = int(color[4:6], 16)
                except:
                    R, G, B = False, False, False

        if color.count(',') == 2: 
            color = color.split(',')
            try:
                R = int(color[0])
                G = int(color[1])
                B = int(color[2])
            except:
                R, G, B = False, False, False
            
        return R, G, B

    def RGB_to_CMYK(self, color, R, G, B):       
        R = R/255
        G = G/255
        B = B/255
        K = 1 - max(R, G, B)
        C = (1 - R - K) / (1 - K)
        M = (1 - G - K) / (1 - K)
        Y = (1 - B - K) / (1 - K)
        color = color.replace(',', ', ')
        CMYK = '{} = {:1.2f}, {:1.2f}, {:1.2f}, {:1.2f}'.format(color, C, M, Y, K)
        print(CMYK)

    def CMYK_to_RGB(self, color, C, M, Y, K):
        R = 255 * (1 - C) * (1 - K) 
        G = 255 * (1 - M) * (1 - K)
        B = 255 * (1 - Y) * (1 - K)
        color = color.replace(',', ', ')
        RGB = '{} = {:3.0f}, {:3.0f}, {:3.0f}'.format(color, R, G, B)
        print(RGB)

if __name__ == '__main__':
    CM = ColorModel()
    CM.parse_args()
    