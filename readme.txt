This code solves displacements of truss structures

It requires an input csv file, that requires following inputs

NodePosX,NodePosY - individual node positions [float][mm]
NodeForceX,NodeForceY - applied forces on the node in X and Y direction [float][N]
BCX,BCY - node constraints in X and Y direction [Bool] (1 means constrained)
DisplacementX,DisplacementY - displacement of a node in X or Y [float][mm]
NodeConnectionA, NodeConnectionB - element connections between nodes [int]
ElementArea, ElementModulus - element cross-section area and Elastic ElementModulus [mm2], [MPa]

An example set-up can be seen in verification1.csv

It outputs the all element stresses and strains, as well as nodal displacements and reaction forces
It also shows 2 plots: 
    deformed versus initial structure (displacement multiplied by 20 for visual clarity)
    deformed structure with a stress heat map
