# -*- coding: utf-8 -*-

import numpy as np
from isomorphism import *
from matrices import *

k2 = np.array([[0, 1],
               [1, 0]])
k3 = np.array([[0, 1, 1],
               [1, 0, 1],
               [1, 1, 0]])

b3_2 = np.array([[0, 0, 0, 1, 1],
                 [0, 0, 0, 1, 1],
                 [0, 0, 0, 1, 1],
                 [1, 1, 1, 0, 0],
                 [1, 1, 1, 0, 0]])

# print(list_aut(k3))
# print(list_aut(b3_2))

# G e H grafos com mesma sequencia de grau mas não isomorfos:
G = np.array([[0, 0, 1, 0, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [1, 1, 0, 1, 0, 0],
              [0, 0, 1, 0, 1, 0],
              [0, 0, 0, 1, 0, 1],
              [0, 0, 0, 0, 1, 0]])

H = np.array([[0, 1, 0, 0, 0, 0],
              [1, 0, 1, 0, 1, 0],
              [0, 1, 0, 1, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0, 1],
              [0, 0, 0, 0, 1, 0]])

# vet_grauG=np.array(list(map(degree,G)))
# LG=laplacian(G)
# vet_grauH=np.array(list(map(degree,H)))
# LH=laplacian(H)
# print("vetor de grau d(G): ", vet_grauG)
# print("L(G):\n", LG)
# print("L*d(G): ", np.dot(LG,vet_grauG))
# print("vetor de grau d(H): ", vet_grauH)
# print("L(H):\n", LH)
# print("L*d(H): ",np.dot(LH,vet_grauH))

# testando função grafo de linha:

# print(edges(G))
# print(lineGraph(G))
# print(lineGraph(H))
# print(verify_iso(LineGraph(G),LineGraph(H)))
#
k4 = np.array([[0, 1, 1, 1],
               [1, 0, 1, 1],
               [1, 1, 0, 1],
               [1, 1, 1, 0]])
#
# lk4=lineGraph(k4)
# print(lk4)
# print(list_aut(lk4))
# print(len(list_aut(k4)))
# print(len(list_aut(lk4)))

# print(verify_homo(k4,k3))
print(chromatic_number(b3_2))
