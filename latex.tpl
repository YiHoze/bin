[article]
output: mydoc
tex:   \documentclass[a4paper]{article}

		\usepackage{fontspec}
	  
		\begin{document}

		\end{document}

[hzbeamer]
output: mydoc
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
output: mydoc
tex:    \documentclass{hzguide}
		\LayoutSetup{}

		\begin{document}

		\end{document}

[memoir]
output: mydoc
tex:   \documentclass[a4paper]{memoir} 

		\usepackage{fontspec}

		\begin{document}

		\end{document}

[oblivoir]
output: mydoc
tex:   \documentclass{oblivoir} 

		\usepackage{fapapersize}
		\usefapapersize{*,*,30mm,*,30mm,*}

		\begin{document}

		\end{document}

[glyph]
output: myfont
placeholders: 3
defaults: Noto Serif CJK KR, 0020, FFFF
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
compile_option: -w
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
compile_option: -c
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
placeholders: 3
defaults: 210mm, 297mm, foo
tex:	`\documentclass{minimal}
		`
		`\usepackage{xparse}
		`\usepackage[a4paper]{geometry}
		`\geometry{paperwidth=\1, paperheight=\2, margin={0pt, 0pt}}
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
		`\mergepdf{\3}
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
compile_option: -l, -c
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
compile_option: -l, -c
placeholders: 2
defaults: 8, 5
tex:	`\documentclass[12pt, twocolumn]{article}
		`\usepackage[a5paper,margin=1.5cm]{geometry}
		`\usepackage{xparse}
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
		`				\tyschar*{##1}
		`				\bool_set_false:N \l_tys_horizon_bool
		`			}{
		`				\int_compare:nTF { \l_tys_cnt_int = 1 }
		`				{
		`					\bool_if:NTF \l_tys_minus_bool
		`					{ \tyschar|{##1} }
		`					{ \tyschar{##1} }
		`				}{
		`					\tyschar{##1}
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
		`\NewDocumentCommand \tyschar { s t{|} m }
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

[multilingual]
output: multilingual
placeholders:1 
defaults: Noto Serif
compile_option: -c
tex:	\documentclass{minimal} 
		\usepackage{fontspec} 
		\setlength\parskip{1.25\baselineskip} 
		\setlength\parindent{0pt}
		\setmainfont{\1}
		\begin{document}
		0 1 2 3 4 5 6 7 8 9 

		english: 
		© Keep this manual® for future use. These---lines--are-dashes.   

		chinese 中文: 
		请妥善保存本手册，以备将来使用。

		czech ČEŠTINA: 
		Uchovejte tuto příručku pro pozdější použití.

		danish DANSK: 
		Gem vejledningen til senere brug.

		dutch NEDERLANDS: 
		Bewaar deze handleiding voor later gebruik.

		finnish SUOMI: 
		Säilytä tämä käsikirja myöhempää käyttöä varten.

		french FRANÇAIS: 
		Conservez ce manuel pour un usage ultérieur.

		german DEUTSCH: 
		Bewahren Sie diese Anleitung für spätere Nutzung auf.

		greek Ελληνικά:
		Φυλάξτε αυτό το εγχειρίδιο για μελλοντική χρήση.

		italian ITALIANO: 
		Conservare questo manuale per utilizzi successivi.

		japanese 日本語: 
		後で使用するために、この取扱説明書を保管してください。

		korean 한국어: 
		나중에 참조할 수 있도록 이 매뉴얼을 잘 보관하십시오.

		norwegian NORSK:
		Oppbevar denne håndboken til senere bruk.

		polish POLSKI: 
		Zachowaj tę instrukcję na przyszłość.

		portuguese PORTUGUÊS (Brazilian): 
		Guarde este manual para uso posterior.

		russian РУССКИЙ ЯЗЫК: 
		Сохраните это руководство на будущее.

		slovakian SLOVENČINA: 
		Odložte si tento návod na neskoršie použitie.

		spanish ESPAÑOL (Latin): 
		Conserve este manual para poder usarlo más adelante.

		swedish SVENSKA: 
		Behåll denna handbok för framtida användning.

		thai ไทย:
		เก็บคู่มือนี้ไว้เพื่อใช้ในอนาคต

		turkish TÜRKÇE: 
		Bu kılavuzu daha sonra kullanmak üzere saklayın.
		\end{document}

[leaflet]
output: myleaflet
placeholders: 3
defaults: foo.pdf, 3, 12
tex:	`\documentclass{minimal}
		`
		`\usepackage{xparse, expl3}
		`\usepackage{graphicx}
		`\usepackage[a4paper]{geometry}
		`'\usepackage{pdfpages}
		`
		`\setlength\fboxsep{0pt}
		`\setlength\parindent{0pt}
		`
		`\ExplSyntaxOn
		`\tl_new:N \leaflet_target_file_tl
		`\int_new:N \leaflet_logic_number
		`\int_new:N \leaflet_real_number
		`\int_new:N \leaflet_back_position
		`\dim_new:N \leaflet_vspace_dim
		`\keys_define:nn { leaflet }
		`{
		`	scale	.tl_set:N = \leaflet_scale_tl,
		`	column	.int_set:N = \leaflet_column_int,
		`	last	.int_set:N = \leaflet_last_page_int,
		`	hspace	.dim_set:N = \leaflet_hspace_dim,
		`	vspace	.code:n = { \dim_set:Nn \leaflet_vspace_dim { #1 -\baselineskip - 0.01pt} },
		`	frame	.bool_set:N	= \leaflet_frame_bool,
		`}
		`
		`\NewDocumentCommand \LeafletSetup { m }
		`{
		`	\keys_set:nn { leaflet } {#1}
		`}
		`
		`\cs_new:Npn \leaflet_impose:n #1
		`{
		`	\hspace{\leaflet_hspace_dim}
		`	\bool_if:NTF \leaflet_frame_bool
		`		{ \fbox{\includegraphics[scale=\leaflet_scale_tl, page=#1]{\leaflet_target_file_tl}} }
		`		{ \includegraphics[scale=\leaflet_scale_tl, page=#1]{\leaflet_target_file_tl} }
		`	\int_compare:nTF { \int_mod:nn {\leaflet_logic_number}{\leaflet_column_int} = 0 }	
		`	{
		`		\int_compare:nT { \leaflet_logic_number < \leaflet_last_page_int }
		`			{ \vspace{\leaflet_vspace_dim} \newline }
		`	}{
		`		\hspace{\leaflet_hspace_dim}
		`	}
		`}
		`
		`\NewDocumentCommand \LeafletImpose { s O{} m }
		`{
		`	\LeafletSetup{#2}
		`	\tl_set:Nn \leaflet_target_file_tl {#3}
		`
		`	\int_compare:nTF { \leaflet_last_page_int = 4 }
		`	{ 
		`		\int_set:Nn \leaflet_back_position {1} 
		`	}{ 
		`		\int_set:Nn \leaflet_back_position { \leaflet_column_int + 1 } 
		`	}
		`
		`	\int_do_until:nn { \leaflet_logic_number = \leaflet_last_page_int }
		`	{
		`		\int_incr:N \leaflet_logic_number
		`		\int_incr:N \leaflet_real_number
		`		\IfBooleanT {#1}
		`		{
		`			\int_compare:nT { \leaflet_logic_number = \leaflet_back_position } 
		`			{ 
		`				\leaflet_impose:n { \leaflet_last_page_int }
		`				\int_incr:N \leaflet_logic_number
		`			}
		`		}
		`		\leaflet_impose:n { \leaflet_real_number }		
		`	}
		`}
		`\ExplSyntaxOff
		`
		`\geometry{
		`	papersize={464mm, 440mm}, 
		`	layoutsize={444mm, 420mm},
		`	margin={0pt, 0pt},
		`	layoutoffset={10mm, 10mm}, 
		`	showcrop
		`}
		`
		`\LeafletSetup{
		`	frame=false,
		`	scale=1, 
		`	hspace=0pt, 
		`	vspace=0pt
		`}
		`
		`\begin{document}
		`\LeafletImpose*[column=\2, last=\3]{\1}
		`%%\includepdf[pages={1-3, 12, 4, 5}, nup=3x2]{\1}
		`%%\includepdf[pages={6-11}, nup=3x2]{\1}
		`\end{document}

[lettercolor]
output: lettercolor
placeholders:1 
defaults: Noto Serif CJK KR
compile_option: -l
style:	`\RequirePackage{kotex}
		`\RequirePackage{tikz}
		`\RequirePackage{environ}
		`
		`\ExplSyntaxOn
		`\sys_if_engine_luatex:TF
		`{
		`	\RequirePackage{colorjamo} %% https://github.com/dohyunkim/colorjamo
		`}{
		`	\XeTeXuseglyphmetrics=0
		`}
		`\ExplSyntaxOff
		`\setmainhangulfont[Script=Hangul,Language=Korean]{Noto Serif CJK KR}
		`
		`\ExplSyntaxOn
		`\cs_generate_variant:Nn \tl_if_eq:nnTF { V }
		`\cs_generate_variant:Nn \tl_if_eq:nnT { V }
		`\cs_generate_variant:Nn \tl_if_eq:nnF { V }
		`
		`\tl_new:N \l_R_tl
		`\tl_new:N \l_G_tl
		`\tl_new:N \l_B_tl
		`\int_new:N \l_R_int
		`\int_new:N \l_G_int
		`\int_new:N \l_B_int
		`\int_new:N \l_R_incr_int
		`\int_new:N \l_G_incr_int
		`\int_new:N \l_B_incr_int
		`
		`\keys_define:nn { LetterColor }
		`{
		`	effect			.tl_set:N = 	\l_lettercolor_effect_tl,
		`	letters			.int_set:N = 	\l_lettercolor_letters_int,
		`	font			.tl_set:N = 	\l_lettercolor_font_tl,
		`	foreground		.tl_set:N = 	\l_lettercolor_fg_color_tl,
		`	background		.tl_set:N = 	\l_lettercolor_bg_color_tl,
		`	transition		.tl_set:N = 	\l_lettercolor_transition_tl,
		`	rand-min 		.tl_set:N = 	\l_lettercolor_rand_min_tl,
		`	rand-max		.tl_set:N = 	\l_lettercolor_rand_max_tl,
		`	grad-continue	.bool_set:N = 	\l_lettercolor_gradient_cont_bool,
		`	grad-RGB		.tl_set:N = 	\l_lettercolor_gradient_RGB_tl,
		`	grad-step		.int_set:N = 	\l_lettercolor_gradient_step_int,
		`	cho				.tl_set:N = 	\l_lettercolor_cho_color_tl,
		`	jung			.tl_set:N = 	\l_lettercolor_jung_color_tl,
		`	jong			.tl_set:N = 	\l_lettercolor_jong_color_tl
		`}
		`
		`\cs_new:Npn \lettercolor_RGB_decompose:N #1
		`{
		`	\tl_set:Nx \l_R_tl { \str_range:Nnn #1 { 1 }{ 2 } }
		`	\tl_set:Nx \l_G_tl { \str_range:Nnn #1 { 3 }{ 4 } }
		`	\tl_set:Nx \l_B_tl { \str_range:Nnn #1 { 5 }{ 6 } }
		`	\int_set:Nn \l_R_int { \exp_args:NV \int_from_hex:n \l_R_tl }
		`	\int_set:Nn \l_G_int { \exp_args:NV \int_from_hex:n \l_G_tl }
		`	\int_set:Nn \l_B_int { \exp_args:NV \int_from_hex:n \l_B_tl }
		`}
		`
		`\NewDocumentCommand \LetterColorSetup { s m }
		`{
		`	\keys_set:nn { LetterColor }{ #2 }
		`	\colorlet{letter}{\l_lettercolor_fg_color_tl}
		`	\colorlet{background}{\l_lettercolor_bg_color_tl}
		`	\IfBooleanT { #1 }
		`	{
		`		\lettercolor_RGB_decompose:N \l_lettercolor_gradient_RGB_tl
		`	}
		`	\int_set_eq:NN \l_R_incr_int \l_lettercolor_gradient_step_int
		`	\int_set_eq:NN \l_G_incr_int \l_lettercolor_gradient_step_int
		`	\int_set_eq:NN \l_B_incr_int \l_lettercolor_gradient_step_int
		`}
		`
		`\NewDocumentCommand \lettercolor { o +m }
		`{
		`	\IfValueT { #1 }
		`	{
		`		\keys_set:nn { LetterColor }{ #1 }
		`	}
		`	\bool_if:NF \l_lettercolor_gradient_cont_bool
		`	{
		`		\lettercolor_RGB_decompose:N \l_lettercolor_gradient_RGB_tl
		`	}
		`	\seq_set_split:Nnn \l_tmpa_seq { \par }{ #2 }
		`	\seq_map_function:NN \l_tmpa_seq \lettercolor_split_lines:n
		`}
		`
		`\int_new:N \l_seq_count_int
		`
		`\cs_new:Npn \lettercolor_split_lines:n #1
		`{
		`	\seq_set_split:Nnn \l_tmpb_seq { \\ }{ #1 }
		`	\int_set:Nn \l_seq_count_int { \seq_count:N \l_tmpb_seq }
		`
		`	\seq_map_inline:Nn \l_tmpb_seq
		`	{
		`		\seq_set_split:Nnn \l_tmpc_seq { ~ }{ ##1 }
		`		\str_case:VnF \l_lettercolor_effect_tl
		`		{
		`			{ initial }{
		`				\seq_map_function:NN \l_tmpc_seq \lettercolor_initial:n
		`			}
		`			{ count }{
		`				\seq_map_function:NN \l_tmpc_seq \lettercolor_count_letters:n
		`			}
		`		}{
		`			\seq_map_function:NN \l_tmpc_seq \lettercolor_split_words:n
		`		}
		`		\int_decr:N \l_seq_count_int
		`		\int_compare:nT { \l_seq_count_int > 0 }
		`		{
		`			\newline
		`		}
		`	}\par
		`}
		`
		`\cs_new:Npn \lettercolor_count_letters:n #1
		`{
		`	\tl_if_eq:VnF \l_lettercolor_transition_tl { none }
		`	{
		`		\lettercolor_assign_color:
		`	}
		`	\exp_args:NNx \int_set:Nn \l_tmpa_int { \tl_count:n { #1 } }	
		`	\int_compare:nTF { \l_tmpa_int >= \l_lettercolor_letters_int }
		`	{
		`		\textcolor{letter}{\l_lettercolor_font_tl #1}
		`	}{
		`		#1
		`	}\space
		`}
		`
		`\cs_new:Npn \lettercolor_initial:n #1
		`{
		`	\str_set:Nx \l_tmpa_str { \str_head:n {#1} }
		`	\str_set:Nx \l_tmpb_str { \str_tail:n {#1} }
		`	\tl_if_eq:VnF \l_lettercolor_transition_tl { none }
		`	{
		`		\lettercolor_assign_color:
		`	}
		`	\textcolor{letter}{\l_lettercolor_font_tl\l_tmpa_str}
		`	\l_tmpb_str\space
		`}
		`
		`\cs_new:Npn \lettercolor_split_words:n #1
		`{
		`	\tl_set:Nn \l_tmpc_tl { #1 }
		`	\tl_map_inline:Nn \l_tmpc_tl
		`	{
		`		\tl_if_eq:VnF \l_lettercolor_transition_tl { none }
		`		{
		`			\lettercolor_assign_color:
		`		}
		`		\str_case:Vn { \l_lettercolor_effect_tl }
		`		{
		`			{ letter }{ \lettercolor_letter:n ##1 }
		`			{ ball }{ \LetterBall{##1}\allowbreak }
		`		}
		`	}
		`	\str_case:Vn { \l_lettercolor_effect_tl }
		`	{
		`			{ letter }{ \space }
		`			{ ball }{ \space\space }
		`	}
		`}
		`
		`\cs_new:Npn \lettercolor_letter:n #1
		`{
		`	\sys_if_engine_xetex:TF
		`	{
		`		\textcolor{letter}{#1}
		`	}{
		`		\begin{colorjamo}
		`			\textcolor{letter}{#1}
		`		\end{colorjamo}
		`	}
		`}
		`
		`\cs_new:Nn \lettercolor_assign_color:
		`{
		`	\str_case:Vn \l_lettercolor_transition_tl
		`	{
		`		{ random }{ \lettercolor_assign_color_rand: }
		`		{ gradient }{ \lettercolor_assign_color_grad: }
		`	}
		`}
		`\cs_new:Nn \lettercolor_assign_color_grad:
		`{
		`	\tl_set:Nx \l_R_tl { \int_use:N \l_R_int }
		`	\tl_set:Nx \l_G_tl { \int_use:N \l_G_int }
		`	\tl_set:Nx \l_B_tl { \int_use:N \l_B_int }
		`	\definecolor{letter}{RGB}{\l_R_tl, \l_G_tl, \l_B_tl}
		`	\lettercolor_complementary:N \l_R_tl
		`	\lettercolor_complementary:N \l_G_tl
		`	\lettercolor_complementary:N \l_B_tl
		`	\definecolor{background}{RGB}{\l_R_tl, \l_G_tl, \l_B_tl}
		`	\lettercolor_grad_incr:NN \l_R_int \l_R_incr_int
		`	\lettercolor_grad_incr:NN \l_G_int \l_G_incr_int
		`	\lettercolor_grad_incr:NN \l_B_int \l_B_incr_int
		`	\tl_if_eq:VnT \l_lettercolor_effect_tl { letter }
		`	{
		`		\sys_if_engine_luatex:T
		`		{
		`			\lettercolor_jamo_color_grad:NN \l_lettercolor_cho_color_tl \jamocolorcho
		`			\lettercolor_jamo_color_grad:NN \l_lettercolor_jung_color_tl \jamocolorjung
		`			\lettercolor_jamo_color_grad:NN \l_lettercolor_jong_color_tl \jamocolorjong
		`		}
		`	}
		`}
		`
		`\cs_new:Npn \lettercolor_jamo_color_grad:NN #1 #2
		`{
		`	\exp_args:NV #2 #1
		`	\lettercolor_RGB_decompose:N #1
		`	\lettercolor_grad_incr:NN \l_R_int \l_R_incr_int
		`	\lettercolor_grad_incr:NN \l_G_int \l_G_incr_int
		`	\lettercolor_grad_incr:NN \l_B_int \l_B_incr_int
		`	\tl_clear:N \l_tmpa_tl
		`	\clist_set:Nn \l_tmpa_clist { \l_R_int, \l_G_int, \l_B_int }
		`	\clist_map_inline:Nn \l_tmpa_clist
		`	{
		`		\tl_set:Nx \l_tmpb_tl { \int_to_Hex:n { ##1 } }
		`		\exp_args:NNx \int_set:Nn \l_tmpb_int { \tl_count:N \l_tmpb_tl }
		`		\int_compare:nT { \l_tmpb_int == 1 }
		`		{
		`			\tl_put_right:Nn \l_tmpb_tl { 0 }
		`			\tl_reverse:N \l_tmpb_tl
		`		}
		`		\tl_put_right:Nx \l_tmpa_tl { \l_tmpb_tl }
		`	}
		`	\tl_set:NV #1 \l_tmpa_tl
		`}
		`
		`\cs_new:Nn \lettercolor_assign_color_rand:
		`{
		`	\lettercolor_assign_rand_dec:N \l_R_tl
		`	\lettercolor_assign_rand_dec:N \l_G_tl
		`	\lettercolor_assign_rand_dec:N \l_B_tl
		`	\definecolor{letter}{RGB}{\l_R_tl, \l_G_tl, \l_B_tl}
		`	\lettercolor_complementary:N \l_R_tl
		`	\lettercolor_complementary:N \l_G_tl
		`	\lettercolor_complementary:N \l_B_tl
		`	\definecolor{background}{RGB}{\l_R_tl, \l_G_tl, \l_B_tl}
		`	\tl_if_eq:VnT \l_lettercolor_effect_tl { letter }
		`	{
		`		\sys_if_engine_luatex:T
		`		{
		`			\lettercolor_assign_rand_hex:N \jamocolorcho
		`			\lettercolor_assign_rand_hex:N \jamocolorjung
		`			\lettercolor_assign_rand_hex:N \jamocolorjong
		`		}
		`	}
		`}
		`\cs_new:Npn \lettercolor_complementary:N #1
		`{
		`	\exp_args:NNx \int_set:Nn \l_tmpa_int { 255 - #1 }
		`	\tl_set:Nx #1 { \int_use:N \l_tmpa_int }
		`}
		`\cs_new:Npn \lettercolor_grad_incr:NN #1 #2
		`{
		`	\int_gadd:Nn #1 { #2 }
		`	\int_compare:nT { #1 > 255}
		`	{
		`		\int_gset:Nn #2 { \l_lettercolor_gradient_step_int * -1 }
		`		\int_gset:Nn #1 { 255 }
		`	}
		`	\int_compare:nT { #1 < 0}
		`	{
		`		\int_gset:Nn #2 { \l_lettercolor_gradient_step_int }
		`		\int_gset:Nn #1 { 0 }
		`	}
		`}
		`\cs_new:Npn \lettercolor_assign_rand_hex:N #1
		`{
		`	\tl_clear:N \l_tmpa_tl
		`	\int_step_inline:nn { 3 }
		`	{
		`		\tl_set:Nx \l_tmpb_tl {
		`			\int_to_Hex:n {
		`				\int_rand:nn {\l_lettercolor_rand_min_tl}{\l_lettercolor_rand_max_tl}
		`			}
		`		}
		`		\exp_args:NNx \int_set:Nn \l_tmpb_int { \tl_count:N \l_tmpb_tl }
		`		\int_compare:nT { \l_tmpb_int == 1 }
		`		{
		`			\tl_put_right:Nn \l_tmpb_tl { 0 }
		`			\tl_reverse:N \l_tmpb_tl
		`		}
		`		\tl_put_right:Nx \l_tmpa_tl { \l_tmpb_tl }
		`	}
		`	\exp_args:NV #1 \l_tmpa_tl
		`}
		`\cs_new:Npn \lettercolor_assign_rand_dec:N #1
		`{
		`	\pgfmathparse { random (\l_lettercolor_rand_min_tl, \l_lettercolor_rand_max_tl) }
		`	\tl_set:No #1 \pgfmathresult
		`}
		`
		`\NewDocumentCommand \LetterBall { m }
		`{
		`	\tikz\node[
		`		circle,shade,draw=white,thin,inner~sep=1pt,
		`		ball~color=background,
		`		text~width=1em,
		`		font=\l_lettercolor_font_tl,text~badly~centered
		`	]{\textcolor{letter}{#1}};
		`}
		`
		`\NewEnviron{LetterColor}[1][]
		`{
		`	\keys_set:nn { LetterColor }{ #1 }
		`	\exp_args:NV \lettercolor \BODY
		`}
		`\ExplSyntaxOff
		`
		`\LetterColorSetup*{
		`	effect = letter, %% ball, initial, count
		`	letters = 5,
		`	font = \bfseries,
		`	foreground = orange,
		`	background = blue,
		`	transition = none, %% gradient, random
		`	rand-min = 0, %% greater than or equal to 0
		`	rand-max = 255, %% less than or equal to 255
		`	grad-continue = false,
		`	grad-RGB = FF0000,
		`	grad-step = 5,
		`	cho = FF0000,
		`	jung = 00FF00,
		`	jong = 0000FF
		`}
tex:	\documentclass{article}
		\usepackage{lettercolor}
		\setlength\parskip{.5\baselineskip}
		\setlength\parindent{0pt}
		\begin{document}
		I am happy to join with you today in what will go down in history as the greatest demonstration for freedom in the history of our nation.

		우리 역사에서 자유를 위한 가장 훌륭한 시위가 있던 날로 기록될 오늘 이 자리에 여러분과 함께하게 된 것을 기쁘게 생각합니다.

		\begin{LetterColor}[effect=letter, transition=None]
		Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation. This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice. It came as a joyous daybreak to end the long night of their captivity.
		\end{LetterColor}

		\begin{LetterColor}[effect=letter, transition=gradient]
		백 년 전, 위대한 어느 미국인이 노예해방령에 서명을 했습니다. 지금 우리가 서 있는 이곳이 바로 그 자리입니다. 그 중대한 선언은 불의의 불길에 시들어가고 있던 수백만 흑인 노예들에게 희망의 횃불로 다가왔습니다. 그것은 그 긴 속박의 밤을 끝낼 흥겨운 새벽으로 왔습니다.
		\end{LetterColor}

		\begin{LetterColor}[effect=letter, transition=random]
		I am happy to join with you today in what will go down in history as the greatest demonstration for freedom in the history of our nation.
		\end{LetterColor}

		\begin{LetterColor}[effect=initial, transition=none]
		우리나라 역사상 자유를 위한 가장 위대한 시위가 있었던 날로서 역사에 기록될 오늘 나는 여러분과 함께 하게 되어 행복합니다.
		\end{LetterColor}

		\begin{LetterColor}[effect=initial, transition=gradient]
		Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation.
		\end{LetterColor}

		\begin{LetterColor}[effect=initial, transition=random]
		백년 전, 오늘 우리가 서있는 자리의 상징적 그림자의 주인공인, 한 위대한 미국인이, 노예해방선언문에 서명하였습니다.
		\end{LetterColor}

		\begin{LetterColor}[effect=ball, transition=none]
		This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice.
		\end{LetterColor}

		\begin{LetterColor}[effect=ball, transition=gradient]
		그 중대한 법령은 억압적 불평등의 불길에 타들어가던 수백만 흑인 노예들에게 위대한 희망의 횃불로서 다가왔습니다.
		\end{LetterColor}

		\begin{LetterColor}[effect=count, letters=5, transition=none]
		It came as a joyous daybreak to end the long night of their captivity.

		그 법령은 그들의 길었던 구속의 밤을 종식하는 기쁨의 새벽이었습니다.

		But one hundred years later, the Negro still is not free.

		그러나 백년이 지난 후에도, 흑인들은 여전히 자유롭지 못합니다.

		One hundred years later, the life of the Negro is still sadly crippled by the manacles of segregation and the chains of discrimination.

		백년이 지난 후에도, 분리의 수갑과 차별의 쇠사슬에 의해 흑인들의 삶은 여전히 슬픈 불구의 상태입니다.
		\end{LetterColor}

		\begin{LetterColor}[effect=count, letters=4, transition=gradient, grad-step=10, font=\itshape]
		One hundred years later, the Negro lives on a lonely island of poverty in the midst of a vast ocean of material prosperity.
			
		백년이 지난 후에도, 물질적 번영이라는 거대한 대양의 한가운데 홀로 떨어진 빈곤의 섬에서 흑인들은 살아가고 있습니다.
			
		One hundred years later, the Negro is still languished in the corners of American society and finds himself an exile in his own land.
			
		백년이 지난 후에도, 흑인들은 미국사회의 한 구석에서 여전히 풀이 죽고 자신의 땅에서 유배당한 자신을 보게 됩니다.
		\end{LetterColor}

		\begin{LetterColor}[effect=count, letters=3, transition=random]
		And so we’ve come here today to dramatize a shameful condition.

		그래서 이 수치스런 상황을 알리고 바꾸고자 우리는 오늘 이 자리에 나온 것입니다.

		In a sense we’ve come to our nation’s capital to cash a check.

		어떤 의미로는 수표를 현금으로 바꾸기 위해서 우리는 우리나라의 수도에 온 것입니다.

		When the architects of our republic wrote the magnificent words of the Constitution and the Declaration of Independence, they were signing a promissory note to which every American was to fall heir.

		우리나라를 건국한 사람들은 헌법과 독립선언문에 숭고한 단어들을 써넣었으며, 모든 미국인들이 상속받게 될 약속어음에 서명하였습니다.
		\end{LetterColor}

		This note was a promise that all men, yes, black men as well as white men, would be guaranteed the “unalienable Rights” of “Life, Liberty and the pursuit of Happiness.”

		그 약속어음은 모든 사람들에게, 예, 백인들처럼 흑인들에게도, 생존, 자유, 그리고 행복추구라는 양도할 수 없는 권리가 보장된다는 하나의 약속이었습니다.

		It is obvious today that America has defaulted on this promissory note, insofar as her citizens of color are concerned.

		오늘날 미국이 시민들의 피부색과 관련하여서만은 지금까지 그 약속어음 대로 이행하지 않고 있다는 것이 명백합니다.

		Instead of honoring this sacred obligation, America has given the Negro people a bad check, a check which has come back marked “insufficient funds.”

		이 신성한 의무를 존중하지 않고서, 미국은 잔고부족이라고 표기되어 되돌아 온 수표, 부도수표를 흑인들에게 주었습니다.

		But we refuse to believe that the bank of justice is bankrupt.

		그러나 우리는 정의의 은행이 파산했다고 믿기를 거부합니다.

		We refuse to believe that there are insufficient funds in the great vaults of opportunity of this nation.

		우리는 이 기회의 나라의 금고에 자금이 부족하다고 믿기를 거부합니다.

		And so, we’ve come to cash this check, a check that will give us upon demand the riches of freedom and the security of justice.

		그래서 우리는 우리에게 넘치는 자유와 정의의 보장을 가져다 줄 수표, 그 수표를 현금으로 바꾸기 위해서 여기에 왔습니다.

		We have also come to this hallowed spot to remind America of the fierce urgency of now.

		우리는 또한 미국으로 하여금 지금의 이 무서운 절박함을 깨닫게 해주기 위해 이 신성한 장소에 왔습니다.

		This is no time to engage in the luxury of cooling off or to take the tranquilizing drug of gradualism.

		지금은 ‘냉정하자’ 라는 사치스런 말이나 점진주의라는 안정제를 취할 때가 아닙니다.

		Now is the time to make real the promises of democracy.

		지금은 민주주의에 대한 약속을 지켜야 할 때입니다.

		Now is the time to rise from the dark and desolate valley of segregation to the sunlit path of racial justice.

		지금은 어둡고 황량한 차별의 계곡에서 양지 바른 인종적 정의의 길로 나와야 할 때입니다.

		Now is the time to lift our nation from the quicksands of racial injustice to the solid rock of brotherhood.

		지금은 인종적 불평등이라는 모래에서 형제애라는 단단한 바위 위로 우리 나라를 들어올려야 할 때입니다.

		Now is the time to make justice a reality for all of God’s children.

		지금은 모든 하느님의 자식들을 위해 정의를 현실화 해야 할 때입니다.

		It would be fatal for the nation to overlook the urgency of the moment.

		지금의 절박함을 무시한다면 그것은 이 나라에 치명적이 될 것입니다.

		This sweltering summer of the Negro’s legitimate discontent will not pass until there is an invigorating autumn of freedom and equality.

		흑인들의 정당한 불만으로 가득찬 이 무더운 여름은 자유와 평등이라는 상쾌한 가을이 오기까지 사라지지 않을 것입니다.

		Nineteen sixty-three is not an end, but a beginning.

		1963년은 끝이 아니라 시작입니다.

		And those who hope that the Negro needed to blow off steam and will now be content will have a rude awakening, if the nation returns to business as usual.

		흑인들이 흥분을 가라앉힐 필요가 있고 적당히 만족할 것을 바라는 사람들은 만약 이 나라가 예전의 그 일상으로 되돌아 가려고 한다면, 거친 깨달음을 얻게 될 것 입니다.

		And there will be neither rest nor tranquility in America until the Negro is granted his citizenship rights.

		흑인들이 그들의 시민권을 인정받기 전까지 미국에는 휴식도 평온도 없을 것입니다.

		The whirlwinds of revolt will continue to shake the foundations of our nation until the bright day of justice emerges.

		저항의 회오리바람은 정의가 출현하는 밝은 날이 올 때까지 우리나라의 기반을 흔들 것입니다.

		But there is something that I must say to my people, who stand on the warm threshold which leads into the palace of justice.

		그러나 정의의 궁전에 이르는 흥분되는 입구에 서있는 여러분께 내가 드려야 할 말이 있습니다.

		In the process of gaining our rightful place, we must not be guilty of wrongful deeds.

		우리의 정당한 지위를 얻는 과정에서 우리는 불법행위에 따른 범법자가 되어서는 안됩니다.

		Let us not seek to satisfy our thirst for freedom by drinking from the cup of bitterness and hatred.

		비통과 증오의 잔에서 흘러내린 물로써 자유를 향한 우리의 갈증을 풀려고 하지 맙시다.

		We must forever conduct our struggle on the high plane of dignity and discipline.

		우리는 품위와 절제의 고귀한 수준을 유지해 가면서 우리의 투쟁을 영원히 수행해 나가야 합니다.

		We must not allow our creative protest to degenerate into physical violence.

		우리의 건설적 항거가 물리적 파괴로 변질되도록 해서는 안될 것입니다.

		Again and again, we must rise to the majestic heights of meeting physical force with soul force.

		계속, 계속해서, 우리는 영혼의 힘과 물리적 힘을 함께 만날 수 있는 저 장엄한 고지를 올라가야 합니다.

		The marvelous new militancy which has engulfed the Negro community must not lead us to a distrust of all white people.

		흑인사회를 휘감고 있는 새로운 투쟁의 기운이 우리를 모든 백인들의 불신의 대상으로 이끌지 않도록 해야 합니다.

		For many of our white brothers, as evidenced by their presence here today, have come to realize that their destiny is tied up with our destiny.

		오늘 이 자리의 참석으로 증명되듯, 많은 우리의 백인형제들은, 그들의 운명이 우리의 운명과 맺어져 있음을 깨달았습니다.

		And they have come to realize that their freedom is inextricably bound to our freedom.

		그리고 그들의 자유가 우리의 자유와 떨어질 수 없게 묶여져 있음을 깨달았습니다.

		We cannot walk alone.

		우리는 홀로 걸어갈 수 없습니다.

		And as we walk, we must make the pledge that we shall always march ahead.

		그리고 걸으며, 우리는 언제나 행진에 앞장설 것을 맹세해야 합니다.

		We cannot turn back.

		우리는 되돌아갈 수 없습니다.

		There are those who are asking the devotees of civil rights, “When will you be satisfied? ”

		인권운동가들에게 다음과 같이 묻는 사람들이 있습니다, “언제쯤 당신들은 만족하겠느냐? ”

		We can never be satisfied as long as the Negro is the victim of the unspeakable horrors of police brutality.

		우리는 절대 만족할 수 없습니다, 흑인들이 경찰들의 만행에 아무런 말도 할 수 없는 두려움의 희생자가 되는 한.

		We can never be satisfied as long as our bodies, heavy with the fatigue of travel, cannot gain lodging in the motels of the highways and the hotels of the cities.

		우리는 절대 만족할 수 없습니다, 우리의 몸이 여행의 피곤으로 무거울 때 고속도로의 모텔과 시내의 호텔에서 잠자리를 얻지 못하는 한.

		We cannot be satisfied as long as the Negro’s basic mobility is from a smaller ghetto to a larger one.

		우리는 만족할 수 없습니다, 흑인들의 이동이 작은 빈민가에서 큰 빈민가로 가는 한.

		We can never be satisfied as long as our children are stripped of their selfhood and robbed of their dignity by signs stating “for white only.”

		우리는 절대 만족할 수 없습니다, 우리의 어린이들이 자존심을 박탈당하고 “백인 전용”이라 쓰여진 문구에 자신들의 존엄성을 강탈당하는 한.

		We cannot be satisfied as long as a Negro in Mississippi cannot vote and a Negro in New York believes he has nothing for which to vote.

		우리는 만족할 수 없습니다, 미시시피의 흑인들이 투표조차 할 수 없고 뉴욕의 흑인들이 투표할 대상이 없다고 믿는 한.

		No, no, we are not satisfied, and we will not be satisfied until justice rolls down like waters, and righteousness like a mighty stream.

		절대로, 절대로, 우리는 만족하지 않습니다. 정의가 강물처럼 흘러내리고, 정당함이 거대한 흐름이 될 때까지, 우리는 만족하지 않을 것입니다.

		I am not unmindful that some of you have come here out of great trials and tribulations.

		여러분들 중 일부는 거대한 시련과 고통으로부터 벗어나 여기에 왔다는 것을 나는 주목하고 있습니다.

		Some of you have come fresh from narrow jail cells.

		여러분들 중 일부는 좁은 감방에서 이제 막 나왔습니다.

		And some of you have come from areas where your quest for freedom left you battered by the storms of persecution and staggered by the winds of police brutality.

		여러분들 중 일부는 자유에 대한 당신의 요구가 당신을 박해의 폭풍 앞에서 부서지게 하고 공권력의 만행이란 바람에 비틀거리게 했던 곳에서 왔습니다.

		You have been the veterans of creative suffering.

		여러분들은 의미있는 고통에 익숙해진 노련한 사람들이 되었습니다.

		Continue to work with the faith that unearned suffering is redemptive.

		그 고통도 과분하다 여기고 보상을 받으리란 믿음으로 계속 해나가십시요.

		Go back to Mississippi, go back to Alabama, go back to South Carolina, go back to Georgia, go back to Louisiana, go back to the slums and ghettos of our northern cities, knowing that somehow this situation can and will be changed.

		돌아가십시요, 알라바마로, 남부 캘리포니아로, 조지아로, 루이지애나로, 북부 도시들의 빈민가와 흑인거주지로, 어떻게든 지금의 이 상황이 변화될 수 있다는 그리고 변화될 것이라는 인식을 갖고서 돌아가십시요.

		Let us not wallow in the valley of despair, I say to you today, my friends.

		절망의 계곡에서 몸부림치지 말자고, 나의 친구들이여, 나는 오늘 여러분께 말합니다.

		And so even though we face the difficulties of today and tomorrow, I still have a dream.

		그래서 우리가 오늘과 내일의 역경을 만나게 된다고 할지라도, 나는 아직도 꿈이 있습니다.

		It is a dream deeply rooted in the American dream.

		그 꿈은 아메리칸 드림에 깊이 뿌리를 둔 꿈입니다.

		I have a dream that one day this nation will rise up and live out the true meaning of its creed, “We hold these truths to be self-evident, that all men are created equal.”

		나에게는 꿈이 있습니다, 언젠가는, 이 나라가 일어나 “모든 사람은 평등하 게 태어났다라는 진실을 우리는 자명으로 유지한다”라는 이 나라 강령의 참뜻대로 살아가는 날이 있을 것이라는 꿈이 있습니다.

		I have a dream that one day on the red hills of Georgia, the sons of former slaves and the sons of former slave owners will be able to sit down together at the table of brotherhood.

		나에게는 꿈이 있습니다, 언젠가는, 조지아주의 붉은 언덕 위에서 노예들의 후손들과 노예소유주들의 후손들이 형제애의 식탁에서 함께 자리할 수 있을 것이라는 꿈이 있습니다.

		I have a dream that one day even the state of Mississippi, a state sweltering with the heat of injustice, sweltering with the heat of oppression, will be transformed into an oasis of freedom and justice.

		나에게는 꿈이 있습니다, 언젠가는, 불의의 열기로 무더운, 억압의 열기로 무더운, 저 미시시피마저도 자유와 정의의 오아시스로 변모할 것이라는 꿈이 있습니다.

		I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character.

		나에게는 꿈이 있습니다, 언젠가는, 나의 네명의 어린 아이들이 그들의 피부 색깔로서 판단되지 않고 그들의 개별성으로 판단되는 그런 나라에서 살게 될 것이라는 꿈이 있습니다.

		I have a dream today.

		오늘 나에게는 꿈이 있습니다.

		I have a dream that one day, down in Alabama, with its vicious racists, with its governor having his lips dripping with the words of “interposition” and “nullification”, one day right there in Alabama little black boys and black girls will be able to join hands with little white boys and white girls as sisters and brothers. I have a dream today.

		나에게는 꿈이 있습니다, 언젠가는, 사악한 인종차별주의자들이 있는 알라바마주, 연방정부의 법과 조치를 따르지 않겠다는 발언을 내뱉는 주지사가 있는 알라바마주, 언젠가는 바로 그 알라바마주에서, 어린 흑인 소년들과 어린 흑인 소녀들이, 어린 백인 소년들과 어린 백인 소녀들과 형제자매로서 손을 맞잡을 수 있을 것이라는 꿈이 있습니다. 오늘 나에게는 꿈이 있습니다.

		I have a dream that one day every valley shall be exalted, and every hill and mountain shall be made low, the rough places will be made plain, and the crooked places will be made straight, and the glory of the Lord shall be revealed, and all flesh shall see it together.

		나에게는 꿈이 있습니다, 언젠가는, 모든 골짜기들은 메워지고, 모든 언덕과 산들은 낮아지고, 거친 곳은 평평해지고, 굽은 곳은 펴지고, 하느님의 영광이 나타나고, 모든 사람들이 다같이 그 영광을 보게 될 것이라는 꿈이 있습니다.

		This is our hope, and this is the faith that I go back to the South with.

		이것이 우리의 희망이며, 이것이 내가 남부로 돌아갈 때 함께 하게 될 신념입니다.

		With this faith, we will be able to hew out of the mountain of despair a stone of hope.

		이 신념으로서, 우리는 절망의 산을 깎아 희망의 돌을 만들어 낼 수 있을 것입니다.

		With this faith, we will be able to transform the jangling discords of our nation into a beautiful symphony of brotherhood.

		이 신념으로써, 우리는 우리나라의 소란한 불협화음을 아름다운 형제애의 교향곡으로 변화시킬 수 있을 것입니다.

		With this faith, we will be able to work together, to pray together, to struggle together, to go to jail together, to stand up for preedom together, knowing that we will be free one day.

		이 신념으로써, 우리가 언젠가는 자유로워 질 것이라 믿으면서, 우리는 함께 일하고, 함께 기도하며, 함께 투쟁하며, 함께 감옥에 가고, 함께 자유를 위해 버텨낼 수 있을 것입니다.

		And this will be the day, this will be the day when all of God’s children will be able to sing with new meaning.

		이 날이, 이 날이 모든 하느님의 자식들이 새로운 의미의 노래를 부를 수 있는 바로 그 날이 될 것입니다.

		My country ‘tis of thee, sweet land of liberty, of thee I sing. Land where my fathers died, land of the Pilgrim’s pride, From every mountainside, let freedom ring.

		나의 나라 그것은 하느님의 것, 달콤한 자유의 땅, 내가 노래하는 하느님의 것 나의 조상들이 죽은 땅, 개척자의 자부심이 있는 땅, 모든 산으로부터 자유가 울려 퍼지게 합시다.

		And if America is to be a great nation, this must become true.

		미국이 위대한 나라가 되려면, 이것은 현실이 되어야 합니다.

		And so let freedom ring from the prodigious hilltops of New Hampshire. Let freedom ring from the mighty mountains of New York. Let freedom ring from the heightening Alleghenies of Pennsylvania. Let freedom
		ring from the snow-capped Rockies of Colorado. Let freedom ring from the curvaceous slopes of California.

		그래서 뉴햄프셔주의 경이로운 언덕으로부터 자유가 울려 퍼지게 합시다. 뉴욕의 거대한 산맥들로부터 자유가 울려 퍼지게 합시다. 펜실베니아주의 높다란 엘리게니산맥으로부터 자유가 울려 퍼지게 합시다. 콜로라도주의
		눈덮인 록키산맥으로부터 자유가 울려 퍼지게 합시다. 캘리포니아주의 굽이진 비탈로부터 자유가 울려 퍼지게 합시다.

		But not only that Let freedom ring from Stone Mountain of Georgia. Let freedom ring from Lookout Mountain of Tennessee. Let freedom ring from every hill and molehill of Mississippi. From every mountainside, let freedom ring.

		그것 뿐만이 아닙니다. 조지아주의 스톤산으로부터 자유가 울려 퍼지게 합시다. 테네시주의 룩아웃산으로부터 자유가 울려 퍼지게 합시다. 미시시피주의 크고 작은 모든 언덕으로부터 자유가 울려 퍼지게 합시다. 모든 산으로부터 자유가 울려 퍼지게 합시다.

		And when this happens, when we allow freedom ring, when we let it ring from every village and every hamlet, from every state and every city, we will be able to speed up that day when all of God’s children, black men and white men, Jews and Gentiles, Protestants and Catholics, will be able to join hands and sing in the words of the old Negro spiritual.

		이렇게 될 때, 자유가 울리게 할 때, 모든 마을과 부락으로부터, 모든 주와 도시로부터, 자유가 울려 퍼지게 할 때, 모든 하느님의 자식들이, 흑인과 백인이, 유대인과 이교도들이, 개신교도와 카톨릭교도들이, 손을 잡고 옛 흑인영가의 구절을 노래부를 수 있는 그날을 우리는 앞당길 수 있을 것입니다.

		Free at last, Free at last.

		마침내 자유, 마침내 자유.

		Thank God Almighty, we are free at last.

		전능하신 하느님 감사합니다, 저희는 마침내 자유가 되었습니다.
		\end{document}	