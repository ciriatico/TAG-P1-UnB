# Nome: Gabriel Mendes Ciriatico Guimarães
# Número de matrícula: 202033202


# Referências externas:
## A ideia da construção de grafo por lista de adjacências a partir de dicionário e sets foi vista em artigo da Programiz ("Adjacency List (With Code in C, C++, Java and Python)") (disponível em: https://www.programiz.com/dsa/graph-adjacency-list).
## A montagem do grafo como tipo abstrato de dados, no entanto, foi feita com base no conteúdo e na lista mostrados na aula 3 do curso.

## O pseudo código utilizado para implementar o algoritmo de Bron-Kerbosh sem pivotamento está aqui: https://iq.opengenus.org/bron-kerbosch-algorithm/ (OpenGenus IQ, "Using Bron Kerbosch algorithm to find maximal cliques in O(3^(N/3))")
## Dessa mesma fonte (OpenGenus IQ) também foi utilizado parte do código em Python. A diferença está no fato de que escolhi usar as operações de set para implementar o pseudo-código (inter, union, difference).
## Isso permitiu uma tradução mais simples e direta do pseudo-código para o código.
## A única parte funcional do código do OpenGenus IQ que foi mantida foi a parte de impressão dos cliques maximais e contagem de cliques maximais.

## Para o código do algoritmo com pivotamente, foi utilizado o artigo de Brito e Santos (2011) (disponível em: http://www.din.uem.br/sbpo/sbpo2011/pdf/87964.pdf).
## No artigo, os autores abordam as diferentes formas de escolha de pivô. Para o trabalho, escolhi o pivotamento por grau máximo de nó.
## O pseudo-código foi facilmente traduzido em código em Python a partir do código do algoritmo sem pivotamento.

class Graph:
    # Grafo unidirecional e sem peso
    
    def __init__(self):
        # Estrutura escolhida é a lista de adjacências, implementada através de 1 dicionário que armazina sets
        # Cada vértice é uma chave do dicionário, possuindo um set de adjacentes
        self.graph = {}
    
    def insert_edge(self, v1, v2):
        # O código não trabalha com estrutura de nós, apenas de grafo, para poder usufruir da junção entre dicionário e sets
        # Assim, para adicionar uma aresta precisa primeiro adicionar os vértices da aresta no dicionário
        if v1 not in self.graph:
            self.graph[v1] = set()
        if v2 not in self.graph:
            self.graph[v2] = set()

        self.graph[v1].add(v2)
        self.graph[v2].add(v1)
    
    def edge_exists(self, v1, v2):
        return v2 in self.graph[v1]
    
    def get_nodes(self):
        return set(self.graph.keys())
    
    def adjacent_nodes(self, v):
        return self.graph[v]
    
    def remove_edge(self, v1, v2):
        self.graph[v1] = self.graph[v1].difference(v2)
        self.graph[v2] = self.graph[v2].difference(v1)
        
    def print_graph(self):
        # Imprimir o grafo como lista de adjacências
        for n in self.graph.keys():
            resultado = str(n) + ": "
            resultado += " -> ".join(list(self.graph[n]))
            print(resultado)

