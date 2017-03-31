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
layout['title']='<b>Stretched Cube-Sphere</b>'

'''
=========
Generate data and create plotly objects.
=========
'''

trace_solidsphere = gowp.sphere(r=0.99,alpha=1.0,color='white')


# plot with list of stretched factors:
Nx=24
N_plot=50

c_list = [1.0,0.75,0.5,0.25]
data_list = []

data_CSmesh_uniform = CSmath.CSgrid_mesh_all(Nx,N_plot=N_plot)
data_CSedge_uniform = CSmath.CSgrid_edge_all(Nx)

for i in range(len(c_list)):
    
    data_CSmesh = CSmath.Schmidt_transform(data_CSmesh_uniform,c=c_list[i])
    trace_CSmesh = gowp.line3d(data_CSmesh)
    
    data_CSedge = CSmath.Schmidt_transform(data_CSedge_uniform,c=c_list[i])
    trace_CSedge = gowp.line3d(data_CSedge,width=8)
    
    if i != 0:
        trace_CSmesh.update(dict(visible=False))
        trace_CSedge.update(dict(visible=False))
    
    data_list.append(trace_CSmesh.copy())
    data_list.append(trace_CSedge.copy())

figdata = go.Data(data_list+[trace_solidsphere])

'''
=========
Slider widget for stretching
=========
'''

steps = []
for i in range(len(c_list)):
    step = dict(
        method = 'restyle',
        args = ['visible', [False] * len(figdata)],
        label = str(c_list[i])
    )
    step['args'][1][i*2] = True # ONLY toggle i'th trace to "visible"
    step['args'][1][i*2+1] = True 
    step['args'][1][-1] = True # and the sphere
    steps.append(step)

sliders = [dict(
    active = 0,
    x=0.0,y=1.2,
    len = 0.25,
    currentvalue = {"prefix": "Stretch factor "},
    #pad = {"t": 50},
    steps = steps,
)]

layout['sliders'] = sliders
      
'''
=========
Additional text
=========
'''
Addition_text=dict(
        x=-0.08,
        y=1.0,
        xref='paper',
        yref='paper',
        align='left',
        text='<b>Note:</b></br>'+
             'Grid stretching is a convenient way  </br>'+
             'for local mesh refinement. The grid  </br>'+
             'configuration is logically unchanged, </br>'+
             'so it only requires minimal changes </br>'+
             'to the parallel software. </br></br>'+
             'GCHP currently only supports globally </br>'+
             'uniform grid, but the stretched grid </br>'+
             'could be a future direction.</br>'+
             '</br>For more details see:</br>'+
             'Harris, L. M., Lin, S. J., & Tu, C.(2016). </br>'+
             'High-resolution climate simulations </br>'+
             'using GFDL HiRAM with a stretched </br>'+
             'global grid. Journal of Climate, 29(11), </br>'+
             '4293-4314.',
             
             
        bgcolor='rgb(255,255,224)',
        showarrow=False
        )

layout['annotations'].append(Addition_text)      
      
'''
=========
Finally, show the entire figure
=========
'''
fig = dict(data=figdata, layout=layout)
pyoff.plot(fig, filename='CubeSphere_stretch.html')
