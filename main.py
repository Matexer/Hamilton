import networkx as nx
import matplotlib.pyplot as plt
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
    NUM_OF_NODES = 160
    MIN_VERTEXES_PER_NODE = 2
    MAX_VERTEXES_PER_NODE = 10
    DIRECTED = False

    graph, graph_dict = GraphGenerator.get_graph(NUM_OF_NODES,
        MIN_VERTEXES_PER_NODE, MAX_VERTEXES_PER_NODE, directed=DIRECTED)

    # brute_algo = BruteForceAlgo(graph_dict)
    # cycle = brute_algo.find_cycle()
    # if cycle:
    #     print(cycle)

    genetic_algo = GeneticAlgo(graph_dict, num_of_seekers=10, max_replications=10000)
    cycle = genetic_algo.find_cycle()
    print(f"Valid: {is_valid_cycle(cycle, graph_dict)}")
    print(genetic_algo.diary[-1])
    GraphPlot(graph, cycle)

    plt.draw()
    plt.show()
