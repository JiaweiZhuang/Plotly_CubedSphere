import plotly.offline as pyoff
import plotly.graph_objs as go
from plotly.widgets import GraphWidget
import numpy as np

import Plotly_layout
import CubeSphere_math as CSmath
import go_wrapper as gowp

"""
See https://plot.ly/python/sliders/
"""


'''
=========
Get the layout info from another file
=========
'''
layout = Plotly_layout.layout

'''
=========
Generate data and create plotly objects.
=========
'''

Nx=24
c=0.5
data_CSmesh = CSmath.CSgrid_mesh_all(Nx,N_plot=50)

data_CSmesh = CSmath.Schmidt_transform(data_CSmesh,c=c)

trace_CSmesh = gowp.line3d(data_CSmesh)

data_CSedge = CSmath.CSgrid_edge_all(Nx)
data_CSedge = CSmath.Schmidt_transform(data_CSedge,c=c)
trace_CSedge = gowp.line3d(data_CSedge,width=8)


'''
=========
Slider widget for stretching
=========
'''


trace_solidsphere = gowp.sphere(r=0.99,alpha=1.0,color='white')

figdata = go.Data([trace_CSmesh,trace_CSedge,trace_solidsphere])
      
'''
=========
Finally, show the entire figure
=========
'''
fig = dict(data=figdata, layout=layout)
pyoff.plot(fig, filename='CubeSphere_stretch.html')
