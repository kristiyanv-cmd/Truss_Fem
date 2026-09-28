import numpy as np

def local_K_matrix(E, A, L):
    """
    Make a local stiffness matrix for a 1D truss. 
    """
    
    k_axial = (E*A)/L
    K_local = k_axial * np.array([[1, -1], [-1, 1]], dtype=float)
    
    return K_local