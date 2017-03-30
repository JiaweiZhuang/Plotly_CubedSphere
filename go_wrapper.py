import numpy as np
import plotly.graph_objs as go
from CubeSphere_math import LLgrid

def line3d(data,color='black',width=2):
    trace = go.Scatter3d(
        x=data[0,:], y=data[1,:], z=data[2,:],
        mode='lines', # we don't need markers
        line=dict(color=color,width=width),
        text=None, # we don't need texts
        hoverinfo='skip',
        showlegend=False
    )
    
    return trace

def marker3d(data,color='blue',size=8,symbol='diamond'):
    trace = go.Scatter3d(
        x=data[0,:], y=data[1,:], z=data[2,:],
        mode='marker', # we don't need lines
        marker=dict(size=size,color=color,symbol=symbol),
        text=None, # we don't need texts
        hoverinfo='skip',
        showlegend=False
    )
        
    return trace

def cube(size=0.2,color='grey'):
    trace_cube = go.Mesh3d(
        # coordinate
        x = size*np.array([-1, -1, 1, 1,-1,-1, 1, 1]),
        y = size*np.array([-1,  1, 1,-1,-1, 1, 1,-1]),
        z = size*np.array([-1, -1,-1,-1, 1, 1, 1, 1]),
        # connectivity
        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color=color,
        opacity=0.5
        )
    return trace_cube

def sphere(r=1.0,color='blue',alpha=0.8,N_plot=36):
    
    x,y,z = LLgrid(N_plot,N_plot)
    
    # contour attributes apply to 3 axes
    # don't want to show the contour when hovering
    cont_att = dict(highlight=False)
    
    trace_sphere = go.Surface(x=r*x,y=r*y,z=r*z,opacity=alpha,
                              showlegend=False, showscale=False,hoverinfo='skip',
                              contours=dict(x=cont_att,y=cont_att,z=cont_att),
                              colorscale=[[0, color], [1, color]])
    
    return trace_sphere
    
