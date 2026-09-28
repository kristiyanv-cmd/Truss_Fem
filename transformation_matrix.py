import numpy as np


def transform_matrix(x1, y1, x2, y2):
    """
    Return the transformation matrix for a 2D truss element.
    
    Maps local element DOFs [u1', v1', u2', v2'] to global DOFs
    [u1, v1, u2, v2]
    
    Input: coordinates (x1, y1) of node 1 and (x2, y2) of node 2.
    
    """
    dx = x2-x1
    dy = y2-y1
    
    theta = np.arctan2(dy, dx)
    cos = np.cos(theta)
    sin = np.sin(theta)
    
    return np.array(
        [[cos, -sin, 0, 0],
         [sin,  cos, 0, 0],
         [0,  0, cos, -sin],
         [0,  0, sin,  cos]],
        dtype=float,
    )

