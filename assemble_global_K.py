import numpy as np
from k_local import local_K_matrices
from k_local import element_length
from transformation_matrix import transform_matrix


def assemble_global_K(E, A, node_pos, con_mat):
    """
    Assemble the global stiffness matrix for a 2D truss structure.
    
    The dimension of the global matrix is the DOF times the number of nodes. 
    
    for a given con_mat, 
    enumerate(con_mat) gives 
    0 0 1 
    1 0 2
    2 1 2 
    the first column is the element number, 
    the second column is the first node of the element, 
    and the third column is the second node
    
    """
    # number of rows times the 2 DOFs per node
    n_dof = 2 * node_pos.shape[0] 
    
    # Empty global stiffness matrix
    K_global = np.zeros((n_dof, n_dof))  
    
    # Get K_locals matrices    
    K_locals = local_K_matrices(E, A, node_pos, con_mat) # An array of local stiffness matrices for each element
    
    for e, (n1, n2) in enumerate(con_mat):
        x1, y1 = node_pos[n1]
        x2, y2 = node_pos[n2]
        
        # Get the transformation matrix for the current element
        T = transform_matrix(x1, y1, x2, y2) 
        
        # Transformation, T is an orth matrix so T.T = T^-1.
        K_e = T @ K_locals[e] @ T.T 
        
        # Position in the global stiffness matrix for the current element's DOFs
        dofs = [2*n1, 2*n1 + 1, 2*n2, 2*n2 + 1] 
        
        # Adding the one element matrix to the global matrix at the correct DOFs
        K_global[np.ix_(dofs, dofs)] += K_e 
        
    return K_global    
    
# element_modulus= np.array([210e9, 210e9, 210e9])  # Young's modulus for each element in Pascals
# element_area= np.array([0.02, 0.01, 0.01])  # Cross-sectional area for each element in square meters
# node_positions = np.array([[0, 0], [1, 0], [1, 1]])  # Nodal coordinates
# connectivity_matrix = np.array([[0, 1], [0, 2], [1, 2]])  # Element connectivity matrix

# print("Element Lengths:", element_length(node_positions, connectivity_matrix))
# print("Local Stiffness Matrices:\n", local_K_matrices(element_modulus, element_area, node_positions, connectivity_matrix))
# print("Global Stiffness Matrix:\n", assemble_global_K(element_modulus, element_area, node_positions, connectivity_matrix))
