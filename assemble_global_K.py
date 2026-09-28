import numpy as np

from k_local import local_K_matrices, local_K_matrices
from k_local import element_length
from transformation_matrix import transform_matrix

def assemble_global_K(E, A, node_pos, con_mat):
    """
    Assemble the global stiffness matrix for a 2D truss structure.
    
    The dimension of the global matrix is the DOF times the number of nodes. 
    """
    
    n_dof = 2 * node_pos.shape[0] # number of rows times the 2 DOFs per node
    K_global = np.zeros((n_dof, n_dof))  # Empty global stiffness matrix
    
    # Get K_loc matrices    
    K_loc = local_K_matrices(E, A, node_pos, con_mat) # An array of local stiffness matrices for each element
    
    
