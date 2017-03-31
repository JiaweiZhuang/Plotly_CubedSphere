import plotly.offline as pyoff
import plotly.graph_objs as go
import numpy as np

import Plotly_layout
import CubeSphere_math as CSmath
import go_wrapper as gowp


'''
=========
Get the layout info from another file
=========
'''
layout = Plotly_layout.layout
layout['title']='<b>Cube-Sphere Grid Comparision</b></br>'+\
                'click on legends to show/hide each type of grid</br>'
layout['legend'] = dict(x=-0.2,y=1.0)
      
'''
=========
Generate data and create plotly objects.
=========
'''

descrip_text = ['"True equi-distant": </br>'+
                'The default grid in GCHP/GEOS5.',
                
                '</br>"Traditional equi-distant": </br>'+
                'The cube-sphere grid first invented, </br> with the simplest formula.</br>'+
                'Not uniform enough.',
                '</br>"Equi-angular": </br>'+
                'The grid in CAM-SE (CESM dycore) </br>'
                'More uniform than our grid at corners, </br>'+
                'but boxes near edges get stretched. </br>'+
                '(length-to-width ratio is not equal to 1)'
                ]

Nx=6
N_plot = 24
width = 4
data_CSmesh0 = CSmath.CSgrid_mesh_all(Nx,N_plot = N_plot,gridtype=0)
trace_CSmesh0 = gowp.line3d(data_CSmesh0,color='black',width = width)
trace_CSmesh0.update(dict(showlegend=True,name=descrip_text[0],visible=True))

data_CSmesh1 = CSmath.CSgrid_mesh_all(Nx,N_plot = N_plot,gridtype=1)
trace_CSmesh1 = gowp.line3d(data_CSmesh1,color='blue',width = width)
trace_CSmesh1.update(dict(showlegend=True,name=descrip_text[1],visible="legendonly"))

data_CSmesh2 = CSmath.CSgrid_mesh_all(Nx,N_plot = N_plot,gridtype=2)
trace_CSmesh2 = gowp.line3d(data_CSmesh2,color='green',width = width)
trace_CSmesh2.update(dict(showlegend=True,name=descrip_text[2],visible=True))

data_CSedge = CSmath.CSgrid_edge_all(N_plot)
trace_CSedge = gowp.line3d(data_CSedge,width=8)

trace_solidsphere = gowp.sphere(r=0.99,alpha=1.0,color='white')


'''
=========
Additional text
=========
'''
Addition_text=dict(
        x=-0.2,
        y=0.1,
        xref='paper',
        yref='paper',
        align='left',
        text='<b>Note:</b></br>'+
             'All three grids here use gnomonic projection,</br>'+
             'which means all grid lines are great circles.</br>'+
             'There are other types of cube-sphere grids, </br>'+
             'but are typically less uniform.</br>'+
             '</br>For more details see:</br>'+
             'Putman, W. M., & Lin, S. J. (2007). </br>'+
             'Finite-volume transport on various  </br>'+
             'cubed-sphere grids. Journal of </br>'+
             'Computational Physics, 227(1), 55-78.',
        bgcolor='rgb(255,255,224)',
        showarrow=False
        )

layout['annotations'].append(Addition_text)

figdata = go.Data([trace_solidsphere,trace_CSedge,
                   trace_CSmesh0,trace_CSmesh1,trace_CSmesh2
                   ])
      
'''
=========
Finally, show the entire figure
=========
'''
fig = dict(data=figdata, layout=layout)
pyoff.plot(fig, filename='CubeSphere_comparision.html')
