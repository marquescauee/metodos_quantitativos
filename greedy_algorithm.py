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


    #Algoritmo Guloso
    def greedy_maximal_independent_set(graph, max_iterations):
        best_solution = set()
        iterations = 0

        while iterations < max_iterations:
            current_solution = set()
            vertices = list(graph.keys())
            random.shuffle(vertices)

            for vertex in vertices:
                if all(neighbour not in current_solution for neighbour in graph[vertex]):
                    current_solution.add(vertex)

            if len(current_solution) > len(best_solution):
                best_solution = current_solution

            iterations += 1

        return best_solution

    #Número de iterações
    max_iterations = 1000

    solution = greedy_maximal_independent_set(graph, max_iterations)
    print(f"Best Solution for Instance {i} After {max_iterations} iterations: {len(solution)}. Vertices Selected: {solution} \n")