import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from solver import solve_truss
from k_local import element_length
from assemble_global_K import assemble_global_K
from post_proc import post_process


class FEModel:

    def __init__(self, NodePos, NodeForces, BC, displacements, ElementJoints, E, A):
        self.NodePos= NodePos
        # print("NodePos:", NodePos)
        self.NodeForces = NodeForces
        self.BC = BC
        self.displacements = displacements
        self.Element = ElementJoints
        self.E = E
        self.A = A
    
    def solve(self):
        self.K = assemble_global_K(self.E, self.A, self.NodePos, self.Element)
        self.u, self.Reactions = solve_truss(self.K, self.NodeForces, self.BC, self.displacements)
        # print("Displacements:", self.u)
        self.NodePos2 = self.NodePos + self.u * 20

    def post_process(self):
        self.element_results, self.node_results = post_process(
            self.E, self.A, self.NodePos, self.Element, self.u, self.Reactions)


def DataReader(filename):
    #reads the data from a CSV file. Drops missing values, forces int for indices.
    #returns (n,2) note, force, boundary condition, displacement and element joint np arrays
    #returns (n,) np arrays for element modulus and area
    #nodes start from node 0
    df = pd.read_csv(filename)
    NodePos = df[['NodePosX', 'NodePosY']].dropna().to_numpy()
    NodeForces = df[['NodeForceX', 'NodeForceY']].dropna().to_numpy()
    BC = df[['BCX', 'BCY']].dropna().to_numpy()
    displacements = df[['DisplacementX', 'DisplacementY']].dropna().to_numpy()
    ElementJoints = df[['NodeConnectionA', 'NodeConnectionB']].dropna().astype(int).to_numpy()
    ElementJoints = ElementJoints - 1  
    E = df['ElementModulus'].dropna().to_numpy()
    A = df['ElementArea'].dropna().to_numpy()

    return NodePos, NodeForces, BC, displacements, ElementJoints, E, A

def Plotter(NodePos, ElementJoints, NodePos2=None):

    # print(ElementJoints)
    
    plt.figure()
    for i, element in enumerate(ElementJoints):
        node1 = element[0]
        node2 = element[1]
        x_values = [NodePos[node1][0], NodePos[node2][0]]
        y_values = [NodePos[node1][1], NodePos[node2][1]]
        plt.plot(x_values, y_values, 'g--', linewidth=2,
                 label='Undeformed' if i == 0 else None)

    if NodePos2 is not None:
        for i, element in enumerate(ElementJoints):
            node1 = element[0]
            node2 = element[1]
            x_values = [NodePos2[node1][0], NodePos2[node2][0]]
            y_values = [NodePos2[node1][1], NodePos2[node2][1]]
            plt.plot(x_values, y_values, 'r-o',
                     label='Deformed' if i == 0 else None)

    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Truss Structure: Undeformed vs Deformed')
    plt.grid()
    plt.legend()
    plt.axis('equal')


def StressPlotter(NodePos2, ElementJoints, stress):
    # Deformed structure, elements coloured by signed stress (tension positive),
    # symmetric range around zero so that zero stress is the neutral colour
    s_max = np.abs(stress).max()
    norm = plt.Normalize(vmin=-s_max, vmax=s_max)
    cmap = plt.get_cmap('coolwarm')

    fig, ax = plt.subplots()
    for element, s in zip(ElementJoints, stress):
        node1 = element[0]
        node2 = element[1]
        ax.plot([NodePos2[node1][0], NodePos2[node2][0]],
                [NodePos2[node1][1], NodePos2[node2][1]],
                color=cmap(norm(s)), linewidth=3)

    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(sm, ax=ax, label='Stress [MPa] (tension +, compression -)')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_title('Deformed Truss Coloured by Stress')
    ax.grid()
    ax.axis('equal')

#def force_BC_formatter()

data = DataReader("verification3.csv")
FEM = FEModel(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
FEM.solve()
FEM.post_process()
Plotter(data[0], data[4],FEM.NodePos2)
StressPlotter(FEM.NodePos2, data[4], FEM.element_results['Stress [MPa]'].to_numpy())
plt.show()
#FEM = FEModel(DataReader("verification1.csv"))
# print(data)
