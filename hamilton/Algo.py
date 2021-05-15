class Algo:
    def __init__(self, graph_dict):
        self.nodes = graph_dict.keys()
        self.num_of_nodes = len(self.nodes)
        self.graph_dict = graph_dict

    def _is_cycle(self, way):
        if len(way) == self.num_of_nodes:
            first_node = way[0]
            last_node = way[-1]
            connections = self.graph_dict[last_node]
            if first_node in connections:
                return True
        return False
