from datetime import datetime

POST_TEMPLATE = {
    "id": -1,
    "title": u"名称（简写）",
    "description": "",
    "usage": "``",
    "complexity": "$\mathcal O()$",
    "code": "",
    "note": "",
    "author": "[Nobody]",
    "time": datetime(2000, 1, 1)
}

LATEX_TEMPLATE_PREV = r'''
\documentclass[UTF8]{article}
\usepackage{ctex}
\usepackage[fontsize=7pt]{fontsize}
\usepackage{graphicx}
\graphicspath{ {./images/} }
\usepackage{listings}
\usepackage{courier}
\usepackage[T1]{fontenc}
\setCJKmainfont{仿宋}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{multicol}
\usepackage[landscape,margin=.1in,footskip=.1in]{geometry}
\geometry{a4paper,left=2cm,right=0.2cm,top=0.3cm,bottom=0.5cm}
\renewcommand{\baselinestretch}{1}
\setlength\parindent{0pt}
\usepackage{titlesec}
\titlespacing\section{0pt}{0pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}
\titlespacing\subsection{0pt}{0pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}
\titlespacing\subsubsection{0pt}{0pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}
\titleformat*{\section}{\LARGE\bfseries}
\titleformat*{\subsection}{\Large\bfseries}
\titleformat*{\subsubsection}{\large\bfseries}
\titleformat*{\paragraph}{\large\bfseries}
\titleformat*{\subparagraph}{\large\bfseries}
\lstdefinestyle{codestyle}{
    language=c++,
    keywordstyle=\bfseries,
    basicstyle=\ttfamily\normalsize,
    breaklines=true,
    tabsize=4,
    showspaces=false,
    showstringspaces=false
}
\lstset{style=codestyle}
\setcounter{secnumdepth}{5}
\setcounter{tocdepth}{5}
\setlength{\columnsep}{0.4cm}
\setlength{\columnseprule}{0.2pt}
\begin{document}
\begin{multicols*}{3}
\tableofcontents
\bigskip
'''

LATEX_TEMPLATE_NEXT = r'''
\end{multicols*}
\end{document}
'''

LATEX_LEVEL = [
    lambda title, number="": "\\section{{{}}}".format(title),
    lambda title, number="": "\\subsection{{{}}}".format(title),
    lambda title, number="": "\\subsubsection{{{}}}".format(title),
    lambda title, number="": "\\paragraph{{{}}}\\hspace{{0cm}}".format(title),
    lambda title, number="": "\\subparagraph{{{}}}\\hspace{{0cm}}".format(
        title),
    lambda title, number="": "\\textbf{{{} {}}}".format(number, title)
]
