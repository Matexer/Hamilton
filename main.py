import networkx as nx
import matplotlib.pyplot as plt
import time
from hamilton import *


class GraphPlot:
    def __init__(self, graph, cycle):
        if cycle:
            cycle.append(cycle[0])
            for i in range(len(cycle) - 1):
                u = cycle[i]
                v = cycle[i + 1]
                graph.edges[u, v]['color'] = "red"
        colors = [graph[u][v]['color'] for u, v in graph.edges]
        nx.draw(graph, edge_color=colors)


def is_valid_cycle(cycle, graph_dict):
    used_nodes = []
    for next_node, node in zip(cycle[1:], cycle):
        used_nodes.append(node)
        if next_node in used_nodes:
            print(f"{next_node} appears twice")
            return False
        possible_nodes = graph_dict[node]
        if next_node not in possible_nodes:
            return False
    return True


if __name__ == "__main__":
    NUM_OF_NODES = 24
    MIN_VERTEXES_PER_NODE = 2
    MAX_VERTEXES_PER_NODE = 2
    DIRECTED = False

    graph, graph_dict = GraphGenerator.get_graph(NUM_OF_NODES,
        MIN_VERTEXES_PER_NODE, MAX_VERTEXES_PER_NODE, directed=DIRECTED)

    brute_algo = BruteForceAlgo(graph_dict)

    start = time.time()
    cycle = brute_algo.find_cycle()
    stop = time.time()
    t = stop - start

    if cycle:
        print(f"Cykl znaleziony przez alg. zachłanny w {t} s")
    else:
        print(f"Brak cyklu potwierdzony przez alg. zachłanny w {t} s")

    genetic_algo = GeneticAlgo(graph_dict, num_of_seekers=10, max_replications=1000)

    start = time.time()
    cycle = genetic_algo.find_cycle()
    stop = time.time()
    t = stop - start

    if cycle:
        print(f"Cykl znaleziony przez alg. genetyczny w {t}s w {genetic_algo.replication_number} generacji")
    else:
        print(f"Brak cyklu potwierdzony przez alg. genetyczny w {t}s")

    GraphPlot(graph, cycle)

    plt.draw()
    # plt.savefig("Graph.png", format="PNG")
    plt.show()
