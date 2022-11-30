#!/usr/bin/env python3

import os
import coaenv as pycoa
from bokeh.io import output_file, save
from bokeh.plotting import Figure
from datetime import datetime, date

pycoa.setwhom('owid')

DATE=date.today().strftime("%b %Y")

localDir="/home/tristan/pycoa/daily_plots/www/"
wwwDir="./"
baseDir="plots/"#+date.today().strftime("%Y%m%d")+"/"
try:
    os.mkdir(localDir+baseDir)
except FileExistsError:
    pass

htmlFile="covid19owid.html"
suffixModelHtml=".model"

localDir="/home/tristan/pycoa/daily_plots/www/"
wwwDir="./"

regionList=['World','Africa','Americas','Asia','Europe','Oceania','G7','G20','Oecd','G77','European Union','Commonwealth']
wdict={'total_deaths':'Death','total_cases':'Cases','total_people_fully_vaccinated':'Fully vaccinated','cur_icu_patients':'Current ICU patients'}
popList=['no','100k']

s="<h2 id=\"plots\">Few covid19 data graphics as examples</h2>"
s=s+"<p>Computed plots on "+datetime.now().strftime("%x, %H:%M")+", using the <code class=\"language-plaintext highlighter-rouge\">"+pycoa.getversion()+"</code> version of PyCoA. Latest data on "+pycoa.get().date.max().strftime("%x")+".</p>"
s=s+"<center>"
s=s+"<iframe src=\""+wwwDir+baseDir+"oa.html\" width=\"520\" height=\"430\" style=\"border:0\" ></iframe>"
s=s+"<iframe src=\""+wwwDir+baseDir+"ob.html\" width=\"520\" height=\"430\" style=\"border:0\" ></iframe>"
s=s+"<iframe src=\""+wwwDir+baseDir+"oc.html\" width=\"520\" height=\"430\" style=\"border:0\" ></iframe>"
s=s+"<iframe src=\""+wwwDir+baseDir+"od.html\" width=\"520\" height=\"430\" style=\"border:0\" ></iframe>"
s=s+"</center><h2 id=\"allplots\">List of plots and pycoa codes for all regions, and various configurations</h2>"

def launch_pycoa(strcmd,f,htmldescr,boolcopy=False,filecopy=""):
    lf=localDir+f
    output_file(lf)
    fig=eval("pycoa.figure"+strcmd)
    if isinstance(fig,Figure):
        fig.toolbar.active_drag=None
        fig.toolbar.active_scroll=None
        fig.toolbar.active_tap=None
    else:
        for t in fig.tabs:
            t.child.toolbar.active_drag=None
            t.child.toolbar.active_scroll=None
            t.child.toolbar.active_tap=None
    save(fig)

    if boolcopy:
        os.system("cp "+lf+" "+localDir+filecopy)

    fin = open(lf, "rt")
    data = fin.read()
    data = data.replace('</body>', '<br/><br/><hr style="width:540px;text-align:left;margin-left: 0;color:#00d7e4"/><p style="font-family: Arial"><img src="https://www.pycoa.fr/fig/logo-bitmap-small.png" height=40 alt="PyCoA logo" align="middle"/>&nbsp;&nbsp;Try it by yourself with the following Pycoa code:</p>'+
        '<p style="padding: 6px; border: 2px solid #00d7e4; background-color: #eeeeee; width: 530px "> <code style="color: blue">pycoa.setwhom("'+pycoa.getwhom()+'")<br/>pycoa.'+strcmd+'</code></p>'+
        '<p style="font-family: Arial"><a href="http://www.pycoa.fr" target="_blank">pycoa.fr&nbsp;<img src="https://raw.githubusercontent.com/wiki/coa-project/pycoa/figs/world-wide-web.png" height="25px" /></a>  <a href="mailto:support@pycoa.fr"><img src="https://raw.githubusercontent.com/wiki/coa-project/pycoa/figs/email.png" height="25px" align="bottom" /></a>   <a href="https://twitter.com/pycoa_fr" target="_blank"><img src="https://raw.githubusercontent.com/wiki/coa-project/pycoa/figs/twitter.png" height="25px" alt="Twitter" /></a>   <a href="https://github.com/coa-project/pycoa" target="_blank"><img src="https://raw.githubusercontent.com/wiki/coa-project/pycoa/figs/github.png" height="25px" alt="GitHub" /></a>   <a href="https://gitlab.in2p3.fr/lpnhe/pycoa" target="_blank"><img src="https://raw.githubusercontent.com/wiki/coa-project/pycoa/figs/gitlab.png" height="25px" alt="GitLab" /></a>   <a href="https://github.com/coa-project/pycoa/wiki" target="_blank"><img src="https://raw.githubusercontent.com/wiki/coa-project/pycoa/figs/information.png" height="25px" alt="User manual" /></a> <a href="https://www.pycoa.fr/doc" target="_blank"><img src="https://raw.githubusercontent.com/wiki/coa-project/pycoa/figs/manual.png" height="25px" alt="Core documentation" /></a> <a href="https://mybinder.org/v2/gh/coa-project/pycoa/dev?labpath=coabook/empty.ipynb" target="_blank"><img src="https://raw.githubusercontent.com/wiki/coa-project/pycoa/figs/mybinder.png" height="20px" alt="MyBinder launch" /></a> <a href="https://colab.research.google.com/github/coa-project/pycoa/blob/dev/coabook/empty.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></p>'+
        '</body>')
    fin.close()
    fin = open(lf, "wt")
    fin.write(data)
    fin.close()

    return "<li><a href=\""+wwwDir+f+"\" target=\"_blank\">"+htmldescr+"</a></li>"

