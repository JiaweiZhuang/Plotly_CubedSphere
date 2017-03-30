import numpy as np


'''
=========
Constants
=========
'''

# Center of the coordinatte
center = [0,0,0]

# 4 corners of a cube panel, along the positive x-axis
# connectivity by array index: 0-1-2-3-0
corners=[[1,1,1],[1,-1,1],[1,-1,-1],[1,1,-1]]

'''
=========
Functions for normal (unstretched) cube-sphere
=========
'''
def combine_piecewise(linedata):
    '''
    linedata: a list of 3 lines to be combined into a single array,
              separated by np.NaN.
    '''
    linebreak=np.array([[np.NaN],[np.NaN],[np.NaN]])
    n_lines=len(linedata) # how many pieces
    
    data_combined=linedata[0] # start from the first piece
    for n in range(1,n_lines): 
        data_combined = np.concatenate([data_combined,linebreak,linedata[n]],
                                       axis=1)
    
    return data_combined

def normalize(v):
    '''
    normalize to unit sphere
    '''
    return v / np.sqrt(v[0,:]**2+v[1,:]**2+v[2,:]**2)

def great_circle(v1,v2,Nx,gridtype=0):
    '''
    v1: [x1,y1,z1]
    v2: [x2,y2,z2]
    
    return: great circle connecting v1 and v2
    '''
    
    alpha = np.arange(0,Nx+1)/Nx

    # modify alpha based on projection type
    if gridtype == 0:
        # true equi-distant 
        # the default grid in GEOS5/GCHP/FV3
        theta = np.arctan(np.sqrt(2));
        gama = np.pi - 2*theta
        alpha = 0.5 * np.sqrt(3) * np.sin(gama*alpha) /    \
                      np.sin(np.pi - theta - gama*alpha)
    elif gridtype == 1:
        # traditional equi-distant 
        # use alpha as it is.
        pass
    elif gridtype == 2:
        # equi-angular
        # the grid in CESM/CAM-SE
        alpha = 0.5 * (np.tan(0.25 * np.pi * (2.0 * alpha - 1.0)) + 1.0)
    else:
        raise ValueError('unknown grid type')
            
    # normalize before feed to v
    v1 /= np.sqrt(np.inner(v1,v1))
    v2 /= np.sqrt(np.inner(v2,v2))
    v = np.outer(v1,1.0-alpha)+np.outer(v2,alpha)

    return normalize(v)

def one_to_all(v_x0):
    '''
    convert gridinfo of 1 panel to 6 panels.
    Assume the input panel is along the positive x-axis
    v: a 3D numpy array.
    
    Use combine_piecewise to convert a list of lines
    before feed to this function
    '''
    
    # Programming note:
    # Always remember to use copy() for assigning the whole array!
    # Otherwise the address, instead of the value, will be passed.
    
    # the panel along the negative x axis
    v_x1 = v_x0.copy()
    v_x1[0,:] *= -1.0 # revert the x-value
    
    # two panels along y-axis
    v_y0 = v_x0.copy()
    v_y0[1,:] = v_x0[0,:] # swap x and y values
    v_y0[0,:] = v_x0[1,:]
    
    v_y1 = v_y0.copy()
    v_y1[1,:] *= -1.0 # revert the y-value
    
    # two panels along z-axis
    v_z0 = v_x0.copy()
    v_z0[2,:] = v_x0[0,:] # swap x and z values
    v_z0[0,:] = v_x0[2,:]
    
    v_z1 = v_z0.copy()
    v_z1[2,:] *= -1.0 # revert the z-value
    
    return combine_piecewise([v_x0,v_x1,v_y0,v_y1,v_z0,v_z1])

def CSgrid_edge_one(Nx):
    
    edges =  [great_circle(corners[0],corners[1],Nx),
              great_circle(corners[3],corners[2],Nx),
              great_circle(corners[0],corners[3],Nx),
              great_circle(corners[1],corners[2],Nx)]
    
    return combine_piecewise(edges)

