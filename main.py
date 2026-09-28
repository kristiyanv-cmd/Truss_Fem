import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import solver
import k_local
import assemble_global_K
import transformation_matrix
'''
for now no clue how to utilize classes prolerly

class FEModel:

    def __init__(self, NodePos, NodeForces, BC, displacements, ElementJoints, E, A):
        self.NodePos= NodePos
        self.NodeForces = NodeForces
        self.BC = BC
        self.displacements = displacements
        self.Element = ElementJoints
        self.E = E
        self.A = A
'''
'''
FEM = FEModel(NodePos, NodeForces, BC, displacements, elementJoints, E, A)
'''
def DataReader(filename):
    #reads the data from a CSV file. Drops missing values, forces int for indices.
    #returns (n,2) note, force, boundary condition, displacement and element joint arrays
    #returns (n,) arrays for element modulus and area
    df = pd.read_csv(filename)
    NodePos = df[['NodePosX', 'NodePosY']].dropna().to_numpy()
    NodeForces = df[['NodeForceX', 'NodeForceY']].dropna().to_numpy()
    BC = df[['BCX', 'BCY']].dropna().to_numpy()
    displacements = df[['DisplacementX', 'DisplacementY']].dropna().to_numpy()
    ElementJoints = df[['NodeConnectionA', 'NodeConnectionB']].dropna().astype(int).to_numpy()
    E = df['ElementModulus'].dropna().to_numpy()
    A = df['ElementArea'].dropna().to_numpy()

    return NodePos, NodeForces, BC, displacements, ElementJoints, E, A

def Plotter(NodePos, ElementJoints):
    print(ElementJoints)
    for element in ElementJoints:
        node1 = element[0]
        node2 = element[1]
        x_values = [NodePos[node1-1][0], NodePos[node2-1][0]]
        y_values = [NodePos[node1-1][1], NodePos[node2-1][1]]
        plt.plot(x_values, y_values, 'b-o')

    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Truss Structure')
    plt.grid()
    plt.axis('equal')
    plt.show()

data = DataReader("verification1.csv")
Plotter(data[0], data[4])
#FEM = FEModel(DataReader("verification1.csv"))
print(data)