cmd=[]
for r in regionList:
    s=s+"<br/><h2>"+r+"</h2>"
    for w,wdescr in wdict.items():
        s=s+"<h3>"+wdescr+"</h3>"
        for p in popList:
            s=s+"<h4>Population normalization : "+p+"</h4><ul>"

            filenameSuff=r+"_"+w+"_pop"+p+"_owid.html"

            s=s+launch_pycoa("plot(which=\""+w+"\",where=\""+r+"\",option='sumall',bypop=\""+p+"\")",
                baseDir+"plotsum_"+filenameSuff,
                "Total sum",
                r=='World' and p=='no' and w=='total_deaths',baseDir+"oa.html")

            s=s+launch_pycoa("plot(which=\""+w+"\",where=\""+r+"\",bypop=\""+p+"\")",
                baseDir+"plot_"+filenameSuff,
                "Country time series")

            s=s+launch_pycoa("hist(which=\""+w+"\",where=\""+r+"\",bypop=\""+p+"\")",
                baseDir+"hist_"+filenameSuff,
                "Histogram",
                r=='World' and p=='100k' and w=='total_people_fully_vaccinated',baseDir+"od.html")

            s=s+launch_pycoa("map(which=\""+w+"\",where=\""+r+"\",bypop=\""+p+"\")",
                baseDir+"map_"+filenameSuff,
                "Map",
                r=='World' and p=='100k' and w=='total_deaths',baseDir+"oc.html")

            if w.startswith('cur_'):
                wha='standard'
                opt=''
            else:
                wha='daily'
                opt='\'smooth7\','
            s=s+launch_pycoa("plot(which=\""+w+"\",where=\""+r+"\",what='"+wha+"',option=["+opt+"'sumall'],bypop=\""+p+"\",typeofplot=\"yearly\")",
                baseDir+"compyear_"+filenameSuff,
                "Yearly comparison",
                r=='World' and p=='no' and w=='total_cases',baseDir+"ob.html")

            s=s+launch_pycoa("plot(which=\""+w+"\",where=\""+r+"\",what='daily',option=['smooth7'],bypop=\""+p+"\")",
                baseDir+"daily_"+filenameSuff,
                "Daily contribution by country")

            if p == 'no':
                s=s+launch_pycoa("hist(which=\""+w+"\",where=\""+r+"\",typeofhist='pie')",
                    baseDir+"pie_"+filenameSuff,
                    "Pie")

            s=s+"</ul>"

#
# Replacement
#
fin = open(localDir+htmlFile+suffixModelHtml, "rt")
fout = open(localDir+htmlFile, "wt")
for line in fin:
    fout.write(line.replace('##CONTENT',s).replace('##DATE',DATE))
fin.close()
fout.close()
