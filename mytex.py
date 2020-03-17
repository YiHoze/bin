import os, sys, glob, argparse, subprocess

try:
    dirCalled = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    dirCalled = False
if dirCalled is False:
    dirCalled = os.path.dirname(sys.argv[0])

parser = argparse.ArgumentParser(
    description = 'Create a LaTeX file for one of the following purposes.'
)
parser.add_argument(
    'output',
    type = str,
    nargs = '?',
    help = 'Specify a filename for output.'
)
parser.add_argument(
    '-cls',
    dest = 'tex_class',
    default = 'hzguide',
    help = 'Choose one among article, hzbeamer, hzguide, memoir, oblivoir. (default: hzguide)'
)
parser.add_argument(
    '-f',
    dest = 'font_glyph',
    action = 'store_true',
    help = "Create one to view a font's glyphs."
)
parser.add_argument(
    '-m',
    dest = 'merge',
    action = 'store_true',
    default = False,
    help = 'Create one to merge PDF files of different sizes.'
)
parser.add_argument(
    '-c',
    dest = 'circled_number',
    action = 'store_true',
    default = False,
    help = 'Create separate PDF files of circled numbers.'
)
parser.add_argument(
    '-tpl',
    dest = 'template',
    action = 'store_true',
    default = False,
    help = 'Create the manual template.' 
)
parser.add_argument(
    '-alb',
    dest = 'album',
    action = 'store_true',
    default = False,
    help = 'Create an album with all the image files in the current directory.'
)
parser.add_argument(
    '-s',
    dest = 'scale',
    default = '1',
    help = 'Image scale (default: 1)'
)
parser.add_argument(
    '-hid',
    dest = 'hide_image_name',
    action = 'store_true',
    default = False,
    help = "Leave out images' filenames when creating an album."
)
parser.add_argument(
    '-1',
    dest = 'one_column',
    action = 'store_true',
    default = False,
    help = 'Make the album\'s layout to be one column. (default: two columns)'
)
parser.add_argument(
    '-n',
    dest = 'no_compile',
    action = 'store_true',
    default = False,
    help = 'Do not compile for album or template'
)
parser.add_argument(
    '-k',
    dest = 'keep',
    action = 'store_true',
    default = False,
    help = 'Keep collateral files when creating an album.'
)

args = parser.parse_args()

def check_to_remove(afile):
    if os.path.exists(afile):
        answer = input('%s alread exists. Are you sure to overwrite it? [y/N] ' %(afile))
        if answer.lower() == 'y':
            os.remove(afile)
            return True
        else:
            return False
    else:
        return True

def tex_article():
    content = """
        \\documentclass[a4paper]{article}
        \\usepackage{fontspec}\n
        \\begin{document}\n
        \\end{document}"""
    return(content)

def tex_hzbeamer():
    content = """
        \\documentclass[10pt,flier=false,hangul=true]{hzbeamer}
        \\usepackage{csquotes}
        \\MakeOuterQuote{\"}
        \\title{}
        \\author{}
        \\institute{}
        \\date{}\n
        \\begin{document}    
        \\begin{frame}[fragile, allowframebreaks=1]{}\n
        \\end{frame}
        \\end{document}"""
    return(content)

def tex_hzguide():
    content = """
        \\documentclass{hzguide}
        \\LayoutSetup{}\n
        \\begin{document}\n
        \\end{document}"""
    return(content)

def tex_memoir():
    content = """
        \\documentclass[a4paper]{memoir} 
        \\usepackage{fontspec}\n
        \\begin{document}\n
        \\end{document}"""
    return(content)

def tex_oblivoir():
    content = """
        \\documentclass{oblivoir} 
        \\usepackage{fapapersize}
        \\usefapapersize{*,*,30mm,*,30mm,*}\n
        \\begin{document}\n
        \\end{document}"""
    return(content)

def create_tex():
    if check_to_remove(tex) is False:
        return
    if args.tex_class == 'article':
        content = tex_article()
    elif args.tex_class == 'hzbeamer':
        content = tex_hzbeamer()
    elif args.tex_class == 'hzguide':
        content = tex_hzguide()
    elif args.tex_class == 'memoir':
        content = tex_memoir()
    elif args.tex_class == 'oblivoir':
        content = tex_oblivoir()
    else:
        content = tex_hzguide()
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)
    processor = os.path.join(dirCalled, 'open.py')    
    subprocess.call(['python', processor, tex])

