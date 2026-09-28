import numpy as np

def dof(node, direction):
    """
    Calculates the row number which corresponds to the degree of freedom for a given node and direction.    
    """
    return 2 * node + direction

def solve_truss(K, n_nodes, forces=None, displacements=None):
    """
    K             : (2n x 2n) global stiffness matrix
    n_nodes       : number of nodes
    forces        : {(node, dir): value}   applied loads
    displacements : {(node, dir): value}   prescribed displacements
                    (0.0 for a fixed support)
    Returns u (full displacement vector), F (full force vector incl. reactions).
    """
    forces = forces or {}
    displacements = displacements or {}
    n_dof = 2 * n_nodes

    # Full force vector from sparse input
    F = np.zeros(n_dof)
    for (node, d), value in forces.items():
        F[dof(node, d)] += value          # += so multiple loads on one DOF add up

    # Full displacement vector with known values filled in
    u = np.zeros(n_dof)
    constrained = []
    for (node, d), value in displacements.items():
        i = dof(node, d)
        u[i] = value
        constrained.append(i)
    constrained = np.array(sorted(set(constrained)), dtype=int)

    free = np.setdiff1d(np.arange(n_dof), constrained)

    # Partitioned solve
    K_ff = K[np.ix_(free, free)]
    K_fc = K[np.ix_(free, constrained)]
    rhs = F[free] - K_fc @ u[constrained]
    u[free] = np.linalg.solve(K_ff, rhs)

    # Reactions at constrained DOFs
    F[constrained] = K[constrained, :] @ u

    return u, F