import random

#Selecionando apenas as instâncias ímpares (step 2)
for i in range(1, 30, 2):

    #Função que gera o grafo
    def build_graph_from_file(file_path):
        graph = {}
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    vertex1, vertex2 = map(int, line.split())
                    if vertex1 not in graph:
                        graph[vertex1] = []
                    if vertex2 not in graph:
                        graph[vertex2] = []
                    graph[vertex1].append(vertex2)
                    graph[vertex2].append(vertex1)
        return graph

    file_path = './'+str(i)+'/result'+str(i)+'.txt'
    

    #Algoritmo Iterated Greedy
    def iterated_greedy(max_iterations, d):
        #variáveis que serão usadas para comparação no final da iteração
        best_independent_set = set()
        best_independent_size = 0
        
        graph = build_graph_from_file(file_path)

        #ordenando o grafo do vértice de menor ordem para o de maior
        #forma de ordenação: função lambda recebe um parâmetro x (chave/vértice do dicionário/grafo) e retorna o comprimento do array de valores
        sorted_candidates = sorted(graph.items(), key=lambda x: len(x[1]))

        #convertendo a lista ordenada para um grafo novamente
        sorted_candidates = dict(sorted_candidates)

        #inicio das iterações
        for _ in range(max_iterations):

            #necessário recriar o grafo a cada iteração, pois este é modificado com a destruição
            graph = build_graph_from_file(file_path)

            #cópia da lista ordenada de candidatos em forma de lista (necessário para não apontarem para o mesmo endereço de memória)
            candidates = list(sorted_candidates)

            #melhor conjunto independente máximo atual
            current_independent_set = set()

            #definição do número de vértices a serem destruídos
            vertices_to_be_destroyed = int(len(candidates) * (d/100) + 1)

            #iterando sobre cada vértice a ser destruído
            for i in range(vertices_to_be_destroyed):

                #pegando o vertice atual que está sendo iterado
                current_vertice = candidates[i]

                #iterando sobre os valores (vizinhos) a serem destruidos de cada chave (vértice) 
                for j in range(len(graph.get(current_vertice))):
                    
                    #seleciona um vértice aleatório do conjunto de candidatos
                    new_neighbor = random.choice(candidates)

                    #se o new_neighbor já é um vizinho ou se o new_neighbor é o próprio vértice que está sendo iterado, gera um novo new_neighbor 
                    while(new_neighbor in graph.get(candidates[i]) or new_neighbor == candidates[i]):
                        new_neighbor = random.choice(candidates)
                    
                    #vizinho que será removido
                    neighbor_to_be_removed = graph.get(candidates[i])[j]
                    
                    #destruição do vizinho antigo e atribuição de um novo vizinho
                    graph.get(candidates[i])[j] = new_neighbor
    
                    #adicionando vértice atual como vizinho do new_neighbor
                    graph[new_neighbor].append(current_vertice)

                    #remover vertice atual da vizinha de neighbor_to_be_removed
                    graph[neighbor_to_be_removed].remove(current_vertice)
    
            while candidates:
                    #enquanto houver candidatos, pega sempre o primeiro (de menor grau)
                    chosen_vertice = candidates[0]
    
                    #adiciona o vertice escolhido ao conjunto independente máximo atual
                    current_independent_set.add(chosen_vertice)

                    #remove o vértice escolhido do conjunto de candidatos
                    candidates.remove(chosen_vertice)
                    
                    #cada vizinho (valor) do vértice escolhido (chave) também é removido da lista de candidatos
                    for neighbor in graph[chosen_vertice]:
                        if neighbor in candidates:
                            candidates.remove(neighbor)

            #se o tamanho do conjunto independente máximo atual é maior que o melhor encontrado até o momento, substitui
            independent_size = len(current_independent_set)
            if independent_size > best_independent_size:
                best_independent_set =  current_independent_set
                best_independent_size = independent_size
        return best_independent_set

    #Número de iterações
    max_iterations = 1000

    #taxa de destruição
    d = 20

    #execução da solução
    solution = iterated_greedy(max_iterations, d)
    print(f"Best Solution for Instance {i} After {max_iterations} iterations: {len(solution)}. Vertices Selected: {solution} \n")