def create_font_glyph():
    if check_to_remove(tex) is False:
        return
    content = r"""
        \documentclass[12pt]{article}
        \usepackage{fontspec}
        \usepackage{xparse}
        \ExplSyntaxOn
        \int_new:N \l_glyph_number
        \tl_new:N \l_glyph_code 
        \int_new:N \l_glyph_slot
        \NewDocumentCommand \ShowGlyphs { mm } 
        {
            \group_begin:			
            \int_set:Nn \l_tmpa_int { \int_from_hex:n {#1} }
            \int_set:Nn \l_glyph_number { \int_from_hex:n {#2} }
                \linespread{1.25}		
                \int_do_while:nn {	\l_tmpa_int < \l_glyph_number } 
                {
                    \int_incr:N \l_tmpa_int		
                    \tl_set:Nn \l_glyph_code { \int_to_Hex:n {\l_tmpa_int} }
                    \int_set:Nn \l_glyph_slot {\the\XeTeXcharglyph"\l_glyph_code} 
                    \int_compare:nT { \l_glyph_slot != 0 }
                    {
                        \parbox{1.5em}{
                            \centering 			
                            \raisebox{-1ex}{ \tiny \int_use:N \l_glyph_slot} \\
                            \char"\l_glyph_code \\
                            \raisebox{1ex}{ \tiny \l_glyph_code }
                        }
                    }
                    \int_set:Nn \l_tmpb_int {\int_mod:nn {\l_tmpa_int} {16} }
                    \int_compare:nT { \l_tmpb_int = 0 }
                        { \newline }
                        { \hskip .25em }
                }	
            \group_end:
            \par
        }
        \ExplSyntaxOff
        \setlength\parindent{0pt}
        \begin{document} 
        \setmainfont{Noto Serif CJK KR}
        \ShowGlyphs{1100}{11FF}
        \ShowGlyphs{A960}{A97C}
        \ShowGlyphs{D7B0}{D7FB}
        \end{document}"""
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)    
    processor = os.path.join(dirCalled, 'open.py')    
    subprocess.call(['python', processor, tex])

def create_template():
    if check_to_remove(tex) is False:
        return    
    content = r"""
        \documentclass[10pt, openany]{hzguide}
        \LayoutSetup{}
        \HeadingSetup{chapterstyle=tandh}
        \setsecnumdepth{chapter}
        \SectionNewpageOn
        \DecolorHyperlinks
        \CoverSetup{    
            FrontLogoImage = {alertsymbol},
            BackLogoImage = {alertsymbol},
            ProductImage = {uncertain},
            title = {Product X},
            DocumentType = {User Guide},
            PubYear = 2018,
            revision = {Rev. 1},
            note = {Keep this manual for later use.},
            manufacturer = Manufacturer,
            address = Seoul
        }
        \begin{document} 
        \frontmatter* 
        \FrontCover
        \tableofcontents
        \mainmatter*
        \chapter{Introduction}\tplpara
        \section{Features}\tpllist
        \section{Package Items}\tplimagetable
        \section{Specifications}\tplspectables
        \chapter{Safety}
        \section{General Precautions}\tpllist[itemize][itemize]
        \section{Tools}\tplimagetable
        \section{Safety Gear}\tplimagetable
        \chapter{Installation}
        \section{Installation Requirements}\tpllist
        \section{Installing X}\tplprocedure[5]
        \section{Checking X}\tplprocedure
        \section{Starting X}\tpllist*
        \chapter{Operation}\tplactions
        \chapter{Troubleshooting}\listofproblems*\tplproblems
        \chapter{Maintenance}
        \section{Precautions for Maintenance}\tpllist
        \section{Scheduled Inspection}\tpllist
        \chapter{Warranty}
        \section{Warranty Coverage}\tplpara*
        \section{Limitation of Liability}\tplpara*\tpllist
        \section{Contact Information}\tplpara*
        \appendix
        \chapter{Technical Information}\tplspectables
        \chapter{Glossary}\tpllist[terms]
        \BackCover
        \end{document}"""
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)
    processor = os.path.join(dirCalled, 'open.py')    
    subprocess.call(['python', processor, tex])
    if not args.no_compile:        
        processor = os.path.join(dirCalled, 'ltx.py')    
        subprocess.call(['python', processor, '-b', '-w', tex])          
        processor = os.path.join(dirCalled, 'open.py')    
        subprocess.call(['python', processor, pdf])

def create_album():
    if check_to_remove(pdf) is False:
        return    
    # Make a file the contains a list of image files
    image_list = []
    image_type = ['pdf', 'jpg', 'jpeg', 'png']
    list_file = 't@mp.t@mp'
    for i in range(len(image_type)):
        fnpattern = '*.' + image_type[i]
        for afile in glob.glob(fnpattern):
            image_list.append(afile)
    image_list.sort()
    image_list = '\n'.join(map(str,image_list))
    with open(list_file, mode='w') as f:
        f.write(image_list)
    # Make a tex file with this content
    if args.one_column:
        content = """
        \\documentclass{hzguide}
        \\LayoutSetup{ulmargin=15mm, lrmargin=15mm}
        \\HeadingSetup{type=report}
        \\begin{document}
        \\MakeAlbum[%s]{%s}
        \\end{document}""" %(args.scale, list_file)
    else:
        content = """
        \\documentclass{hzguide}
        \\usepackage{multicol}
        \\LayoutSetup{ulmargin=15mm, lrmargin=15mm}
        \\HeadingSetup{type=report}
        \\begin{document}
        \\begin{multicols}{2}
        \\MakeAlbum[%s]{%s}
        \\end{multicols}
        \\end{document}""" %(args.scale, list_file)
    if args.hide_image_name:
        content = content.replace('MakeAlbum', 'MakeAlbum*')
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)
    if not args.no_compile:        
        processor = os.path.join(dirCalled, 'ltx.py')    
        subprocess.call(['python', processor, '-b', '-c', tex])          
        processor = os.path.join(dirCalled, 'open.py')    
        subprocess.call(['python', processor, pdf])
    if not args.keep:
        os.remove(list_file)
        os.remove(tex)

