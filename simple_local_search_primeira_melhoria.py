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
    
    def simple_local_search(max_iterations):
        #variáveis que serão usadas para comparação no final da iteração
        best_independent_set = set()
        best_independent_size = 0
        
        graph = build_graph_from_file(file_path)

        #inicio das iterações
        for _ in range(max_iterations):

            #lista de candidatos
            candidates = list(graph.keys())
            
            #melhor conjunto independente máximo atual
            current_independent_set = set()

            while candidates:
                #vértice inicial selecionado aleatoriamente
                current_vertice = random.choice(candidates)

                #ordem do vértice atual (número de vizinhos)
                current_vertice_length = len(graph.get(current_vertice))

                #limitador de iterações dentro dos vizinhos do vértice atual (caso não encontre vizinho de ordem menor)
                iterations_inside_neighbors_limit = 0

                #posicao do vizinho
                neighbor_position = 0

                while(iterations_inside_neighbors_limit < current_vertice_length):

                    #pega o próximo vizinho (em ordem de 0 a tamanho do vértice atual)
                    neighbor = graph.get(current_vertice)[neighbor_position]

                    #ordem do vizinho
                    neighbor_length = len(graph.get(neighbor))

                    #se a ordem do vizinho é menor que a do vértice atual e se o vizinho for um candidato, substitui o vértice atual e começa a percorrer os vizinhos do novo vértice a partir do primeiro
                    if(neighbor_length < current_vertice_length and neighbor in candidates):
                        current_vertice = neighbor
                        current_vertice_length = neighbor_length
                        iterations_inside_neighbors_limit = 0
                        neighbor_position = 0

                    iterations_inside_neighbors_limit += 1
                    neighbor_position += 1

                #adiciona o vertice escolhido ao conjunto independente máximo atual
                current_independent_set.add(current_vertice)

                #remove o vértice escolhido do conjunto de candidatos
                candidates.remove(current_vertice)
                
                #cada vizinho (valor) do vértice escolhido (chave) também é removido da lista de candidatos
                for neighbor in graph[current_vertice]:
                    if neighbor in candidates:
                        candidates.remove(neighbor)
                        
            #se o tamanho do conjunto independente máximo atual é maior que o melhor encontrado até o momento, substitui
            independent_size = len(current_independent_set)
            if independent_size > best_independent_size:
                best_independent_set =  current_independent_set
                best_independent_size = independent_size
        return best_independent_set
            

    #Número de iterações
    max_iterations = 2000

    #execução da solução
    solution = simple_local_search(max_iterations)
    print(f"Best Solution for Instance {i} After {max_iterations} iterations: {len(solution)}. Vertices Selected: {solution} \n")