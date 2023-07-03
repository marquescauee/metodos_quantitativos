import math
import random

#Selecionando apenas as instâncias ímpares (step 2)
for i in range(1, 30):
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

    def semi_greedy(I, k):

        best_independent_set = set()
        best_independent_size = 0 

        sorted_candidates = sorted(graph.items(), key=lambda x: len(x[1]))

        sorted_candidates = dict(sorted_candidates)

        for _ in range(I):

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
    
    def partial_destruction(semi_greedy_solution, D):

        semi_greedy_solution = list(semi_greedy_solution)

        for _ in range(math.ceil(int(len(semi_greedy_solution) * (D/100)))):
            semi_greedy_solution.remove(random.choice(semi_greedy_solution))
        
        return semi_greedy_solution
    
    def rebuilding_semi_greedy(solution_partial_destruction, I):
        for _ in range (I):
            list_of_candidates = list(graph.keys())

            while list_of_candidates:
                    candidate = random.choice(list_of_candidates)
                    is_neighbor = False
                    if(candidate not in solution_partial_destruction):
                        for vertice in solution_partial_destruction:
                            vertice_neighbors = graph.get(vertice)
                            if(candidate in vertice_neighbors):
                                is_neighbor = True
                                break
                        if(not is_neighbor):
                            solution_partial_destruction.append(candidate)
                    list_of_candidates.remove(candidate)
        return solution_partial_destruction

    def grasp_iterated_greedy(max_iterations, I):

        initial_max_iterations = max_iterations
        best_solution = list()
        l = 0

        while(l < max_iterations):
            
            semi_greedy_solution = semi_greedy(int(max_iterations * (I/100)), k)
                
            if(l == 0):
                best_solution = list(semi_greedy_solution)

            solution_partial_destruction = partial_destruction(semi_greedy_solution, D)

            solution_rebuilding_semi_greedy = rebuilding_semi_greedy(solution_partial_destruction, int(max_iterations * (I/100)))
        
            if(len(solution_rebuilding_semi_greedy) > len(best_solution)):
                best_solution = solution_rebuilding_semi_greedy

            max_iterations -= int(initial_max_iterations * (I/100))
            l += 1
        return best_solution

    #Gerando o Grafo
    file_path = './'+str(i)+'/result'+str(i)+'.txt'
    graph = build_graph_from_file(file_path)

    #Número de iterações
    max_iterations = 1000

    #Taxa de seleção de candidatos
    k = 20

    #Taxa de perturbação
    perturbation = 20

    #Taxa de destruição
    D = 50

    #Porcentagem de Iterações do algoritmo interno
    I = 10

    solution = grasp_iterated_greedy(max_iterations, I)
    print(f"Best Solution for Instance {i} After {max_iterations} iterations: {len(solution)}. Vertices Selected: {solution} \n")
