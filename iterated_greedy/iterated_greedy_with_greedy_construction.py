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
    
    def iterated_greedy(max_iterations, d):
        #variáveis que serão usadas para comparação no final da iteração
        best_independent_set = set()
        best_independent_size = 0

        #INÍCIO DA CONSTRUÇÃO DA SOLUÇÃO INICIAL (ALGORITMO GULOSO)
        independent_set = set()
        vertices = sorted(graph.items(), key=lambda x: len(x[1]))
        vertices = dict(vertices)
        vertices = list(vertices)

        while vertices:
            v = vertices[0]

            independent_set.add(v)
            vertices.remove(v)
            
            for value in graph[v]:
                if value in vertices:
                    vertices.remove(value) 

        best_independent_set = independent_set
        best_independent_size = len(independent_set)
        #FIM DA CONSTRUÇÃO INICIAL

        #ordenando o grafo do vértice de menor ordem para o de maior
        #forma de ordenação: função lambda recebe um parâmetro x (chave/vértice do dicionário/grafo) e retorna o comprimento do array de valores
        sorted_candidates = sorted(graph.items(), key=lambda x: len(x[1]))

        #convertendo a lista ordenada para um dicionário novamente
        sorted_candidates = dict(sorted_candidates)

        #melhor conjunto independente máximo atual
        current_independent_set = best_independent_set
        
        #inicio das iterações
        for _ in range(max_iterations):

            #cópia da lista ordenada de candidatos em forma de lista (necessário para não apontarem para o mesmo endereço de memória)
            candidates = list(sorted_candidates)

            #definição do número de vértices a serem destruídos
            vertices_to_be_destroyed = int(len(current_independent_set) * (d/100) + 1)

            #convertendo set pra uma lista
            current_independent_set = list(current_independent_set)

            #vertices removidos
            vertices_removed = list()

            #FASE DE DESTRUIÇÃO
            for _ in range(vertices_to_be_destroyed):
                #obtendo vértice a ser removido
                vertice_removed = random.choice(current_independent_set)

                #removendo do conjunto independente atual
                current_independent_set.remove(vertice_removed)

                #adicionando na lista de removidos
                vertices_removed.append(vertice_removed)

            #FASE DE CONSTRUÇÃO
            for candidate in candidates:
                #booleano pra verificar se o candidato é vizinho de alguém
                is_neighbor = False
                #candidato não pode estar no conjunto independente atual e não pode estar na lista de removidos (não queremos reinserir um vértice que acabou de ser removido)
                if(candidate not in current_independent_set and candidate not in vertices_removed):
                    #pra cada vértice no conjunto independente atual
                    for vertice in current_independent_set:
                        #pega todos os vizinhos do vértice da iteração
                        vertice_neighbors = graph.get(vertice)
                        #se o candidato for vizinho de alguém, então não adiciona no conjunto independente atual
                        if(candidate in vertice_neighbors):
                            is_neighbor = True
                            break
                    #se a variável is_neighbor for false, então o candidato não é vizinho de ninguém. Adiciona no conjunto
                    if(not is_neighbor):
                        current_independent_set.append(candidate)

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