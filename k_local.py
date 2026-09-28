import numpy as np

def element_length(node_positions, connectivity_matrix):
    """
    Calculate the length of a 1D truss element given its nodal coordinates.
    """

    element_lengths = np.zeros(connectivity_matrix.shape[0])

    for i in range(connectivity_matrix.shape[0]):
        node1 = connectivity_matrix[i, 0]
        node2 = connectivity_matrix[i, 1]
        
        x1 = node_positions[node1, 0]
        x2 = node_positions[node2, 0]
        y1 = node_positions[node1, 1]
        y2 = node_positions[node2, 1]
        
        element_lengths[i] = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return element_lengths

def local_K_matrix(E, A):
    """
    Make a local stiffness matrix for a 1D truss. 
    """

    L = def element_length(node_positions, connectivity_matrix)    
    k_axial = (E*A)/L
    K_local = k_axial * np.array([[1, -1], [-1, 1]], dtype=float)
    
    return K_local