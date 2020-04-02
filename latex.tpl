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
		\MakeOuterQuote{"}

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
placeholders: 3
defaults: Noto Serif CJK KR, 0020, FFFF
compile_option: -b, -c
tex:    `\documentclass{article}
		`
		`\usepackage[a4paper, margin=2cm]{geometry}
		`\usepackage{fontspec}
		`\usepackage{xcolor}
		`
		`\XeTeXuseglyphmetrics=0
		`
		`\ExplSyntaxOn
		`\int_new:N \l_glyph_number
		`\int_new:N \l_glyph_slot
		`\tl_new:N \l_glyph_code 
		`\int_new:N \l_linebreak_int
		`\int_new:N \l_pagebreak_int
		`
		`\cs_new:Npn \line_page_break:nnn #1 #2 #3
		`{
		`	\int_set:Nn \l_linebreak_int { \int_mod:nn { #1 }{ #2 } }
		`	\int_set:Nn \l_pagebreak_int { \int_mod:nn { #1 }{ #3 } }
		`	\int_compare:nTF { \l_linebreak_int = 0 }
		`	{
		`	\int_compare:nTF { \l_pagebreak_int = 0 }
		`		{
		`			\clearpage
		`		}{
		`			\par
		`		}
		`	}{
		`		\hspace{.5em}
		`	}
		`}
		`
		`\NewDocumentCommand \ShowGlyphsByUnicode { m m m } 
		``{
		`	\setlength\parskip{-2ex}
		`	\setmainfont{#1}\fontsize{11pt}{13pt}\selectfont
		`	\group_begin:			
		`	\int_set:Nn \l_tmpa_int { \int_from_hex:n {#2} }
		`	\int_set:Nn \l_glyph_number { \int_from_hex:n {#3} }	
		`	\int_do_while:nn {	\l_tmpa_int <= \l_glyph_number } 
		`	{                
		`		\tl_set:Nn \l_glyph_code { \int_to_Hex:n {\l_tmpa_int} }
		`		\int_set:Nn \l_glyph_slot {\the\XeTeXcharglyph"\l_glyph_code} 
		`		\int_compare:nTF { \l_glyph_slot != 0 }
		`		{
		`			\parbox{1.5em}{
		`				\centering 			
		`				\raisebox{-2ex}{\sffamily\color{gray} \tiny \int_use:N \l_glyph_slot} \
		`				\char"\l_glyph_code \
		`				\raisebox{2ex}{\sffamily\color{darkgray} \tiny \l_glyph_code }
		`			}
		`		}{
		`			\parbox{1.5em}{
		`				\centering
		`				\raisebox{-2ex}{\sffamily\color{gray} \tiny \int_use:N \l_glyph_slot} \
		`				\fbox{\parbox{0.75em}{\rule{0pt}{2ex}}} \
		`				\raisebox{2ex}{\sffamily\color{darkgray} \tiny \l_glyph_code }
		`			}
		`		}       
		`		\line_page_break:nnn {  \l_tmpa_int }{ 16 }{ 256 }		         
		`		\int_incr:N \l_tmpa_int
		`	}	
		`	\group_end:
		`	\par
		`}
		`\NewDocumentCommand \ShowGlyphsBySlot { m O{1} d() }
		`{
		`	\setlength\parskip{.1ex}
		`	\font\MyFont="#1"~at~11pt \MyFont
		`	\IfValueTF{ #3 }
		`	{
		`		\int_set:Nn \l_tmpa_int { #3 }
		`	}{
		`		\int_set:Nn \l_tmpa_int { \the\XeTeXcountglyphs\MyFont }
		`	}
		`	\int_decr:N \l_tmpa_int	
		`	\int_step_inline:nnn { #2 }{ \l_tmpa_int }
		`	{
		`		\parbox{1.5em}{
		`			\centering
		`			\raisebox{-2ex}{\sffamily\color{gray} \tiny ##1} \
		`			\XeTeXglyph##1
		`		}
		`		\line_page_break:nnn { ##1 }{ 20 }{ 400 }		
		`	}	
		`}
		`\ExplSyntaxOff
		`
		`\linespread{1}
		`\setlength\parindent{0pt}
		`
		`\begin{document}     
		`%%\ShowGlyphsBySlot{Noto Serif CJK KR}%%[1](10000)
		`\ShowGlyphsByUnicode{\1}{\2}{\3}
		`\end{document}

[manual]
output: manual
compile_option: -b, -w
tex:	`\documentclass[10pt, openany]{hzguide}
		`
		`\LayoutSetup{}
		`\HeadingSetup{chapterstyle=tandh}
		`\setsecnumdepth{chapter}
		`\SectionNewpageOn
		`\DecolorHyperlinks
		`
		`\CoverSetup{    
		`	FrontLogoImage = {alertsymbol},
		`	BackLogoImage = {alertsymbol},
		`	ProductImage = {uncertain},
		`	title = {Product X},
		`	DocumentType = {User Guide},
		`	PubYear = 2018,
		`	revision = {Rev. 1},
		`	note = {Keep this manual for later use.},
		`	manufacturer = Manufacturer,
		`	address = Seoul
		`}
		`\begin{document} 
		`\frontmatter* 
		`\FrontCover
		`\tableofcontents
		`
		`\mainmatter*
		`\chapter{Introduction}\tplpara
		`\section{Features}\tpllist
		`\section{Package Items}\tplimagetable
		`\section{Specifications}\tplspectables
		`\chapter{Safety}
		`\section{General Precautions}\tpllist[itemize][itemize]
		`\section{Tools}\tplimagetable
		`\section{Safety Gear}\tplimagetable
		`\chapter{Installation}
		`\section{Installation Requirements}\tpllist
		`\section{Installing X}\tplprocedure[5]
		`\section{Checking X}\tplprocedure
		`\section{Starting X}\tpllist*
		`\chapter{Operation}\tplactions
		`\chapter{Troubleshooting}\listofproblems*\tplproblems
		`\chapter{Maintenance}
		`\section{Precautions for Maintenance}\tpllist
		`\section{Scheduled Inspection}\tpllist
		`\chapter{Warranty}
		`\section{Warranty Coverage}\tplpara*
		`\section{Limitation of Liability}\tplpara*\tpllist
		`\section{Contact Information}\tplpara*
		`
		`\appendix
		`\chapter{Technical Information}\tplspectables
		`\chapter{Glossary}\tpllist[terms]
		`
		`\BackCover
		`\end{document}

[album]
output: album
image_list: im@ges.txt
placeholders: 2
defaults: 2, 1
compile_option: -b, -c
tex:	`\documentclass{hzguide}
		`
		`\usepackge{multicol}
		`\LayoutSetup{ulmargin=15mm, lrmargin=15mm}
		`\HeadingSetup{type=article}
		`
		`\begin{document}
		`\begin{multicols}{\1}
		`\MakeAlbum[\2]{%(image_list)s}
		`\MakeAlbum* to hide image names
		`\end{multicols}
		`\end{document}

[merge]
output: merged
tex:	`\documentclass{minimal}
		`
		`\usepackage[a4paper]{geometry}
		`\geometry{paperwidth=216mm, paperheight=303mm, margin={0pt, 0pt}}
		`\usepackage{graphicx}
		`
		`\ExplSyntaxOn
		`\sys_if_engine_pdftex:T { \pdfminorversion=6 }
		`
		`\NewDocumentCommand \mergepdf { m }
		`{
		`	\bool_gset_false:N \g_tmpa_bool %% Not to break the last page
		`	\clist_set:Nn \l_tmpa_clist { #1 }    
		`	\int_set:Nn \l_tmpa_int { \clist_count:N \l_tmpa_clist }
		`	\int_step_inline:nn { \l_tmpa_int }
		`	{
		`		\clist_pop:NN \l_tmpa_clist \l_tmpa_tl
		`		\int_compare:nT { ##1 == \l_tmpa_int }
		`		{
		`			\bool_gset_true:N \g_tmpa_bool
		`		}
		`		\fetchpage{ \l_tmpa_tl }
		`	}
		`}
		`
		`\int_new:N \g_lastximage_int
		`\NewDocumentCommand \lastpageofpdf { m }
		`{
		`	\get_last_page_of_pdf:nN { #1 } \g_lastximage_int
		`}
		`
		`\cs_new_nopar:Npn \get_last_page_of_pdf:nN #1 #2
		`{
		`	\str_case_e:nn { \c_sys_engine_str }
		`	{
		`		{ xetex } {
		`			\int_gset:Nn #2 { \xetex_pdfpagecount:D "#1" }
		`		}
		`		{ pdftex } {
		`			\pdfximage{#1}
		`			\int_gset:Nn #2 { \pdflastximagepages }
		`		}
		`		{ luatex } {
		`			\saveimageresource { #1 }
		`			\int_gset:Nn #2 { \lastsavedimageresourcepages }
		`		}
		`	}
		`}
		`
		`\NewDocumentCommand \fetchpage { m }
		`{    
		`	\lastpageofpdf{#1.pdf}
		`	\int_step_inline:nn { \g_lastximage_int }    
		`	{
		`		\mbox{}\vfill
		`		\centering{\includegraphics[width=\paperwidth, page=##1]{#1}}
		`		\vfill
		`		\bool_if:NTF \g_tmpa_bool 
		`		{
		`			\int_compare:nT { ##1 < \g_lastximage_int }
		`			{
		`				\break
		`			}            
		`		}{
		`			\break
		`		}        
		`	}
		`}
		`\ExplSyntaxOff
		`
		`\begin{document}
		`\mergepdf{A, B, C}
		`\end{document}

[number]
output: circled_numbers
placeholders: 1
defaults: 20
tex:	`\documentclass{hzguide}
		`
		`\LayoutSetup{}
		`\CirnumSetup{
		`	font=\sffamily\Large\bfseries,
		`	fgcolor=white,
		`	bgcolor=red,
		`	sep=0.25pt,
		`	raise=-.5ex,
		`	base=99
		`}
		`
		`\ExplSyntaxOn
		`\NewDocumentCommand \numbers { m }
		`{
		`	\int_step_inline:nn { #1 }
		`	{
		`		\cirnum{##1}
		`		\newpage
		`	}	
		`}
		`\ExplSyntaxOff
		`
		`\pagestyle{empty}
		`
		`\begin{document}
		`\numbers{\1}
		`\end{document}

[permute]
output:	permute
placeholders: 1
defaults: adei
compile_option: -l, -b, -c
tex:	`\documentclass{article}
		`\usepackage{kotex}
		`\ExplSyntaxOn
		`\tl_new:N \l_out_tl
		`\NewDocumentCommand \PermuteWord { m }
		`{
		`	\v_permute_word:nno { #1 } { 1 } { \tl_count:n { #1 } }
		`}
		`\cs_new:Npn \v_permute_word:nnn #1 #2 #3
		`{
		`	\int_compare:nTF { #2 == #3 }
		`	{
		`		\v_print_swapped_word:n { #1 }
		`	}
		`	{
		`		\int_step_inline:nnn { #2 } { #3 }
		`		{
		`			\v_tlswap_fn:nnnN { #2 } { ##1 } { #1 } \l_out_tl
		`			\v_permute_word:Von \l_out_tl { \int_eval:n { #2 + 1 } } { #3 }
		`		}
		`	}
		`}
		`\cs_generate_variant:Nn \v_permute_word:nnn { Von, nno }
		`\cs_new:Npn \v_tlswap_fn:nnnN #1 #2 #3 #4
		`{
		`	\tl_clear:N #4
		`	\tl_set:Nx \l_tmpa_tl { #3 }
		`
		`	\int_step_inline:nn { \tl_count:N \l_tmpa_tl }
		`	{
		`		\int_case:nnF { ##1 }
		`		{
		`			{ #1 } { \tl_put_right:Nx #4 { \tl_item:Nn \l_tmpa_tl { #2 } } }
		`			{ #2 } { \tl_put_right:Nx #4 { \tl_item:Nn \l_tmpa_tl { #1 } } }
		`		}
		`		{
		`			\tl_put_right:Nx #4 { \tl_item:Nn \l_tmpa_tl { ##1 } }
		`		}
		`	}
		`}
		`\cs_new:Npn \v_print_swapped_word:n #1
		`{
		`	\mbox{ #1 }
		`	\space\space
		`}
		`\ExplSyntaxOff
		`\setlength\parindent{0pt}
		`\begin{document}
		`\PermuteWord{\1}
		`\end{document}

[lotto]
output:	lotto
compile_option: -l, -b, -c
placeholders: 2
defaults: 8, 5
tex:	`\documentclass[12pt, twocolumn]{article}
		`\usepackage[a5paper,margin=1.5cm]{geometry}
		`\usepackage{luacode}
		`\usepackage{tikz}
		`\newcommand\DrawBalls{
		`	\luaexec{
		`		local m, n = 6, 45
		`		local balls = {}
		`		local tmps = {}
		`		for i = n-m+1, n do
		`			local drawn = math.random(i)
		`			if not tmps[drawn] then
		`				tmps[drawn] = drawn	   
		`			else
		`				tmps[i] = i
		`				drawn = i
		`			end
		`			balls[\#balls+1] = drawn
		`		end
		`		table.sort(balls)
		`		for i=1,\#balls do
		`			tex.print("\\LottoBall{", balls[i], "}")
		`		end
		`	}
		`}
		`\newcommand*\LottoBall[1]{%%
		`	\GetBallColor
		`	\tikz\node[
		`			circle,shade,draw=white,thin,inner sep=1pt,
		`			ball color=ball,
		`			text width=1em,
		`			font=\sffamily,text badly centered,white
		`	]{#1};%%
		`}
		`\ExplSyntaxOn    	
		`\tl_new:N \l_R_tl
		`\tl_new:N \l_G_tl
		`\tl_new:N \l_B_tl
		`\NewDocumentCommand \GetBallColor { }
		`{
		`	\tl_set:Nx \l_R_tl { \int_rand:nn {0}{255} }
		`	\tl_set:Nx \l_G_tl { \int_rand:nn {0}{255} }
		`	\tl_set:Nx \l_B_tl { \int_rand:nn {0}{255} }
		`	\definecolor{ball}{RGB}{\l_R_tl, \l_G_tl, \l_B_tl}		
		`}
		`\NewDocumentCommand \DrawWeek { m }
		`{
		`	\int_step_inline:nn {#1}
		`	{
		`		\DrawBalls\\
		`	}
		`}	
		`\ExplSyntaxOff
		`\newcommand*\lotto[2]{
		`	\luaexec{
		`		today = os.time{year=os.date("\%%Y"), month=os.date("\%%m"), day=os.date("\%%d")}
		`		saturday_index = 6 - (os.date("\%%w"))
		`		for i=1, #1 do    
		`			next_saturday = today + (saturday_index * 86400)				
		`			date = os.date("\%%Y-\%%m-\%%d", next_saturday)
		`			tex.print("\\par\\textbf{",date,"}\\par\\nopagebreak")
		`			tex.print("\\DrawWeek{#2}")
		`			saturday_index = saturday_index + 7
		`		end
		`	}              
		`}	
		`\setlength\parindent{0pt}
		`\setlength\parskip{.5ex}
		`\begin{document}
		`\lotto{\1}{\2}
		`\end{document}  

[tys]
output:	mytys
compile_option: -b
placeholders: 1
defaults: 12.86,302.9534,-8276.1,5.1064,389.56
tex:	`\documentclass[a4paper]{article}
		`
		`\usepackage{fontspec}
		`\usepackage{xcolor}
		`\usepackage{cancel}
		`\usepackage{varwidth}
		`
		`\providecommand\disablekoreanfonts{}
		`
		`\ExplSyntaxOn
		`\keys_define:nn { tys }
		`{
		`	tysfont          .tl_set:N = \l_tys_font_tys_tl,
		`	otherfont        .tl_set:N = \l_tys_font_other_tl,
		`	fontsize         .tl_set:N = \l_tys_font_size_tl,
		`	charwidth        .dim_set:N = \l_tys_char_width_dim,
		`	decimalsymbol    .tl_set:N = \l_tys_decimal_symbol_tl,
		`	zerosymbol       .tl_set:N = \l_tys_zero_symbol_tl,
		`	linespacing      .tl_set:N = \l_tys_linespacing_tl,
		`	poscolor         .tl_set:N = \l_tys_positive_color_tl,
		`	negcolor         .tl_set:N = \l_tys_negative_color_tl,
		`}
		`
		`\NewDocumentCommand \TysSetup { m }
		`{
		`	\keys_set:nn { tys }{ #1  }
		`}
		`
		`\bool_new:N \l_tys_minus_bool
		`\bool_new:N \l_tys_before_decimal_bool
		`\bool_new:N \l_tys_after_decimal_bool
		`\bool_new:N \l_tys_horizon_bool
		`\tl_new:N \l_tys_absolute_tl
		`\int_new:N \l_tys_decimal_position_int
		`\int_new:N \l_tys_digits_before_decimal_int
		`\int_new:N \l_tys_digits_after_decimal_int
		`\int_new:N \l_tys_cnt_int
		`\int_new:N \l_tys_digit_int
		`\int_new:N \l_tys_space_int
		`
		`\NewDocumentCommand \Tys { o >{\SplitList{,}} m }
		`{
		`	\group_begin:
		`	\IfValueT {#1} { 
		`		\keys_set:nn { tys }{ #1 } 
		`	}
		`	\begin{varwidth}{\linewidth}
		`	\disablekoreanfonts
		`	\setlength\parindent{0pt}
		`	\tl_set:Nn \baselinestretch {\l_tys_linespacing_tl}
		`	\int_zero:N \l_tys_decimal_position_int
		`	\int_zero:N \l_tys_digits_before_decimal_int
		`	\int_zero:N \l_tys_digits_after_decimal_int
		`	\ProcessList{#2}{ \tys_get_decimal_position:n }
		`	\ProcessList{#2}{ \tys_process:n }
		`	\vspace{-\baselineskip}  
		`	\end{varwidth}
		`	\group_end:
		`}
		`
		`\cs_new:Npn \tys_get_decimal_position:n #1
		`{
		`	\exp_args:Nx \tl_if_eq:nnTF { \tl_head:n {#1} }{-}
		`	{ 
		`		\tl_set:Nn \l_tys_absolute_tl { \tl_tail:n {#1} } 
		`	}{ 
		`		\tl_set:Nn \l_tys_absolute_tl {#1} 
		`	}
		`	\int_zero:N \l_tys_cnt_int
		`	\exp_args:Nx \tl_map_inline:nn { \l_tys_absolute_tl }
		`	{
		`		\int_incr:N \l_tys_cnt_int
		`		\tl_if_eq:nnT {##1}{.}
		`		{
		`			\int_compare:nT { \l_tys_decimal_position_int < \l_tys_cnt_int  }
		`			{
		`				\int_set:Nn \l_tys_decimal_position_int { \l_tys_cnt_int }
		`			}
		`		}    
		`	}
		`}
		`
		`\cs_new:Npn \tys_process:n #1
		`{
		`	\fp_compare:nTF { #1 < 0 } 
		`	{ 
		`		\bool_set_true:N \l_tys_minus_bool 
		`	}{ 
		`		\bool_set_false:N \l_tys_minus_bool 
		`	}
		`	\exp_args:Nx \tl_if_eq:nnTF { \tl_head:n {#1} }{-}
		`	{
		`		\tl_set:Nn \l_tys_absolute_tl { \tl_tail:n {#1} } 
		`	}{
		`		\tl_set:Nn \l_tys_absolute_tl {#1} 
		`	}
		`
		`	\int_zero:N \l_tys_cnt_int
		`	\exp_args:Nx \tl_map_inline:nn { \l_tys_absolute_tl }
		`	{
		`		\int_incr:N \l_tys_cnt_int    
		`		\tl_if_eq:nnT {##1}{.}
		`		{
		`			\int_set:Nn \l_tys_space_int { \l_tys_decimal_position_int - \l_tys_cnt_int }
		`		}
		`	}
		`	\int_step_inline:nnnn {1}{1}{ \l_tys_space_int } { \hspace*{\l_tys_char_width_dim} }
		`	\exp_args:Nx \tys_convert:n { \l_tys_absolute_tl }
		`}
		`
		`\cs_new:Npn \tys_convert:n #1
		`{ 
		`	\bool_if:NTF \l_tys_minus_bool
		`	{ 
		`		\color{\l_tys_negative_color_tl} 
		`	}{ 
		`		\color{\l_tys_positive_color_tl} 
		`	}
		`	\tys_get_digit_numbers:n {#1}
		`	\int_if_even:nTF { \l_tys_digits_before_decimal_int }
		`	{ 
		`		\bool_set_true:N \l_tys_horizon_bool 
		`	}{ 
		`		\bool_set_false:N \l_tys_horizon_bool 
		`	}
		`	\int_set:Nn \l_tys_cnt_int { \l_tys_digits_before_decimal_int }
		`	\tl_map_inline:nn {#1} 
		`	{ 
		`		\tl_if_eq:nnTF {##1}{.}
		`		{ 
		`			\fontspec{\l_tys_font_other_tl}
		`			\l_tys_font_size_tl
		`			\l_tys_decimal_symbol_tl      
		`			\bool_set_true:N \l_tys_horizon_bool
		`		}{
		`			\bool_if:NTF \l_tys_horizon_bool
		`			{         
		`				\tys*{##1}
		`				\bool_set_false:N \l_tys_horizon_bool
		`			}{
		`				\int_compare:nTF { \l_tys_cnt_int = 1 }
		`				{
		`					\bool_if:NTF \l_tys_minus_bool
		`					{ \tys|{##1} }
		`					{ \tys{##1} }
		`				}{
		`					\tys{##1}
		`				}
		`				\bool_set_true:N \l_tys_horizon_bool 
		`			}
		`		}
		`		\int_decr:N \l_tys_cnt_int
		`	}
		`	\newline
		`}
		`
		`\cs_new:Npn \tys_get_digit_numbers:n #1
		`{
		`	\bool_set_true:N \l_tys_before_decimal_bool
		`	\bool_set_false:N \l_tys_after_decimal_bool
		`	\int_zero:N \l_tys_cnt_int
		`	\tl_map_inline:nn {#1}
		`	{
		`		\int_incr:N \l_tys_cnt_int
		`		\tl_if_eq:nnT {##1}{.}
		`		{
		`			\int_zero:N \l_tys_cnt_int
		`			\bool_set_false:N \l_tys_before_decimal_bool
		`			\bool_set_true:N \l_tys_after_decimal_bool
		`		}
		`		\bool_if:NT \l_tys_before_decimal_bool
		`		{ 
		`			\int_set:Nn \l_tys_digits_before_decimal_int { \l_tys_cnt_int }
		`		}
		`		\bool_if:NT \l_tys_after_decimal_bool
		`		{ 
		`			\int_set:Nn \l_tys_digits_after_decimal_int { \l_tys_cnt_int }
		`		}
		`	}
		`}
		`
		`%% 1D360 = 119648 : 1, 100, ...
		`%% 1D369 = 119657 : 10, 1000, ...
		`\NewDocumentCommand \tys { s t{|} m }
		`{  
		`	\group_begin:  
		`	\l_tys_font_size_tl
		`	\tl_if_eq:nnTF {#3}{0}
		`	{
		`		\fontspec{\l_tys_font_other_tl}
		`		\makebox[\l_tys_char_width_dim]{
		`			\l_tys_zero_symbol_tl
		`		}
		`	}{
		`		\IfBooleanTF {#1}
		`		{ 
		`			\int_set:Nn \l_tys_digit_int { #3 + 119656 } 
		`		}{ 
		`			\int_set:Nn \l_tys_digit_int { #3 + 119647 } 
		`		}
		`		\fontspec{\l_tys_font_tys_tl}
		`		\makebox[\l_tys_char_width_dim]{
		`			\IfBooleanTF {#2} 
		`			{ 
		`				\cancel{\char"\int_to_Hex:n{\l_tys_digit_int} } 
		`			}{ 
		`				\char"\int_to_Hex:n{\l_tys_digit_int} 
		`			}
		`		}
		`	}  
		`	\group_end:
		`}
		`\ExplSyntaxOff
		`
		`\TysSetup{
		`	linespacing=1,
		`	tysfont={Apple Symbols},
		`	otherfont={Arial},
		`	fontsize=\normalsize,
		`	charwidth=0.5em,
		`	decimalsymbol=.,
		`	zerosymbol={\char"25CB},
		`	poscolor=black,
		`	negcolor=black
		`}
		`
		`\begin{document}
		`\Tys{\1}
		`\end{document}