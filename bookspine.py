import argparse

parser = argparse.ArgumentParser(
    description = 'Get the spine width for a book.'
)
parser.add_argument(
    'pages',
    nargs = '?',
    type = int,
    help = 'Specify the number of pages.'
)
parser.add_argument(
    '-t',
    dest = 'paper_type',
    type = int,
    default = 0,
    help = 'Choose a paper type. The default is 0.'
)
parser.add_argument(
    '-w',
    dest = 'paper_weight',    
    type = int,
    default = 120,
    help = 'Specify the paper weight. The default is 120.'
)
parser.add_argument(
    '-m',
    dest = 'margin',
    type = int,
    default = 1,
    help = 'Specify the margin for binding. The default is 1 (mm).'
)
parser.add_argument(
    '-l',
    dest = 'list',
    action = 'store_true',
    default = False,
    help = 'Display the details of a paper type. To view every type, set a larger number than the count to the -t option, such as 10.'
)
args = parser.parse_args()

vellum = {70:0.08, 80:0.09, 95:0.115, 100:0.12, 120:0.14, 150:0.17, 180:0.2, 220:0.24}
art = {80:0.06, 100:0.08, 120:0.095, 150:0.12, 180:0.15, 200:0.17, 250:0.22, 300:0.27}
snow = {80:0.07, 100:0.09, 120:0.105, 150:0.14, 180:0.18, 200:0.19, 250:0.26}
mat = {70:0.07, 80:0.08, 90:0.095, 100:0.11}
elight = {70:0.11, 80:0.13}
arte = {105:0.155, 130:0.19, 160:0.23, 190:0.27, 210:0.3, 230:0.32}
rendezvous = {90:0.13, 105:0.14, 130:0.17, 160:0.22, 190:0.25, 210:0.29, 240:0.33}
montblanc = {90:0.12, 100:0.13, 130:0.18, 160:0.23, 190:0.26, 210:0.29, 240:0.32}
paper_types = [vellum, art, snow, mat, elight, arte, rendezvous, montblanc]
paper_names = ["Vellum", "Art", "Snow", "M-Mat", "E-Light", "Arte", "Rendezvous", "Mont Blanc"]

def paper_list_show():
    if args.paper_type > len(paper_types):
        cnt = 0
        for i in paper_types:
            print("\n%s" %(paper_names[cnt]))
            cnt += 1
            for j in i:
                print("%3d g \t %s mm" %(j, i[j]))
    else:
        print(paper_names[args.paper_type])
        for i in paper_types[args.paper_type]:
            print("%3d g \t %s mm" %(i, paper_types[args.paper_type].get(i)))

if args.list:
    paper_list_show()        
else:    
    if args.pages is None:
        parser.print_help()
        cnt = 0
        for i in paper_names:
            cnt += 1
            print("   %d:%s" %(cnt, i))
    else: 
        paper_thickness = paper_types[args.paper_type].get(args.paper_weight)
        print("%d pages with %d g %s of which thickness is %0.2f mm" %(args.pages,  args.paper_weight, paper_names[args.paper_type], paper_thickness))    
        A = args.pages / 2 * paper_thickness + args.margin    
        B = args.paper_weight * args.pages * 0.6 / 1000 + args.margin
        print("%0.2f mm from the paper thickness\n%0.2f mm from the paper weight" %(A, B))
