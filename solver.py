import numpy as np

def dof(node, dir):
    """Global row index for a given node and direction (0 = x, 1 = y)."""
    if dir == 'X':
        direction = 0
    elif dir == 'Y':
        direction = 1
    else:
        raise ValueError("Direction must be 'X' or 'Y'.")

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
    F_mod = F - K @ u_nonzero_known     # If u_nonzero_known is zero, this does nothing. Otherwise, it moves the known displacements to the right-hand side.

    # Replace the constrained equations by "1 * u_i = prescribed value"
    K_mod = K.astype(float)          # copy, so the original K is untouched
    K_mod[constrained, :] = 0
    K_mod[:, constrained] = 0
    K_mod[constrained, constrained] = 1
    F_mod[constrained] = u_nonzero_known[constrained]

    # One ordinary solve on the full-size system
    u = np.linalg.solve(K_mod, F_mod)
    return u


# def test_solve_truss():
#     # Build K for the 3-node example (EA = 1)
#     nodes = np.array([[0, 0], [1, 0], [0, 1]], dtype=float)
#     bars = [(0, 1), (0, 2), (1, 2)]
#     EA = 1.0

#     K = np.zeros((6, 6))
#     for i, j in bars:
#         d = nodes[j] - nodes[i]
#         L = np.linalg.norm(d)
#         c, s = d / L
#         k = EA / L * np.array([[c*c, c*s], [c*s, s*s]])
#         idx = [dof(i, 'X'), dof(i, 'Y'), dof(j, 'X'), dof(j, 'Y')]
#         K[np.ix_(idx, idx)] += np.block([[k, -k], [-k, k]])

#     forces = {(2, 'Y'): -10.0}
#     F = np.zeros(6)
#     F[dof(2, 'Y')] = -10.0

#     def show(title, u):
#         print(title)
#         for n in range(len(u) // 2):
#             print(f"  node {n}: ux = {u[dof(n, 'X')]:8.4f}   uy = {u[dof(n, 'Y')]:8.4f}")

#     def check_equilibrium(BC, u):
#         constrained = [dof(n, d) for (n, d) in BC]
#         free = [i for i in range(6) if i not in constrained]

#         residual = K @ u - F                 # zero wherever no support acts
#         assert np.allclose(residual[free], 0), residual[free]

#         R = residual[constrained]            # reactions at the constrained DOFs
#         print("  reactions at constrained DOFs", constrained, "->", np.round(R, 4))

#         # Global equilibrium: reactions + applied loads sum to zero in x and y
#         total = F.copy()
#         total[constrained] += R
#         assert np.isclose(total[0::2].sum(), 0)   # sum of all x-forces
#         assert np.isclose(total[1::2].sum(), 0)   # sum of all y-forces

#     # Case 1: all-zero boundary conditions
#     BC = {(0, 'X'): 0.0, (0, 'Y'): 0.0, (1, 'Y'): 0.0}
#     u = solve_truss(K, forces, BC)
#     show("Case 1: zero BCs", u)
#     assert np.allclose(u, [0, 0, 0, 0, -10, -10]), u
#     check_equilibrium(BC, u)

#     # Case 2: node 1 displaced 0.5 in y
#     BC = {(0, 'X'): 0.0, (0, 'Y'): 0.0, (1, 'Y'): 0.5}
#     u = solve_truss(K, forces, BC)
#     show("Case 2: node 1 displaced 0.5 in y", u)
#     assert np.allclose(u, [0, 0, 0, 0.5, -10.5, -10]), u
#     check_equilibrium(BC, u)

#     print("All tests passed")

# test_solve_truss()