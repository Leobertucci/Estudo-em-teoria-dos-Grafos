# -*- coding: utf-8 -*-

import itertools
import numpy as np
import queue

"""
Optei inicialmente por usar matrizes de adjacência para representar grafos, pois como trabalharemos com
homomorfismos, acredito que teremos que verificar adjacência de vértices muitas vezes.
"""

"""A ideia de um algoritmo inicial é gerar todas as funções dos vértices de G nos vértices de H e verificar 
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

"""Próximo passo: para cada função f de V(G) em V(H), verificar se f é homomorfismo. Para isso, vamos 
iterar nas arestas de x. Retorna o primeiro f que encontrar, ou False caso não encontre nenhum."""

# retorna uma lista com as arestas de G. Note que tratamos uma aresta como uma tupla, ordenada, para facilitar
# iteração nas arestas. Ao verificar se uma aresta uv pertence a edges(G), basta garantir que uv está em ordem crescente.
def edges(G):
    edgs = []
    for i in range(len(G)):
        for j in range(i + 1, len(G)):
            if G[i][j]: edgs.append((i, j))
    return edgs

def verify_homo(G, H):
    for f in gen_func(len(G), len(H)):
        homo = True
        # vejamos se f é homomorfismo:
        for (i, j) in edges(G):
            if H[f[i]][f[j]] == 0:
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

def verify_iso(G, H):
    if len(G) != len(H): return False
    for f in list(itertools.permutations(list(range(len(G))))):
        iso = True
        # vejamos se f é homomorfismo:
        for (i, j) in edges(G):
            if H[f[i]][f[j]] == 0:
                iso = False
                break
        if iso:  # vejamos se f^-1 é homomorfismo:
            g = invert(f)
            for (i, j) in edges(H):
                if G[g[i]][g[j]] == 0:
                    return False
        if iso: return f
    return False

# Listando todos os automorfismos de G
def list_aut(G):
    lista_auts = []
    for f in list(itertools.permutations(list(range(len(G))))):
        iso = True
        for (i, j) in edges(G):
            if G[f[i]][f[j]] == 0:
                iso = False
                break
        if iso:
            g = invert(f)
            for (i, j) in edges(G):
                if G[g[i]][g[j]] == 0:
                    iso = False
                    break
        if iso: lista_auts.append(f)
    return lista_auts

# Listando homomorfismos de G em H
def list_homo(G, H):
    lista_homo = []
    for f in gen_func(len(G), len(H)):
        homo = True
        # vejamos se f é homomorfismo:
        for (i, j) in edges(G):
            if H[f[i]][f[j]] == 0:
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
def complement(G):
    n = len(G)
    H=np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1,n):
            H[i][j]= (G[i][j] + 1) % 2
            H[j][i]= (G[i][j] + 1) % 2
    return H

# número cromático de G
def chromatic_number(G):
    n = 1
    while 1:
        if verify_homo(G, k(n)): return n
        n += 1

# verifica se G é um core comparando grupo de automorfismos com monoide de endomorfismos
def is_core(G):
    if list_aut(G)==list_homo(G, G) :return True
    return False

# encontra core de G
def find_core(G):
    if is_core(G): return G
    for i in range(len(G)):
        Y=np.delete(np.delete(G, i, 0), i, 1)
        if verify_homo(G, Y): return find_core(Y)

# busca em largura, retorna vetor de predecessor e de camada. Funciona em grafos simples ou orientados
def bfs(G, s):
    n=len(G)
    camada=[-1]*n # ninguém explorado
    camada[s]=0
    pred=[-1]*n
    q=queue.Queue()
    q.put(s)
    while not q.empty():
        u=q.get()
        for v in range(n):
            if G[u][v]==1:
                if camada[v]==-1:
                    q.put(v)
                    camada[v]=camada[u]+1
                    pred[v]=u
    return pred,camada

# retorna o menor caminho entre dois vértices u e v em um grafo simples ou orientado G pode ser feito parando bfs quando achar caminho
def path(G, u, v):
    pred,camada=bfs(G, u)
    if camada[v]==-1: return False
    w=v
    p=[]
    while pred[w] != -1:
        p.append(w)
        w=pred[w]
    p.append(w)
    p.reverse()
    return p

# retorna bipartição de G ou falso. Adaptação do bfs, tempo polinomial. Fixado para funcionar em grafos desconexos
def is_bipartite(G):
    n = len(G)
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
                if G[u][v] == 1:
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
def matching_bip(G):
    n=len(G)
    # primeiro encontrar bipartição:
    try:
        A,B = is_bipartite(G)
    except:
        print("G não é bipartido")
        return
    # orienta arestas de A para B:
    for u in B:
        G[u]*=(-1)
    # adiciona fonte e sorvedouro:
    fonte=np.array([0]*n)
    for u in A:
        fonte[u]=1
    G=np.concatenate((G, [fonte]))
    G=np.concatenate((G, np.transpose([(-1) * np.concatenate([fonte, [0]])])),1)
    sorv = np.array([0]*(n+1))
    for u in B:
        sorv[u] = -1
    G = np.concatenate((G, [sorv]))
    G = np.concatenate((G, np.transpose([(-1) * np.concatenate([sorv, [0]])])),1)
    # encontra caminho p da fonte para sorvedouro, atualiza M por meio de diferença simétrica com p e
    # altera direção do caminho p em G:
    M=[]
    p = path(G, n, n + 1)
    while p:
        for i in range(1,len(p)):    #altera sentido de p em G
            G[p[i - 1]][p[i]] *= -1
            G[p[i]][p[i - 1]] *= -1
        p.pop(0)
        p.pop(len(p)-1)
        arestas_p=[]
        for i in range(1,len(p)):
            arestas_p.append({p[i-1],p[i]})
        for e in arestas_p:     #dif simétrica M e arestas_p
            if e in M: M.remove(e)
            else: M.append(e)
        p = path(G, n, n + 1)
    return M

#tamanho emparelhamento máximo de G bipartido
def ni(G):
    return len(matching_bip(G))

#tamanho 2-emparelhamento máximo de G. Ver 6.1.4 Lovász
def ni2(G):
    n=len(G)
    Y=np.zeros((2*n, 2*n), dtype=int)
    for (i,j) in edges(G):
        Y[2*i][2*j+1]=1
        Y[2*j+1][2*i]=1
        Y[2*i+1][2*j]=1
        Y[2*j][2*i+1]=1
    return ni(Y)

#verifica se G é 2-bicrítico
def is_2bicritic(G):
    n = len(G)
    for i in range(n):
        Y=np.delete(np.delete(G, i, 0), i, 1)
        if ni2(Y) != n-1:   # 2-emparelhamento máximo é perfeito?
            return False
    return True







