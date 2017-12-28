import plotly.offline as pyoff
import plotly.graph_objs as go

import Plotly_layout
import CubeSphere_math as CSmath
import go_wrapper as gowp# -*- coding: utf-8 -*-

# set a clean background
layout = Plotly_layout.layout
layout['annotations'] = [] # remove my personal signature

# tweak initial camera angle (https://plot.ly/python/3d-camera-controls/)
layout['scene']['camera']['eye'] = {'x': 1.4, 'y': -0.6, 'z': 0.6}

# =======================
# make individual objects
# =======================

# object 1: transparent sphere
trace_sphere = gowp.sphere(r=0.985, alpha=0.5,color='white')

# object 2: white, solid sphere
trace_solidsphere = gowp.sphere(r=0.99,alpha=1.0,color='white')

# object 3: cube edge all panels
data_CSedge_all = CSmath.CSgrid_edge_all(12)
trace_CSedge_all = gowp.line3d(data_CSedge_all,width=8)

# object 4: 6 nodes along edges
N_nodes = 6
data_nodes = CSmath.CSgrid_edge_one(N_nodes)
trace_nodes = gowp.marker3d(data_nodes)

# object 5: c6 mesh on a panel: node connected by great circles
data_connect = CSmath.CSgrid_mesh_one(N_nodes)
trace_connect = gowp.line3d(data_connect,width=4)

# object 6: c24 mesh full
data_CSmesh_all = CSmath.CSgrid_mesh_all(24)
trace_CSmesh_all = gowp.line3d(data_CSmesh_all)

# =============================
# assemble objects into figures
# =============================

# Step 1: Image of a cube with 6 faces, no subdivisions
figdata = go.Data(
           [trace_sphere,
            trace_CSedge_all,
           ])

fig = dict(data=figdata, layout=layout)
pyoff.plot(fig, filename='CS_step1.html')

# Step 2: Image of a C6 cube where the nodes on each edge are shown (no connecting arcs yet)
figdata = go.Data(
           [trace_sphere,
            trace_CSedge_all,
            trace_nodes
           ])

fig = dict(data=figdata, layout=layout)
pyoff.plot(fig, filename='CS_step2.html')

# Step 3: Image of a C6 cube where one face has been filled out fully, with connecting arcs and node
figdata = go.Data(
           [trace_sphere,
            trace_CSedge_all,
            trace_nodes,
            trace_connect
           ])

fig = dict(data=figdata, layout=layout)
pyoff.plot(fig, filename='CS_step3.html')

# Step 4: Image of a C24 cube
figdata = go.Data(
           [trace_solidsphere,
            trace_CSedge_all,
            trace_CSmesh_all
           ])

fig = dict(data=figdata, layout=layout)
pyoff.plot(fig, filename='CS_step4.html')