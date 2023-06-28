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
  
    #Algoritmo Semi-Greedy
    def semi_greedy(iterations, k):
        graph = build_graph_from_file(file_path)
        best_independent_set = set()
        best_independent_size = 0 
        sorted_candidates = sorted(graph.items(), key=lambda x: len(x[1]))
        sorted_candidates = dict(sorted_candidates)
        for _ in range(iterations):
            candidates = list(sorted_candidates)
            independent_set = set()
            while candidates:
                partial_candidates = int(len(candidates) * (k/100) + 1)
                candidates = candidates[:partial_candidates]

                chosen_vertice = random.choice(candidates)

                independent_set.add(chosen_vertice)
                candidates.remove(chosen_vertice)
                
                for neighbor in graph[chosen_vertice]:
                    if neighbor in candidates:
                        candidates.remove(neighbor) 
               

            independent_size = len(independent_set)
            if independent_size > best_independent_size:
                best_independent_set =  independent_set
                best_independent_size = independent_size
        return best_independent_set

    #Número de iterações
    max_iterations = 10000

    #Porcentagem de candidatos
    k = 100

    solution = semi_greedy(max_iterations, k)
    print(f"Best Solution for Instance {i} After {max_iterations} iterations: {len(solution)}. Vertices Selected: {solution} \n")
