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
    graph = build_graph_from_file(file_path)
  
    #Algoritmo Semi-Greedy
    def semi_greedy(iterations, k):
        #variáveis que serão usadas para comparação no final da iteração
        best_independent_set = set()
        best_independent_size = 0 

        #ordenando o grafo do vértice de menor ordem para o de maior
        #forma de ordenação: função lambda recebe um parâmetro x (chave/vértice do dicionário/grafo) e retorna o comprimento do array de valores
        sorted_candidates = sorted(graph.items(), key=lambda x: len(x[1]))

        #convertendo a lista ordenada para um grafo novamente
        sorted_candidates = dict(sorted_candidates)

        #inicio das iterações
        for _ in range(iterations):
            #cópia da lista ordenada de candidatos em forma de lista (necessário para não apontarem para o mesmo endereço de memória)
            candidates = list(sorted_candidates)

            #melhor conjunto independente máximo atual
            current_independent_set = set()

            #enquanto houver candidatos, seleciona o de menor grau para compor o conjunto independente máximo
            while candidates:       
                #definição da quantidade de candidatos a serem reatribuídos na lista
                partial_candidates = int(len(candidates) * (k/100) + 1)

                partial_list = list()

                for i in range (partial_candidates):
                   partial_list.append(candidates[i])

                #candidates = candidates[:partial_candidates]

                #seleção aleatória do percentual de candidatos
                chosen_vertice = random.choice(partial_list)

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

    #Porcentagem de candidatos
    k = 20

    solution = semi_greedy(max_iterations, k)
    print(f"Best Solution for Instance {i} After {max_iterations} iterations: {len(solution)}. Vertices Selected: {solution} \n")
