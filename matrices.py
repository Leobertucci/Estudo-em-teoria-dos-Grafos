# -*- coding: utf-8 -*-

import numpy as np
import isomorphism as iso

# Grau de um vértice
def degree(u):
    s = 0
    for i in u:
        s += i
    return s

# Grau máximo de G
def maxDegree(G):
    return max(list(map(degree,G)))

# retorna a matriz Laplaciana de G
def laplacian(G):
    # L=[]
    # for u in G:
    # L.append(list(map(lambda i: -i, u.copy())))
    L = (-1) * np.copy(G)
    for i in range(len(G)):
        L[i][i] = degree(G[i])
    return L

# recebe duas tuplas com dois elementos, cada uma representando uma aresta, e retorna se elas são incidentes.
def incident(e, f):
    if e[0] in f or e[1] in f: return True
    return False

# retorna a matriz de adjacência do grafo de linha de G
def lineGraph(G):
    edgs = iso.edges(G)
    m = len(edgs)
    lineG = np.zeros((m, m), dtype=int)
    for i in range(m):
        for j in range(i + 1, m):
            if incident(edgs[i], edgs[j]):
                lineG[i][j] = 1
                lineG[j][i] = 1
    return lineG

# retorna grafo completo k_n ou bipartido completo k_nm
def k(n,m=None):
    if m==None:
        kn = np.ones((n, n), dtype=int)
        for i in range(n):
            kn[i][i] = 0
        return kn
    else:
        knm = np.zeros((n+m, n+m), dtype=int)
        for i in range(n):
            for j in range(n,n+m):
                knm[i][j]=1
                knm[j][i]=1
        return  knm

# ciclo em n vértices
def c(n):
    cn=np.zeros((n, n), dtype=int)
    for i in range(n):
        cn[i][i-1]=1
        cn[i][i-n+1]=1
    return cn

# caminho de comprimento n
def p(n):
    pn = np.zeros((n+1, n+1), dtype=int)
    pn[0][1]=1
    for i in range(1,n):
        pn[i][i-1] = 1
        pn[i][i+1] = 1
    pn[n][n-1]=1
    return pn

# grafo complementar
def complement(G):
    n = len(G)
    H=np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1,n):
            H[i][j]= (G[i][j] + 1) % 2
            H[j][i]= (G[i][j] + 1) % 2
    return H

# produto tensorial
def tensorProduct(G,H):
    n = len(G)
    m = len(H)
    GxH = np.zeros((n*m, n*m), dtype=int)
    for e in iso.edges(G):
        for f in iso.edges(H):
            GxH[e[0]*m+f[0]][e[1]*m+f[1]]=1
            GxH[e[1]*m+f[1]][e[0]*m+f[0]]=1
            GxH[e[0]*m+f[1]][e[1]*m+f[0]]=1
            GxH[e[1]*m+f[0]][e[0]*m+f[1]]=1
    return GxH

# grafo de aplicações G^H
def mapGraph(F,X):
    n=len(F)
    m=len(X)
    G = np.zeros((n**m,n**m),dtype=int)
    maps=iso.gen_func(m,n)
    for f in maps:
        for g in maps:
            edge = True
            # vejamos se f~g:
            for (i, j) in iso.edges(X):
                if F[f[i]][g[j]]==0 or F[f[j]][g[i]]==0:
                    edge=False
                    break
            if edge:
                G[maps.index(f)][maps.index(g)]=1
    return G

#Vetor de Lovász referente aos grafos conexos não isomorfos de k_1 até k_4
def lovasz_vector(G):
    G8=np.array([[0,1,0,0],
                 [1,0,1,1],
                 [0,1,0,1],
                 [0,1,1,0]])
    G9=np.array([[0,1,1,0],
                 [1,0,1,1],
                 [1,1,0,1],
                 [0,1,1,0]])
    return [len(iso.list_homo(k(1),G)),
            len(iso.list_homo(k(2),G)),
            len(iso.list_homo(p(2),G)),
            len(iso.list_homo(k(3),G)),
            len(iso.list_homo(p(3),G)),
            len(iso.list_homo(k(1,3),G)),
            len(iso.list_homo(c(4),G)),
            len(iso.list_homo(G8,G)),
            len(iso.list_homo(G9,G)),
            len(iso.list_homo(k(4),G))]



