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

    #Algoritmo Iterated Greedy
    def iterated_greedy(max_iterations):
        best_set = set()
        best_size = 0
        for _ in range(max_iterations):
            graph = build_graph_from_file(file_path)

            independent_set = set()
            vertices = set(graph.keys())
            while vertices:
                v = random.choice(tuple(vertices))
                independent_set.add(v)
                vertices.remove(v)
                vertices.difference_update(graph[v])

            independent_size = len(independent_set)
            if independent_size > best_size:
                best_set =  independent_set
                best_size = independent_size
        return best_set

    #Número de iterações
    max_iterations = 1000

    solution = iterated_greedy(max_iterations)
    print(f"Best Solution for Instance {i} After {max_iterations} iterations: {len(solution)}. Vertices Selected: {solution} \n")
