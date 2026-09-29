import numpy as np


def solve_truss(K, NodeForces, BC, displacements):
    """Solves the 2D truss system for nodal displacements and reaction forces.

    Parameters:
    -----------
    K             : (2n x 2n) ndarray - Global stiffness matrix
    NodeForces    : (n, 2) ndarray    - Applied forces in [X, Y] per node
    BC            : (n, 2) ndarray    - Boundary condition flags (1 = constrained, 0 = free)
    displacements : (n, 2) ndarray    - Prescribed additional displacements in [X, Y]

    Returns:
    --------
    u_total : (n, 2) ndarray - Displacements per node [u_x, u_y]
    R_total : (n, 2) ndarray - Reaction forces per node [R_x, R_y]
    """
    n_dof = K.shape[0]

    # Flatten inputs to 1D DOF vectors
    F_ext = NodeForces.flatten()
    bc_flat = BC.flatten().astype(bool)
    disp_flat = displacements.flatten()

    constrained = np.where(bc_flat)[0]

    # Helper function for solving a single pass
    def solve_pass(F_vector, u_prescribed_flat):
        u_known = np.zeros(n_dof)
        u_known[constrained] = u_prescribed_flat[constrained]

        F_mod = F_vector - K @ u_known

        K_mod = K.astype(float)
        if len(constrained) > 0:
            K_mod[constrained, :] = 0.0
            K_mod[:, constrained] = 0.0
            K_mod[constrained, constrained] = 1.0
            F_mod[constrained] = u_known[constrained]

        return np.linalg.solve(K_mod, F_mod)

    # Pass 1: Applied Forces + Constrained Nodes
    u_zero = np.zeros(n_dof)
    u_model1 = solve_pass(F_ext, u_zero)

    # Pass 2: Incremental Pass — Additional Displacements
    F_zero = np.zeros(n_dof)
    u_incremental = solve_pass(F_zero, disp_flat)

    # Superposition
    u_total_flat = u_model1 + u_incremental

    # Reaction Forces: R = K * u_total - F_ext
    R_total_flat = K @ u_total_flat - F_ext
    R_total_flat[~bc_flat] = 0.0

    # Reshape outputs to match (n, 2) format
    u_total = u_total_flat.reshape(-1, 2)
    R_total = R_total_flat.reshape(-1, 2)

    return u_total, R_total