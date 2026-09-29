import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from solver import solve_truss
from k_local import element_length
from assemble_global_K import assemble_global_K


#for now no clue how to utilize classes prolerly

class FEModel:

    def __init__(self, NodePos, NodeForces, BC, displacements, ElementJoints, E, A):
        self.NodePos= NodePos
        print("NodePos:", NodePos)
        self.NodeForces = NodeForces
        print("NodeForces:", NodeForces)
        self.BC = BC
        self.displacements = displacements
        self.Element = ElementJoints
        print("ElementJoints:", ElementJoints)
        self.E = E
        self.A = A
    
    def solve(self):
        self.K = assemble_global_K(self.E, self.A, self.NodePos, self.Element)
        self.u = solve_truss(self.K, self.NodeForces, self.BC)
    
    #def post_process(self):
    

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

    print(ElementJoints)
    
    for element in ElementJoints:
        node1 = element[0]
        node2 = element[1]
        x_values = [NodePos[node1][0], NodePos[node2][0]]
        y_values = [NodePos[node1][1], NodePos[node2][1]]
        plt.plot(x_values, y_values, 'b-o')

    if NodePos2 is not None:
        for element in ElementJoints:
            node1 = element[0]
            node2 = element[1]
            x_values = [NodePos2[node1][0], NodePos2[node2][0]]
            y_values = [NodePos2[node1][1], NodePos2[node2][1]]
            plt.plot(x_values, y_values, 'r--')

    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Truss Structure')
    plt.grid()
    plt.axis('equal')
    plt.show()

#def force_BC_formatter()

data = DataReader("verification3.csv")
FEM = FEModel(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
FEM.solve()
Plotter(data[0], data[4])
#FEM = FEModel(DataReader("verification1.csv"))
print(data)
