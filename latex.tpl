[article]
output: mytex
tex:   \documentclass[a4paper]{article}

        \usepackage{fontspec}
      
        \begin{document}

        \end{document}

[hzbeamer]
output: mytex
tex:   \documentclass[10pt,flier=false,hangul=true]{hzbeamer}

        \usepackage{csquotes}
        \MakeOuterQuote{\"}

        \title{}
        \author{}
        \institute{}
        \date{}

        \begin{document}    
        \begin{frame}[fragile, allowframebreaks=1]{}

        \end{frame}
        \end{document}

[hzguide]
output: mytex
tex:    \documentclass{hzguide}
        \LayoutSetup{}

        \begin{document}

        \end{document}

[memoir]
output: mytex
tex:   \documentclass[a4paper]{memoir} 

        \usepackage{fontspec}

        \begin{document}

        \end{document}

[oblivoir]
output: mytex
tex:   \documentclass{oblivoir} 

        \usepackage{fapapersize}
        \usefapapersize{*,*,30mm,*,30mm,*}

        \begin{document}

        \end{document}

[glyph]
output: myfont
tex:   \documentclass[12pt]{article}

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
        \end{document}

[manual]
output: manual
compile_option: -b, -w
tex:   \documentclass[10pt, openany]{hzguide}

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
        \end{document}

[album]
output: album
image_list: im@ges.txt
compile_option: -b, -c
tex:   \documentclass{hzguide}
        
        %%\usepackge{multicol}
        \LayoutSetup{ulmargin=15mm, lrmargin=15mm}
        \HeadingSetup{type=article}

        \begin{document}
        %%\begin{multicols}{2}
        \MakeAlbum[1]{%(image_list)s}
        %%\MakeAlbum* to hide image names
        %%\end{multicols}
        \end{document}

[merge]
output: merged
tex:   \documentclass{minimal}
        
        \usepackage[a4paper]{geometry}
        \geometry{paperwidth=216mm, paperheight=303mm, margin={0pt, 0pt}}
        \usepackage{graphicx}
        \usepackage{xparse}

        \ExplSyntaxOn
        \sys_if_engine_pdftex:T { \pdfminorversion=6 }

        \NewDocumentCommand \mergepdf { m }
        {
            \bool_gset_false:N \g_tmpa_bool %% Not to break the last page
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
                    \int_gset:Nn #2 { \xetex_pdfpagecount:D "#1" }
                }
                { pdftex } {
                    \pdfximage{#1}
                    \int_gset:Nn #2 { \pdflastximagepages }
                }
                { luatex } {
                    \saveimageresource { #1 }
                    \int_gset:Nn #2 { \lastsavedimageresourcepages }
                }
            }
        }

        \NewDocumentCommand \fetchpage { m }
        {    
            \lastpageofpdf{#1.pdf}
            \int_step_inline:nn { \g_lastximage_int }    
            {
                \mbox{}\vfill
                \centering{\includegraphics[width=\paperwidth, page=##1]{#1}}
                \vfill
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
        \end{document}

[number]
output: circled_numbers
tex:   \documentclass{hzguide}

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
        \end{document}