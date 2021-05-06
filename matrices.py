# -*- coding: utf-8 -*-

import numpy as np
import isomorphism as iso

# Grau de um vértice
def degree(u):
    s = 0
    for i in u:
        s += i
    return s

def laplacian(G):
    # L=[]
    # for u in G:
    # L.append(list(map(lambda i: -i, u.copy())))
    L = (-1) * np.copy(G)
    for i in range(len(G)):
        L[i][i] = degree(G[i])
    return L

"""Gerando a matriz de adjacência do grafo de linha de um grafo G."""

# recebe duas tuplas com dois elementos, cada uma representando uma aresta, e retorna se elas são incidentes.
def incident(e, f):
    if e[0] in f or e[1] in f: return True
    return False

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
