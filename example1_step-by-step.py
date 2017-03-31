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
layout['title']='<b>Cube-Sphere Step by Step</b>'

'''
=========
Generate data and create plotly objects.
=========
'''

# object 0: sphere
trace_sphere = gowp.sphere()
trace_sphere.update(dict(visible=False))# don't show at first

# object 1: lat-lon grid
data_LLgrid = CSmath.LLgridline()
trace_LLgrid = gowp.line3d(data_LLgrid,width=1,color='blue')
trace_LLgrid.update(dict(visible=False))

# object 2: cube
trace_cube = gowp.cube()
trace_cube.update(dict(visible=False))# don't show at first

# object 3: projection beam
data_proj = CSmath.projection()
trace_proj = gowp.line3d(data_proj,width=8,color='blue')
trace_proj.update(dict(visible=False))# don't show at first

# object 4 : projection beam reverse
data_proj_rev = CSmath.projection(reverse_x=True)
trace_proj_rev = gowp.line3d(data_proj_rev,width=8,color='blue')
trace_proj_rev.update(dict(visible=False))

# object 5: cube edge one panel
data_CSedge_one = CSmath.CSgrid_edge_one(12)
trace_CSedge_one = gowp.line3d(data_CSedge_one,width=8)

# object 6: cube edge all panels
data_CSedge_all = CSmath.CSgrid_edge_all(12)
trace_CSedge_all = gowp.line3d(data_CSedge_all,width=8)

# object 7: 6 nodes along edges
N_nodes = 6
data_nodes = CSmath.CSgrid_edge_one(N_nodes)
trace_nodes = gowp.marker3d(data_nodes)
trace_nodes.update(dict(visible=False))

# object 8: c6 mesh on a panel: node connected by great circles
data_connect = CSmath.CSgrid_mesh_one(N_nodes)
trace_connect = gowp.line3d(data_connect,width=8)
trace_connect.update(dict(visible=False))

# object 9: c24 meth on a panel
Nx = 24
data_CSmesh_one = CSmath.CSgrid_mesh_one(Nx)
trace_CSmesh_one = gowp.line3d(data_CSmesh_one)
    
# object 10: c24 mesh full
data_CSmesh_all = CSmath.CSgrid_mesh_all(Nx)
trace_CSmesh_all = gowp.line3d(data_CSmesh_all)
    
# object 11: another solid sphere to be plotted together with the full mesh
trace_solidsphere = gowp.sphere(r=0.99,alpha=1.0,color='white')

# combine all objects to a single list
figdata = go.Data(
           [trace_sphere,
           trace_LLgrid,
           trace_cube,
           trace_proj,
           trace_proj_rev,
           trace_CSedge_one,
           trace_CSedge_all,
           trace_nodes,
           trace_connect,
           trace_CSmesh_one,
           trace_CSmesh_all,
           trace_solidsphere
           ])

N_objects = len(figdata)

'''
=========
Description
=========
'''

descrip_text = \
    [['Step0','A sphere with lat-lon grid overlaid',''],
     ['Step1','Insert a cube and project one of its faces to the sphere',''],
     ['Step2','Same for all the other faces',''],
     ['Step3','Now the sphere is divided into 6 panels with no gaps and overlaps',
      'Two polar panels are just the same as other 4 panels. </br>\
       This structure will remove with the polar singularities and reduce the CFL constraint.'],
     ['Step4','To further generate a grid mesh, insert nodes onto panel edges.',
      'Here the nodes are following equi-distant spacing along the edges. </br>\
       Other configurations are also possible. (see the next example)'],
     ['Step5','Connect nodes by great circles to get a mesh. Now you are done!',
      'There are many other ways to divide those 6 panels into grid meshes. </br>\
       The algorithm here (used in GCHP/GEOS5) leads to a highly uniform grid.'],
     ['Step6','Make a finer mesh in the same way',''],
     ['Step7','A full Cube Sphere mesh',
      'This is called a C24 grid (24 boxes along each edge). </br>\
       There are 24x24x6=3456 grid boxes in total, similar to the 4x5 Lat-Lon grid (3312 boxes).'],
    ]
    
N_step = len(descrip_text)

visible_config = np.ones((N_step,N_objects), dtype=bool)
# use [:] to keep the type unchanged
visible_config[:] = \
          [
           [1,1,0,0,0,0,0,0,0,0,0,0],
           [1,1,1,1,0,1,0,0,0,0,0,0],
           [1,1,1,1,1,1,1,0,0,0,0,0],
           [1,1,0,0,0,1,1,0,0,0,0,0],
           [1,1,0,0,0,1,1,1,0,0,0,0],
           [1,1,0,0,0,1,1,1,1,0,0,0],
           [1,1,0,0,0,1,1,0,0,1,0,0],
           [0,0,0,0,0,1,1,0,0,0,1,1],
          ]

'''
=========
Design the update menu
=========
'''

button_config = []

for n in range(N_step):
    config_temp =  dict(label = descrip_text[n][0],
                        method = 'update', #need to change both objects and layout
                        args = [{'visible': visible_config[n]},
                                {'title': '<b>'+descrip_text[n][1]+'</b>'+
                                 '</br>'+descrip_text[n][2]}]
                        )
    button_config.append(config_temp.copy())

updatemenus = list([
    dict(type="buttons",
         buttons=button_config,
         active=-1,
         #direction = 'left',
         pad = {'r': 10, 't': 10},
         showactive = True,
         x = 0.0,
         xanchor = 'left',
         y = 1.0,
         yanchor = 'top' 
    )
])

layout['updatemenus'] = updatemenus
      
'''
=========
Finally, show the entire figure
=========
'''
fig = dict(data=figdata, layout=layout)
pyoff.plot(fig, filename='CubeSphere_step-by-step.html')
