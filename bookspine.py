import argparse

class BookSpineWidth(object):
    def __init__(self, pages=0, type='vellum', weight=120, margin=1):
        self.papers = {
            'vellum':{70:0.08, 80:0.09, 95:0.115, 100:0.12, 120:0.14, 150:0.17, 180:0.2, 220:0.24},
            'art':{80:0.06, 100:0.08, 120:0.095, 150:0.12, 180:0.15, 200:0.17, 250:0.22, 300:0.27},
            'snow': {80:0.07, 100:0.09, 120:0.105, 150:0.14, 180:0.18, 200:0.19, 250:0.26},
            'mat':{70:0.07, 80:0.08, 90:0.095, 100:0.11},
            'elight':{70:0.11, 80:0.13},
            'arte':{105:0.155, 130:0.19, 160:0.23, 190:0.27, 210:0.3, 230:0.32},
            'rendezvous':{90:0.13, 105:0.14, 130:0.17, 160:0.22, 190:0.25, 210:0.29, 240:0.33},
            'montblanc':{90:0.12, 100:0.13, 130:0.18, 160:0.23, 190:0.26, 210:0.29, 240:0.32}
        }
        self.paper_types = {
            'vellum':'Vellum', 
            'art':'Art', 
            'snow':'Snow', 
            'mat':'M-Mat', 
            'elight':'E-Light', 
            'arte':'Arte', 
            'rendezvous':'Rendezvous', 
            'montblanc':'Mont Blanc'
        }
        self.pages = pages
        self.paper_type = type
        self.paper_weight = weight
        self.margin = margin
        self.list_bool = False

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Get the spine width for a book.'
        )
        parser.add_argument(
            'pages',
            nargs = 1,
            type = int,
            help = 'Specify a page count'
        )
        parser.add_argument(
            '-t',
            dest = 'paper_type',
            help = 'specify a paper type. The default is vellum'
        )
        parser.add_argument(
            '-w',
            dest = 'paper_weight', 
            type = int,   
            help = 'Specify the paper weight. The default is 120.'
        )
        parser.add_argument(
            '-m',
            dest = 'margin',
            type = int,
            help = 'Specify the margin for binding. The default is 1 (mm).'
        )
        parser.add_argument(
            '-l',
            dest = 'list',
            action = 'store_true',
            default = False,
            help = 'Display paper details.'
        )
        args = parser.parse_args()
        self.pages = args.pages[0]
        if args.paper_type is not None:
            self.paper_type = args.paper_type
        if args.paper_weight is not None:
            self.paper_weight = args.paper_weight
        if args.margin is not None:
            self.margin = args.margin
        self.list_bool = args.list

    def show_papers(self):
        for paper in self.paper_types:
            print('\n%s:' %(self.paper_types[paper]))
            paper_feature = self.papers[paper]
            for weight in paper_feature:
                print('%3d g \t %s mm' %(weight, paper_feature[weight]))
            answer = input('\nPress Enter to continue or Q to quit.')
            if answer.lower() == 'q':
                return

    def calculate(self): 
        try:
            name = self.paper_types[self.paper_type]
            width = self.papers[self.paper_type][self.paper_weight]
            msg = '\nWith %d g %s paper of which width is %0.3f mm, %d pages make the spine:' %(self.paper_weight, name, width, self.pages)
            print(msg)
            spine = (self.pages / 2 * width) + self.margin    
            msg = '%0.2f mm with a margin of %d mm from the paper width' %(spine, self.margin)
            print(msg)
        except:
            print('\nNo corresponding width data is found.')
        spine = (self.paper_weight * self.pages * 0.6 / 1000) + self.margin
        msg = '%0.2f mm with a margin of %d mm from the paper weight\n' %(spine, self.margin)
        print(msg)

if __name__ == '__main__':
    spine = BookSpineWidth()
    spine.parse_args()
    if spine.list_bool:
        spine.show_papers()
    else:
        spine.calculate()
