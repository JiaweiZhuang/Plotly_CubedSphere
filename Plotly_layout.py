from plotly.graph_objs import Layout

# use the same axis attribute for x,y,z
axis_att = dict(
            range=[-1,1],
            title='',
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=False,
            showticklabels=False,
            showspikes=False, # don't want to project onto axis walls
            )

annotations=[
    dict(
        x=1.0,
        y=1.0,
        xref='paper',
        yref='paper',
        text='Left drag: rotate </br>  \
              Right drag: move </br>   \
              Roll: zoom in/out</br>   \
              </br> </br> Author: Jiawei Zhuang',
        showarrow=False
    )
    ]

layout = Layout(
    title='Cube Sphere',
    width=800,
    height=700,
    autosize=False,
    hovermode=False,
    dragmode="turntable",
    scene=dict(xaxis=axis_att,yaxis=axis_att,zaxis=axis_att),
    annotations=annotations
)

'''
    camera=dict(
        up=dict(
            x=0,
            y=0,
            z=1 
        ),  
        eye=dict(
            x=-1.7428,
            y=1.0707,
            z=0.7100,
        )   
    ),  
    aspectratio = dict( x=1, y=1, z=0.7 ),
    aspectmode = 'manual'
'''