# -*- coding: utf-8 -*-

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

grotzsch=np.array([[0,1,1,0,0,0,0,1,0,0,1],
                   [1,0,0,1,0,0,1,0,0,1,0],
                   [1,0,0,0,1,0,1,0,1,0,0],
                   [0,1,0,0,1,0,0,0,1,0,1],
                   [0,0,1,1,0,0,0,1,0,1,0],
                   [0,0,0,0,0,0,1,1,1,1,1],
                   [0,1,1,0,0,1,0,0,0,0,0],
                   [1,0,0,0,1,1,0,0,0,0,0],
                   [0,0,1,1,0,1,0,0,0,0,0],
                   [0,1,0,0,1,1,0,0,0,0,0],
                   [1,0,1,1,0,1,0,0,0,0,0]])
#
# lk4=lineGraph(k4)
# print(lk4)
# print(list_aut(lk4))
# print(len(list_aut(k4)))
# print(len(list_aut(lk4)))

# print(verify_homo(k4,k3))
# print(chromatic_number(b3_2))

# print(is_core(k(5)))
# v5=np.zeros((5, 5), dtype=int)
# print(len(list_aut(v5)))
# print(len(list_aut(k(5))))
# print(len(list_homo(v5,v5)))
# print(len(list_homo(k(5),k(5))))
# print(list_aut(grotzsch))

# print(len(list_aut(c(7))))
# print(len(list_homo(c(7),c(7))))
# print(len(list_aut(complement(c(7)))))
# print(len(list_homo(complement(c(7)),complement(c(7)))))
# print(is_core(complement(c(7))))
# print(is_core(c(9)))

# testando bfs e emparelhamento máximo

# print(path(c(7),0,4))
# print(bfs(c(5),2))
# print(is_bipartite(H))
# print(list(map(lambda x: -x,[3,4])))
# a=np.array([2,3])
# print((-1)*a)
# fonte=np.array([0]*6)
# print(np.concatenate([G,np.transpose([fonte])]))
# print(np.transpose([np.concatenate([fonte,np.array([0])])]))
# print(ni2(c(4)))
# print(matching_bip(c(6)))
# print(edges(c(7)))
print(is_2bicritic(c(17)))