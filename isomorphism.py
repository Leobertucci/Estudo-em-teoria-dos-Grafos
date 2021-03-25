# -*- coding: utf-8 -*-

import itertools
import numpy as np

"""
Optei inicialmente por usar matrizes de adjacência para representar grafos, pois como trabalharemos com
homomorfismos, acredito que teremos que verificar adjacência de vértices muitas vezes.
"""

"""A ideia de um algoritmo inicial é gerar todas as funções dos vértices de x nos vértices de y e verificar 
uma a uma se alguma delas é um homomorfismo. Começamos com uma função que gera todas as funções de um 
conjunto com n elementos {0,1,...,n-1} em um conjunto com m elementos {0,1,...,m-1}. Trataremos uma função f 
como uma lista com n elementos, onde o valor na posição i indica o valor de f(i)."""

def gen_func(n, m):
    funcoes = []
    mapsto = [0] * n
    while mapsto != [m - 1] * n:
        funcoes.append(tuple(mapsto.copy()))
        # print(func,'\n')
        mapsto[n - 1] += 1
        for i in range(1, n):
            if mapsto[n - i] >= m:
                mapsto[n - i] = 0
                mapsto[n - i - 1] += 1
    funcoes.append(tuple(mapsto))
    return funcoes

"""Próximo passo: para cada função f de V(x) em V(y), verificar se f é homomorfismo. Para isso, vamos 
iterar nas arestas de x. Retorna o primeiro f que encontrar, ou False caso não encontre nenhum."""

def edges(X):
    edgs = []
    for i in range(len(X)):
        for j in range(i + 1, len(X)):
            if X[i][j]: edgs.append((i, j))
    return edgs

def verify_homo(X, Y):
    for f in gen_func(len(X), len(Y)):
        homo = True
        # vejamos se f é homomorfismo:
        for (i, j) in edges(X):
            if Y[f[i]][f[j]] == 0:
                homo = False
                break
        if homo: return f
    return False


"""Vamos construir agora um algoritmo ingênuo para verificar a existência isomorfismo. Não é necessário verificar 
todas as funções de um conjunto no outro desta vez, apenas as bijetivas. Para isso usaremos a função 
"permutations" da biblioteca itertools. Usamos também o seguinte resultado para simplificar o cálculo: 
Se x e y são isomorfos, então f de x em y é isomorfismo se e só se é um homomorfismo bijetivo.
"""

def invert(f):
    g = [0] * len(f)
    for i in range(len(f)):
        g[f[i]] = i
    return g

def verify_iso(X, Y):
    if len(X) != len(Y): return False
    for f in list(itertools.permutations(list(range(len(X))))):
        iso = True
        # vejamos se f é homomorfismo:
        for (i, j) in edges(X):
            if Y[f[i]][f[j]] == 0:
                iso = False
                break
        if iso:  # vejamos se f^-1 é homomorfismo:
            g = invert(f)
            for (i, j) in edges(Y):
                if X[g[i]][g[j]] == 0:
                    return False
        if iso: return f
    return False

# Listando todos os automorfismos de X
def list_aut(X):
    lista_auts = []
    for f in list(itertools.permutations(list(range(len(X))))):
        iso = True
        for (i, j) in edges(X):
            if X[f[i]][f[j]] == 0:
                iso = False
                break
        if iso:
            g = invert(f)
            for (i, j) in edges(X):
                if X[g[i]][g[j]] == 0:
                    iso = False
                    break
        if iso: lista_auts.append(f)
    return lista_auts

# Listando homomorfismos de X em Y
def list_homo(X, Y):
    lista_homo = []
    for f in gen_func(len(X), len(Y)):
        homo = True
        # vejamos se f é homomorfismo:
        for (i, j) in edges(X):
            if Y[f[i]][f[j]] == 0:
                homo = False
                break
        if homo: lista_homo.append(f)
    return lista_homo

# retorna grafo completo em n vértices
def k(n):
    kn = np.ones((n, n), dtype=int)
    for i in range(n):
        kn[i][i] = 0
    return kn

# número cromático de X
def chromatic_number(X):
    n = 1
    while 1:
        if verify_homo(X, k(n)): return n
        n += 1

#verifica se X é um core
def verify_core(X):
    if list_aut(X)==list_homo(X,X) :return True
    return False

#encontra core de X
def find_core(X):
    # list_core=[k(2),k(3)]
    if verify_core(X): return X
    for i in range(len(X)):
        Y=np.delete(np.delete(X,i,0),i,1)
        if verify_homo(X,Y): return find_core(Y)
