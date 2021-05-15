import random
from abc import ABC
import networkx as nx
from collections import defaultdict


class GraphGenerator(ABC):
    @classmethod
    def __get_dict(cls, n, min_v, max_v, directed):
        graph_dict = defaultdict(list)
        nodes = [i for i in range(n)]
        for node in nodes:
            num_of_vertexes = random.randint(min_v, max_v)
            nodes_to_connect = nodes[:]
            nodes_to_connect.remove(node)
            for _ in range(num_of_vertexes):
                node_to_connect = random.choice(nodes_to_connect)
                nodes_to_connect.remove(node_to_connect)
                graph_dict[node].append(node_to_connect)

        if directed:
            return graph_dict

        for node in nodes:
            connected_nodes = graph_dict[node]
            for connected_node in connected_nodes:
                examined_node_connections = graph_dict[connected_node]
                if node not in examined_node_connections:
                    examined_node_connections.append(node)

        return graph_dict

    @staticmethod
    def get_graph(n, min_v, max_v, directed=True):
        assert (min_v > 0),\
            f"Dla MIN_VERTEXES_PER_NODE=0 graf może być niespójny."
        assert (max_v >= min_v),\
            "Minimalna liczba powiązań musi być mniejsza lub równa maksymalnej."
        assert (n > max(max_v, min_v)),\
            "Liczba powiązań nie może przekraczać liczby węzłów."

        graph_dict = GraphGenerator.__get_dict(n, min_v, max_v, directed)
        if directed:
            graph = nx.DiGraph()
        else:
            graph = nx.Graph()
        graph.add_nodes_from(graph_dict.keys())
        for node in graph_dict.keys():
            for connected_node in graph_dict[node]:
                graph.add_edge(node, connected_node, color='black')
        return graph, graph_dict
