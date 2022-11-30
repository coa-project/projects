#!/usr/bin/env python3

import coaenv as cf
from bokeh.io import output_file, save, export_png
import os

fig=cf.figureplot(option="sumall")
export_png(fig,filename="tryme.png")

