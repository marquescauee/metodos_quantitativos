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

    file_path = './'+str(i)+'/result'+str(i)+'.txt'
    graph = build_graph_from_file(file_path)

  
    #Algoritmo Greedy
    def iterated_greedy(iterations):
        graph = build_graph_from_file(file_path)
        best_set = set()
        best_size = 0
        for _ in range(iterations):
            independent_set = set()
            vertices = sorted(graph, key = graph.get)
            while vertices:
                v = vertices[0] 
                #guloso: pega sempre o vértice do índice 0 (menor grau) (vertices ordenado pelo grau [não decrescente])
                #semi-guloso: pega aleatoriamente um dos vértices entre os índices 0 e ceil(k*n/100) - 1

                independent_set.add(v)
                vertices.remove(v)
                
                for value in graph[v]:
                    if value in vertices:
                        vertices.remove(value) 
                graph.pop(v)

            independent_size = len(independent_set)
            if independent_size > best_size:
                best_set =  independent_set
                best_size = independent_size
        return best_set

    #Número de iterações
    max_iterations = 10000

    solution = iterated_greedy(max_iterations)
    print(f"Best Solution for Instance {i} After {max_iterations} iterations: {len(solution)}. Vertices Selected: {solution} \n")