def CSgrid_edge_all(Nx):

    return one_to_all(CSgrid_edge_one(Nx))

def CSgrid_mesh_one(Nx,N_plot=12):
    '''
    Nx: Grid resolution.
    
    N_plot: How many points used to contruct a 3D line. 
            Not necessarily equal to Nx.
    '''
    
    # generate nodes along two edges
    node_1 = (great_circle(corners[0],corners[1],Nx),
              great_circle(corners[3],corners[2],Nx))

    # connect nodes by great circles
    # For inner mesh, we can use gridtype1, whose computation is the fastest.
    # It doesn't affect the actually gridtype.
    mesh_separate_1 = [None]*(Nx+1)
    for n in range(Nx+1):
        mesh_separate_1[n] = great_circle(node_1[0][:,n],node_1[1][:,n],N_plot,
                                          gridtype=1)
    
    mesh_combined_1 = combine_piecewise(mesh_separate_1)
    
    # another direction
    node_2 = (great_circle(corners[0],corners[3],Nx),
              great_circle(corners[1],corners[2],Nx))

    mesh_separate_2  = [None]*(Nx+1)
    for n in range(Nx+1):
        mesh_separate_2[n] = great_circle(node_2[0][:,n],node_2[1][:,n],N_plot,
                                          gridtype=1)
    
    mesh_combined_2 = combine_piecewise(mesh_separate_2)
    
    return combine_piecewise([mesh_combined_1,mesh_combined_2])

def CSgrid_mesh_all(Nx,N_plot=12):
    
    return one_to_all(CSgrid_mesh_one(Nx,N_plot=N_plot))
    
'''
=========
Additionals
=========
'''

def LLgrid(Nlat,Nlon):
    # assume uniform sphere
    
    u = np.linspace(0, 2 * np.pi, Nlon)
    v = np.linspace(0, np.pi, Nlat)
    
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    return (x,y,z)

def LLgridline(Nlat=12,Nlon=24):   
    
    x,y,z = LLgrid(Nlat,Nlon)
    v = np.array([x,y,z]).swapaxes(0,1)
    
    lonline = combine_piecewise( list(v) )
    latline = combine_piecewise( list(v.swapaxes(0,2)) )
    
    return combine_piecewise([lonline,latline])

def projection(reverse_x=False):
    '''
    Project from the center to the corners
    only need two points to define a straight line.
    '''
    data_proj = []
    for corner in corners:
        one_beam = np.array([center,corner/np.sqrt(3)]).T
        if reverse_x: one_beam[0,:] *= -1.0
                              
        # always be careful when appending a whole array
        data_proj.append(one_beam.copy())

    return combine_piecewise(data_proj)

'''
=========
Only for the stretched cube-sphere
=========
'''
def cart2sph(xyz):
    
    # r-lat-lon
    rll = np.zeros_like(xyz)
    
    tho2 = xyz[0,:]**2+xyz[1,:]**2 # tho^2 = x^2+y^2
    rll[0,:] = np.sqrt(tho2+xyz[2,:]**2)
    rll[1,:] = np.arctan(xyz[2,:]/np.sqrt(tho2))
    rll[2,:] = np.arctan2(xyz[1,:],xyz[0,:]) + np.pi
    
    return rll

def sph2cart(rll):
    xyz = np.zeros_like(rll)
    
    xyz[0,:] = rll[0,:]*np.cos(rll[1,:])*np.cos(rll[2,:])
    xyz[1,:] = rll[0,:]*np.cos(rll[1,:])*np.sin(rll[2,:])
    xyz[2,:] = rll[0,:]*np.sin(rll[1,:])

    return xyz

def Schmidt_transform(v,c=1.0):
    
    D = (1-c**2)/(1+c**2)
    
    r_lat_lon = cart2sph(v)
    
    r_lat_lon[1,:] = np.arcsin( (D+np.sin(r_lat_lon[1,:])) /
                                (1+D*np.sin(r_lat_lon[1,:])) )
    
    v_new = sph2cart(r_lat_lon)
    
    return v_new