class Algorithms:
    
    def bron_kerbosh(graph_a, r, p, x):
        # Se os conjuntos de nós potenciais e de nós rejeitados estiverem vazios, então o conjunto r é um clique maximal        
        if ((len(p) == 0) or (p is None)) and (len(x) == 0):
            print(str(len(r)) + " vértices: ", sorted(list(r)))
            return 1

        cliques_maximais = 0

        # Para cada nó no conjunto de nós potenciais
        for i in p:
            new_p = p.intersection(graph_a[i])
            new_r = r.union({i})
            new_x = x.intersection(graph_a[i])

            # O algoritmo é aplicado de forma recursiva, retornando a quantidade de cliques maximais encontrados
            cliques_maximais += Algorithms.bron_kerbosh(graph_a, new_r, new_p, new_x)

            # Nós testados podem ser removidos do conjunto de potenciais e colocados no conjunto de nós rejeitados
            p = p.difference({i})
            x = x.union({i})

        return cliques_maximais
    
    def biggest_degree_node(graph_a, p):
        # Método que retorna o nó com maior grau em uma lista de adjacências
        n_max = 0

        for v in p:
            if len(graph_a[v]) > n_max:
                n_max = len(graph_a[v])
                bnode = v

        return bnode
    
    def bron_kerbosh_with_pivot(graph_a, r, p, x):   
        if ((len(p) == 0) or (p is None)) and (len(x) == 0):
            print(str(len(r)) + " vértices: ", sorted(list(r)))
            return 1

        cliques_maximais = 0

        # As 2 próximas linhas são a única mudança significativa com o código do algoritmo sem pivotamento
        # Na seguinte, escolhemos o pivô com maior grau em uma lista de adjacências (P U X)
        pivot = Algorithms.biggest_degree_node(graph_a, p.union(x))

        # Aqui, fazemos o loop para P \ N(pivot) ao invés de para P, reduzindo as recursões
        for i in p.difference(graph_a[pivot]):
            new_p = p.intersection(graph_a[i])
            new_r = r.union({i})
            new_x = x.intersection(graph_a[i])

            cliques_maximais += Algorithms.bron_kerbosh_with_pivot(graph_a, new_r, new_p, new_x)

            p = p.difference({i})
            x = x.union({i})

        return cliques_maximais
    
    def nodes_with_mutual_friends(graph_a, node_a):
        # Método que retorna a quantidade de nós que tem nós adjacentes em comum
        comuns = 0

        for vizinho in graph_a[node_a]:
            comuns += len(graph_a[vizinho].intersection(graph_a[node_a]))

        # Como as arestas são contadas 2 vezes, 1 em cada lista dos vértices de origem, sua contagem precisa ser dividida
        return comuns/2
    
    def local_clustering_coefficient(graph_a, node_a):
        # Cálculo do coeficiente de aglomeração local, como visto em aula
        k = len(graph_a[node_a])

        # Se o nó tem apenas 1 vizinho, não é possível que os vizinhos desse nó sejam vizinhos entre si (um nó não pode ser vizinho de si mesmo)
        if k <= 1:
            return 0

        n = Algorithms.nodes_with_mutual_friends(graph_a, node_a)

        return (2*n)/(k*(k-1))
    
    def average_clustering_coefficient(graph_a):
        # O coeficiente de aglomeração médio é a média dos coeficientes locais de aglomeração
        local_coefficients = 0

        for node in graph_a.keys():
            local = Algorithms.local_clustering_coefficient(graph_a, node)
            local_coefficients += local

        return local_coefficients/len(graph_a.keys())

def read_mtx_file(filename):
    # Leitura do arquivo .mtx fornecido, retornando as arestas em formato de lista de listas
    with open(filename) as f:
        content = f.readlines()
    
    content = [linha for linha in content if linha[0] != "%"]
    content = content[1:]
    
    content = [linha.strip("\n") for linha in content]
    content = [linha.split(" ") for linha in content]
    
    return content

def matrix_to_graph(M, G):
    # Preenchimento de grafo a partir da lista de arestas lida a partir do arquivo .mtx
    for edge in M:
        G.insert_edge(int(edge[0]), int(edge[1]))
    
    return G

p1 = read_mtx_file("soc-dolphins.mtx")

G = Graph()
G = matrix_to_graph(p1, G)

print("\nAplicando o algoritmo de Bron-Kerbosh, sem pivotamento:")

n_cliques_sem_pivot = Algorithms.bron_kerbosh(G.graph, set(), G.get_nodes(), set())
print("\n" + str(n_cliques_sem_pivot) + " cliques maximais encontrados.")
print("---------------------------------------")

print("\nAplicando o algoritmo de Bron-Kerbosh, com pivotamento:")
n_cliques_com_pivot = Algorithms.bron_kerbosh_with_pivot(G.graph, set(), G.get_nodes(), set())
print("\n" + str(n_cliques_com_pivot) + " cliques maximais encontrados.")
print("---------------------------------------")

acoef = Algorithms.average_clustering_coefficient(G.graph)
print("\nO coeficiente médio de aglomeração do grafo é: {0:.5}".format(acoef))