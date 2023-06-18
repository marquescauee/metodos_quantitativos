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

    #Algoritmo Semi-Guloso
    def semi_greedy(max_iterations):
        best_independent_set_size = 0

        for _ in range(max_iterations):
            best_independent_set = set()
            remaining_vertices = set(graph.keys())
            while remaining_vertices:
                max_deg = 0
                best_vertex = None
                for v in remaining_vertices:
                    degree = len(graph[v])
                    if degree > max_deg:
                        max_deg = degree
                        best_vertex = v
                best_independent_set.add(best_vertex)
                remaining_vertices.remove(best_vertex)
                remaining_vertices.difference_update(graph[best_vertex])

            if len(best_independent_set) > best_independent_set_size:
                best_independent_set_size = len(best_independent_set)
        return best_independent_set
    
    #Número de iterações
    max_iterations = 1000

    solution = semi_greedy(max_iterations)
    print(f"Best Solution for Instance {i} After {max_iterations} iterations: {len(solution)}. Vertices Selected: {solution} \n")