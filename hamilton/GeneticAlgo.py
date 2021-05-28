import random
from .Algo import Algo


class GeneticAlgo:
    def __init__(self, graph_dict, num_of_seekers=10, max_replications=100):
        self.max_replications = max_replications
        self.seekers = [GeneticAlgo.Seeker([random.choice(tuple(graph_dict.keys()))], [], graph_dict)
                        for _ in range(num_of_seekers)]

        self.num_of_seekers = num_of_seekers
        self.replication_number = 0
        self.diary = []

    def make_log(self):
        scores = [len(seeker.way) for seeker in self.seekers]
        best_score = max(scores)
        log = f"{self.replication_number}|Seekers: {len(self.seekers)}| Best: {best_score}"
        self.diary.append(log)

    def manage_replication(self):
        self.replication_number += 1
        scores = [len(seeker.way) for seeker in self.seekers]
        total_score = sum(scores)
        seekers_num = [i for i in range(len(self.seekers))]
        law_to_replication = {i: (scores[i] / total_score) for i in seekers_num}
        new_seekers = []
        seekers_to_add = self.num_of_seekers
        for seeker_i, score in law_to_replication.items():
            if not seekers_to_add:
                break
            for _ in range(int(round(score * self.num_of_seekers, 0))):
                old_seeker = self.seekers[seeker_i]
                new_seeker = old_seeker.replicate()
                if new_seeker:
                    new_seekers.append(new_seeker)
                    seekers_to_add -= 1
                else:
                    break
        self.seekers = new_seekers

    def find_cycle(self):
        while self.replication_number <= self.max_replications:
            for seeker in self.seekers:
                seeker.search()
                if seeker.founded_cycle:
                    self.make_log()
                    return seeker.way

            self.manage_replication()
            self.make_log()
        return False

    class Seeker(Algo):
        def __init__(self, way, ancestor_way, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ancestor_way = ancestor_way
            self.way = way

            self.stuck = False
            self.founded_cycle = False

        def go_forward(self):
            current_node = self.way[-1]
            possible_nodes = self.graph_dict[current_node]
            possible_unvisited_nodes = set(possible_nodes) - set(self.way)
            if not possible_unvisited_nodes:
                self.stuck = True
                return

            if current_node in self.ancestor_way[:-1]:
                i = self.ancestor_way[:-1].index(current_node)
                preferred_next_node = self.ancestor_way[i + 1]
                if preferred_next_node in possible_unvisited_nodes:
                    self.way.append(preferred_next_node)
                    return

            self.way.append(random.choice(tuple(possible_unvisited_nodes)))

        def search(self):
            while not self.stuck:
                self.go_forward()

            if self._is_cycle(self.way):
                self.founded_cycle = True

        def replicate(self):
            visited_nodes_with_unvisited_alternatives = {}

            for i in range(len(self.way) - 1):
                node = self.way[i]
                visited_node = self.way[i+1]
                possible_nodes = set(self.graph_dict[node])
                possible_nodes.remove(visited_node)
                alternatives = possible_nodes
                unvisited_alternatives = alternatives - set(self.way)
                if unvisited_alternatives:
                    visited_nodes_with_unvisited_alternatives[node] = unvisited_alternatives

            if not visited_nodes_with_unvisited_alternatives:
                return False

            nodes_to_choose = list(visited_nodes_with_unvisited_alternatives.keys())
            while nodes_to_choose:
                node = random.choice(nodes_to_choose)
                nodes_to_choose.remove(node)

                alternatives = visited_nodes_with_unvisited_alternatives[node]
                i = self.way.index(node)

                old_way = self.way[:i + 1]
                ancestor_way = self.way[i+1:]
                unvisited_alternatives = alternatives - set(old_way)
                if not unvisited_alternatives:
                    continue

                old_way.append(random.choice(tuple(unvisited_alternatives)))
                way = old_way
                return GeneticAlgo.Seeker(way, ancestor_way, self.graph_dict)

            return False
