'''
Post-processing functions for the truss finite element model.

It calculates the stress, strain and outputs a clean overview of the results.
It should show the stress and strain for each element,
the displacements for each node, and the reaction forces at the supports.

'''

import numpy as np
import pandas as pd

from k_local import element_length


def element_strain_stress(E, A, node_pos, con_mat, u):
    """
    Calculate the axial strain, stress and normal force of each element.

    INPUTS:
    E: array of Young's modulus for each element
    A: array of cross-sectional areas for each element
    node_pos: (n, 2) array of nodal coordinates
    con_mat: (m, 2) connectivity matrix (nodes start from 0)
    u: (n, 2) array of nodal displacements

    OUTPUTS:
    strain: (m,) array of axial strains
    stress: (m,) array of axial stresses (positive = tension)
    force: (m,) array of axial forces (positive = tension)
    """
    L = element_length(node_pos, con_mat)

    n1 = con_mat[:, 0]
    n2 = con_mat[:, 1]

    # Direction cosines of each element
    d = node_pos[n2] - node_pos[n1]
    c = d[:, 0] / L
    s = d[:, 1] / L

    # Elongation = relative displacement projected on the element axis
    du = u[n2] - u[n1]
    elongation = du[:, 0] * c + du[:, 1] * s

    strain = elongation / L
    stress = E * strain
    force = stress * A

    return strain, stress, force


def post_process(E, A, node_pos, con_mat, u, R):
    """
    Compute the element results and print a clean overview of the results.

    OUTPUTS:
    element_results: DataFrame with the strain, stress and force per element
    node_results: DataFrame with the displacements and reaction forces per node
    """
    strain, stress, force = element_strain_stress(E, A, node_pos, con_mat, u)

    # Element numbering starts from 1 in the input file, so print the same
    element_results = pd.DataFrame({
        'Element': np.arange(1, len(con_mat) + 1),
        'NodeA': con_mat[:, 0] + 1,
        'NodeB': con_mat[:, 1] + 1,
        'Strain [-]': strain,
        'Stress [MPa]': stress,
        'Force [N]': force,
    })

    node_results = pd.DataFrame({
        'Node': np.arange(1, len(node_pos) + 1),
        'u_x [mm]': u[:, 0],
        'u_y [mm]': u[:, 1],
        'R_x [N]': R[:, 0],
        'R_y [N]': R[:, 1],
    })

    fmt = '{:.6e}'.format
    print("\n=== Element results (tension positive) ===")
    print(element_results.to_string(index=False, float_format=fmt))
    print("\n=== Nodal displacements and reaction forces ===")
    print(node_results.to_string(index=False, float_format=fmt))
    print()

    return element_results, node_results