def merge_pdf():
    if check_to_remove(tex) is False:
        return
    content = r"""
        \documentclass{minimal}
        \usepackage[a4paper]{geometry}
        \usepackage{graphicx}
        \usepackage{xparse}
        \geometry{paperwidth=216mm, paperheight=303mm, margin={0pt, 0pt}}
        \ExplSyntaxOn
        \sys_if_engine_pdftex:T
        {
            \pdfminorversion=6
        }
        \NewDocumentCommand \mergepdf { m }
        {
            \bool_gset_false:N \g_tmpa_bool % Not to break the last page
            \clist_set:Nn \l_tmpa_clist { #1 }    
            \int_set:Nn \l_tmpa_int { \clist_count:N \l_tmpa_clist }
            \int_step_inline:nn { \l_tmpa_int }
            {
                \clist_pop:NN \l_tmpa_clist \l_tmpa_tl
                \int_compare:nT { ##1 == \l_tmpa_int }
                {
                    \bool_gset_true:N \g_tmpa_bool
                }
                \fetchpage{ \l_tmpa_tl }
            }

        }
        \int_new:N \g_lastximage_int
        \NewDocumentCommand \lastpageofpdf { m }
        {
            \get_last_page_of_pdf:nN { #1 } \g_lastximage_int
        }

        \cs_new_nopar:Npn \get_last_page_of_pdf:nN #1 #2
        {
            \str_case_e:nn { \c_sys_engine_str }
            {
                { xetex } {
                    \int_gset:Nn #2 {
                        \xetex_pdfpagecount:D "#1"
                    }
                }
                { pdftex } {
                    \pdfximage{#1}
                    \int_gset:Nn #2 {
                        \pdflastximagepages
                    }
                }
                { luatex } {
                    \saveimageresource { #1 }
                    \int_gset:Nn #2 {
                        \lastsavedimageresourcepages
                    }
                }
            }
        }
        \NewDocumentCommand \fetchpage { m }
        {    
            \lastpageofpdf{#1.pdf}
            \int_step_inline:nn { \g_lastximage_int }    
            {        
                \includegraphics[width=\paperwidth, page=##1]{#1}
                \bool_if:NTF \g_tmpa_bool 
                {
                    \int_compare:nT { ##1 < \g_lastximage_int }
                    {
                        \break
                    }            
                }{
                    \break
                }        
            }
        }
        \ExplSyntaxOff
        \begin{document}
        \mergepdf{A, B, C}
        \end{document}"""
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)
    processor = os.path.join(dirCalled, 'open.py')    
    subprocess.call(['python', processor, tex])

def create_circled_numbers():
    if check_to_remove(tex) is False:
        return
    content = r"""
        \documentclass{hzguide}
        \LayoutSetup{}
        \CirnumSetup{
            font=\sffamily\Large\bfseries,
            fgcolor=white,
            bgcolor=red,
            sep=0.25pt,
            raise=-.5ex,
            base=99
        }
        \ExplSyntaxOn
        \NewDocumentCommand \numbers { m }
        {
            \int_step_inline:nn { #1 }{
                \cirnum{##1}
                \newpage
            }	
        }
        \ExplSyntaxOff
        \pagestyle{empty}
        \begin{document}
        \numbers{20}
        \end{document}"""
    with open(tex, mode='w', encoding='utf-8') as f:
        f.write(content)
    processor = os.path.join(dirCalled, 'open.py')    
    subprocess.call(['python', processor, tex])
    content = """
        xelatex %s
        pdfcrop %s @@@.pdf
        pdftk @@@.pdf burst
        """ %(tex, pdf)
    with open('create_circled_numbers.cmd', mode='w', encoding='utf-8') as f:
        f.write(content)

if args.output is None:
    if args.template:
        basename = 'manual'
    elif args.album:
        basename = 'album'
    else:
        basename = 'mytex'
else:
    filename = os.path.basename(args.output)
    basename = os.path.splitext(filename)[0]

tex = basename + '.tex'
pdf = basename + '.pdf'

if args.album:
    create_album()
elif args.font_glyph:
    create_font_glyph()
elif args.circled_number:
    create_circled_numbers()
elif args.merge:
    merge_pdf()
elif args.template:
    create_template()
else:
    create_tex()

