import math
import random

for i in range(1, 27):
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

    def semi_greedy(k):

        best_independent_set = set()
        best_independent_size = 0 

        sorted_candidates = sorted(graph.items(), key=lambda x: len(x[1]))

        sorted_candidates = dict(sorted_candidates)

        candidates = list(sorted_candidates)

        current_independent_set = set()

        while candidates:       
            partial_candidates = int(math.ceil(len(candidates) * (k/100)))

            partial_list = list()

            for i in range (partial_candidates):
                partial_list.append(candidates[i])

            chosen_vertice = random.choice(partial_list)

            current_independent_set.add(chosen_vertice)

            candidates.remove(chosen_vertice)
        
            for neighbor in graph[chosen_vertice]:
                if neighbor in candidates:
                    candidates.remove(neighbor) 
            
        independent_size = len(current_independent_set)
        if independent_size > best_independent_size:
            best_independent_set =  current_independent_set
            best_independent_size = independent_size
        return best_independent_set
    
    def simple_local_search_random_improvement(initialSolution, max_iterations):
        #Solução Atual (Na primeira iteração, a melhor solução é a solução inicial gerada pelo semi-greedy)
        best_solution = list(initialSolution)
        number_of_iterations_used = 1

        for _ in range(max_iterations):
            #Lista de melhorias encontradas
            list_of_improvements = list()

            for i in range(len(best_solution)):

                #contador pra verificar se percorreu toda a vizinhança
                #exemplo: estou percorrendo a vizinha e ja consegui adicionar 2, mas ainda posso adicionar mais, então ainda não quero atualizar minha lista de melhoria. Só vou atualizar ela quando terminar de percorrer toda a vizinhança
                counter_neighbors = 0

                #Remove um vértice da solução atual 
                removed_vertice = best_solution[i]
                best_solution.remove(removed_vertice)

                #lista que conterá os vértices adicionados que melhoram a solução
                vertices_added_to_improve_solution = list()

                #Tenta adicionar vértices da lista de candidatos no conjunto atual
                for candidate in graph.get(removed_vertice):
                    counter_neighbors += 1

                    #Boolean para validar se o vértice pode ser adicionado no conjunto atual
                    can_be_added = True

                    #Boolean para validar se um vizinho já foi inserido anteriormente (fazemos isso para validar se o próximo candidato a ser inserido não é vizinho de um vértice que foi inserido anteriormente)
                    is_neighbor_of_candidate_added_before = False
                   
                    #Pega os vizinhos do candidato em potencial a ser inserido
                    neighbors_of_current_candidate = graph.get(candidate)

                    #Para cada vértice que está na melhor solução atual
                    for vertice in best_solution:
                        #Se o vértice é um vizinho do candidato, então não pode ser adicionado
                        if (vertice in neighbors_of_current_candidate):
                            can_be_added = False
                            break
                    if(can_be_added):
                        #valida se o candidato é vizinho de um vértice que foi adicionado anteriormente para melhorar a solução
                        for possible_neighbor in vertices_added_to_improve_solution:

                            #se o candidato inserido anteriormente é vizinho do candidato que to tentando inserir, então não pode
                            if possible_neighbor in neighbors_of_current_candidate or possible_neighbor == candidate:
                                is_neighbor_of_candidate_added_before = True
                                break 
                        if(is_neighbor_of_candidate_added_before):
                            continue

                        #se passar por essa duas validações, então o candidato não é vizinho de ninguém e pode ser adicionado no conjunto
                        vertices_added_to_improve_solution.append(candidate)

                        #se o tamanho da lista de vértices adicionados + o tamanho original da melhor solução for maior que o tamanho da solução original
                        #colocamos o +1 porque a melhor solução sempre tem um elemento removido para tentar inserir outros, logo uma solução inicial de 7 vértices chega neste ponto com somente 6

                    #EXEMPLO:
                        #best_solution começa valendo 7, mas chega aqui valendo 6, pois removemos um vértice para tentar adicionar mais
                        #se eu só consegui adicionar 1 vértice (len(vertices_added_to_improve_solution) = 1), então não muda nada, pois removi um vértice inicialmente e adicionei outro no lugar dele
                        #se eu consegui adicionar 2 ou mais vértices, então a solução parcial é melhor
                    if((len(vertices_added_to_improve_solution) + len(best_solution) > len(best_solution) + 1) and counter_neighbors == len(graph.get(removed_vertice))):
                        merged_list = vertices_added_to_improve_solution + best_solution
                            
                        #adiciona a merged_list (lista de vértices adicionados + lista da solução inicial) na lista de melhorias
                        list_of_improvements.append(merged_list.copy())

                #devolve o vértice removido à solução inicial para que comece uma nova iteração sobre o próximo vértice
                best_solution.insert(i, removed_vertice)

            #se houver alguma melhoria existente, pega uma melhoria aleatória
            if(list_of_improvements):
                number_of_iterations_used += 1
                best_solution = random.choice(list_of_improvements)
            else:
                return [best_solution, number_of_iterations_used] 
        return [best_solution, number_of_iterations_used]
  
    def grasp_simple_local_search(max_iterations, I):

        initial_max_iterations = max_iterations
        best_solution = list()
        l = 0

        while(l < max_iterations):
            
            semi_greedy_solution = semi_greedy(k)
                
            if(l == 0):
                best_solution = list(semi_greedy_solution)

            local_search_solution = simple_local_search_random_improvement(semi_greedy_solution, int(initial_max_iterations * (I/100)))

            if(len(local_search_solution[0]) > len(best_solution)):
                best_solution = local_search_solution[0]

            max_iterations -= local_search_solution[1]
            l += 1
        return best_solution

    #Gerando o Grafo
    file_path = './'+str(i)+'/result'+str(i)+'.txt'
    graph = build_graph_from_file(file_path)

    #Número de iterações
    max_iterations = 1000

    #Taxa de seleção de candidatos
    k = 10

    #Porcentagem de Iterações do algoritmo interno
    I = 10
    
    solution = grasp_simple_local_search(max_iterations, I)
    print(f"Best Solution for Instance {i} After {max_iterations} iterations: {len(solution)}. Vertices Selected: {solution} \n")