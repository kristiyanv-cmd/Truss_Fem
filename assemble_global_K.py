import numpy as np

def assemble_global_K(E, A, node_pos, con_mat):
    """
    """
    
    n_dof = 2 * node_pos.shape[0] # number of rows times the 2 DOFs per node
    K_global = np.zeros((n_dof, n_dof))  # Empty global stiffness matrix