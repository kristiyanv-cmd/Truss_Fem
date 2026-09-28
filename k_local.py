import numpy as np

def element_length(node_pos, con_mat):
    """
    Calculate the length of a 1D truss element given its nodal coordinates.

    OUTPUTS:
    element_lengths: array of lengths for each element
    """

    element_lengths = np.zeros(con_mat.shape[0])

    for i in range(con_mat.shape[0]):
        node1 = con_mat[i, 0]
        node2 = con_mat[i, 1]
        
        x1 = node_pos[node1, 0]
        x2 = node_pos[node2, 0]
        y1 = node_pos[node1, 1]
        y2 = node_pos[node2, 1]
        
        element_lengths[i] = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return element_lengths


def local_K_matrix(E, A, node_pos, con_mat):
    
    L = element_length(node_pos, con_mat)

    K_local = np.zeros((con_mat.shape[0], 2, 2))

    for i in range(con_mat.shape[0]):
        
        k_axial = (E[i] * A[i]) / L[i]

        K_local[i] = k_axial * np.array([[1, -1],
                                         [-1, 1]])

    return K_local


element_modulus= np.array([210e9, 210e9])  # Young's modulus for each element in Pascals
element_area= np.array([0.02, 0.01])  # Cross-sectional area for each element in square meters
node_positions = np.array([[0, 0], [1, 0], [1, 1]])  # Nodal coordinates
connectivity_matrix = np.array([[0, 1], [0, 2]])  # Element connectivity matrix

print("Element Lengths:", element_length(node_positions, connectivity_matrix))
print("Local Stiffness Matrices:\n", local_K_matrix(element_modulus, element_area, node_positions, connectivity_matrix)[1])
