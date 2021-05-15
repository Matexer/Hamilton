import random
from .Algo import Algo


class BruteForceAlgo(Algo):
    def __search(self, way):
        if self._is_cycle(way):
            return way

        last_node = way[-1]
        possible_nodes = self.graph_dict[last_node]
        possible_unvisited_nodes = set(possible_nodes) - set(way)
        cycle = False
        for node in possible_unvisited_nodes:
            if cycle:
                return cycle

            new_way = way + [node]
            if len(new_way) > self.num_of_nodes:
                return cycle

            cycle = self.__search(new_way)
        return cycle

    def find_cycle(self):
        way = [random.choice(tuple(self.nodes))]
        return self.__search(way)