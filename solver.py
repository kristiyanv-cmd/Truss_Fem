import numpy as np

def dof(node, direction):
    """Global row index for a given node and direction (0 = x, 1 = y)."""
    if direction not in (0, 1):
        raise ValueError("Direction must be 0 (x) or 1 (y).")
    
    return 2 * node + direction

def solve_truss(K, forces=None, BC=None):
    """
    K      : (2n x 2n) global stiffness matrix
    forces : {(node, dir): value}   applied loads
    BC     : {(node, dir): value}   prescribed displacements
                (0.0 for a fixed support)

    Returns u : full displacement vector (length 2n).
    """
    forces = forces or {}
    BC = BC or {}
    n_dof = K.shape[0]

    # Build the full force vector from the sparse input
    F = np.zeros(n_dof)
    for (node, d), value in forces.items():
        F[dof(node, d)] += value

    # Full displacement vector with the known values filled in
    u_nonzero_known = np.zeros(n_dof)   # This assumes either zero or a known displacement.
    constrained = []
    for (node, d), value in BC.items(): 
        i = dof(node, d)
        u_nonzero_known[i] = value
        constrained.append(i)
    constrained = np.array(constrained, dtype=int)

    # Move the known-displacement terms to the right-hand side
    F_mod = F - K @ u_nonzero_known

    # Replace the constrained equations by "1 * u_i = prescribed value"
    K_mod = K.astype(float)          # copy, so the original K is untouched
    K_mod[constrained, :] = 0
    K_mod[:, constrained] = 0
    K_mod[constrained, constrained] = 1
    F_mod[constrained] = u_nonzero_known[constrained]

    # One ordinary solve on the full-size system
    u = np.linalg.solve(K_mod, F_mod)
    return u