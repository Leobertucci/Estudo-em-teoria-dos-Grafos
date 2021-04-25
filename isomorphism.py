# -*- coding: utf-8 -*-

import itertools
import numpy as np
import queue

"""
Optei inicialmente por usar matrizes de adjacência para representar grafos, pois como trabalharemos com
homomorfismos, acredito que teremos que verificar adjacência de vértices muitas vezes.
"""

"""A ideia de um algoritmo inicial é gerar todas as funções dos vértices de x nos vértices de y e verificar 
uma a uma se alguma delas é um homomorfismo. Começamos com uma função que gera todas as funções de um 
conjunto com n elementos {0,1,...,n-1} em um conjunto com m elementos {0,1,...,m-1}. Trataremos uma função f 
como uma lista com n elementos, onde o valor na posição i indica o valor de f(i)."""

# gera as m^n funções
def gen_func(n, m):
    funcoes = []
    mapsto = [0] * n
    while mapsto != [m - 1] * n:
        funcoes.append(tuple(mapsto.copy()))
        mapsto[n - 1] += 1
        for i in range(1, n):
            if mapsto[n - i] >= m:
                mapsto[n - i] = 0
                mapsto[n - i - 1] += 1
    funcoes.append(tuple(mapsto))
    return funcoes

"""Próximo passo: para cada função f de V(x) em V(y), verificar se f é homomorfismo. Para isso, vamos 
iterar nas arestas de x. Retorna o primeiro f que encontrar, ou False caso não encontre nenhum."""

# retorna uma lista com as arestas de X. Note que tratamos uma aresta como uma tupla, ordenada, para
# facilitar iteração nas arestas. Ao verificar se uma aresta uv pertence a edges(X), basta garantir que
# uv está em ordem crescente.
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

# ciclo em n vértices
def c(n):
    cn=np.zeros((n, n), dtype=int)
    for i in range(n):
        cn[i][i-1]=1
        cn[i][i-n+1]=1
    return cn

# grafo complementar
def complement(X):
    n = len(X)
    Y=np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1,n):
            Y[i][j]=(X[i][j]+1)%2
            Y[j][i]=(X[i][j]+1)%2
    return Y

# número cromático de X
def chromatic_number(X):
    n = 1
    while 1:
        if verify_homo(X, k(n)): return n
        n += 1

# verifica se X é um core comparando grupo de automorfismos com monoide de endomorfismos
def is_core(X):
    if list_aut(X)==list_homo(X,X) :return True
    return False

# encontra core de X
def find_core(X):
    if is_core(X): return X
    for i in range(len(X)):
        Y=np.delete(np.delete(X,i,0),i,1)
        if verify_homo(X,Y): return find_core(Y)

# busca em largura, retorna vetor de predecessor e de camada.
# funciona em grafos simples ou orientados
def bfs(X, s):
    n=len(X)
    camada=[-1]*n # ninguém explorado
    camada[s]=0
    pred=[-1]*n
    q=queue.Queue()
    q.put(s)
    while not q.empty():
        u=q.get()
        for v in range(n):
            if X[u][v]==1:
                if camada[v]==-1:
                    q.put(v)
                    camada[v]=camada[u]+1
                    pred[v]=u
    return pred,camada

# retorna o menor caminho entre dois vértices u e v em um grafo simples ou orientado X
# pode ser feito parando bfs quando achar caminho
def path(X,u,v):
    pred,camada=bfs(X,u)
    if camada[v]==-1: return False
    w=v
    p=[]
    while pred[w] != -1:
        p.append(w)
        w=pred[w]
    p.append(w)
    p.reverse()
    return p

# retorna bipartição de X ou falso. Adaptação do bfs, tempo polinomial. Fixado para funcionar em
# grafos desconexos
def is_bipartite(X):
    n = len(X)
    camada = [-1]*n  # ninguém explorado
    color = [-1]*n # ninguém colorido
    q = queue.Queue()
    while -1 in camada:     # enquanto alguém não explorado
        w=camada.index(-1)
        q.put(w)
        camada[w] = 0
        color[w] = 0
        while not q.empty():
            u = q.get()
            for v in range(n):
                if X[u][v] == 1:
                    if color[v]==color[u]: return False
                    if camada[v] == -1:
                        q.put(v)
                        camada[v] = camada[u] + 1
                        color[v] = (color[u]+1)%2
    A,B=[],[]
    for i in range(n):
        if color[i]: B.append(i)
        else: A.append(i)
    return A,B


# Adaptação algoritmo de fluxo máximo para encontrar emparelhamento máximo em um grafo bipartido.
def matching_bip(X):
    n=len(X)
    # primeiro encontrar bipartição:
    try:
        A,B = is_bipartite(X)
    except:
        print("X não é bipartido")
        return
    # orienta arestas de A para B:
    for u in B:
        X[u]*=(-1)
    # adiciona fonte e sorvedouro:
    fonte=np.array([0]*n)
    for u in A:
        fonte[u]=1
    X=np.vstack((X,fonte))
    X=np.hstack((X,np.transpose([(-1)*np.concatenate([fonte,[0]])])))
    sorv = np.array([0]*(n+1))
    for u in B:
        sorv[u] = -1
    X = np.vstack((X, sorv))
    X = np.hstack((X, np.transpose([(-1)*np.concatenate([sorv,[0]])])))
    # encontra caminho p da fonte para sorvedouro, atualiza M por meio de diferença simétrica com p e
    # altera direção do caminho p em X:
    M=[]
    p = path(X,n,n+1)
    while p:
        for i in range(1,len(p)):    #altera sentido de p em X
            X[p[i-1]][p[i]] *= -1
            X[p[i]][p[i-1]] *= -1
        p.pop(0)
        p.pop(len(p)-1)
        arestas_p=[]
        for i in range(1,len(p)):
            arestas_p.append({p[i-1],p[i]})
        for e in arestas_p:     #dif simétrica M e arestas_p
            if e in M: M.remove(e)
            else: M.append(e)
        p = path(X, n, n + 1)
    return M

#tamanho emparelhamento máximo de X bipartido
def ni(X):
    return len(matching_bip(X))

#tamanho 2-emparelhamento máximo de X. Ver 6.1.4 Lovász
def ni2(X):
    n=len(X)
    Y=np.zeros((2*n, 2*n), dtype=int)
    for (i,j) in edges(X):
        Y[2*i][2*j+1]=1
        Y[2*j+1][2*i]=1
        Y[2*i+1][2*j]=1
        Y[2*j][2*i+1]=1
    return ni(Y)

#verifica se X é 2-bicrítico
def is_2bicritic(X):
    n = len(X)
    for i in range(n):
        Y=np.delete(np.delete(X,i,0),i,1)
        if ni2(Y) != n-1:   # 2-emparelhamento máximo é perfeito?
            return False
    return True







