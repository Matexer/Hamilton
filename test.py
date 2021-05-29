import tracemalloc
import csv
import time
from typing import NamedTuple, Literal
from hamilton import GraphGenerator, BruteForceAlgo, GeneticAlgo
from main import GraphPlot
import matplotlib.pyplot as plt


class TestCase(NamedTuple):
    nodes: int
    min_vpn: int
    max_vpn: int
    directed: Literal[True, False]


def measure(func):
    tracemalloc.start()
    start = time.time_ns()
    result = func()
    _, pike = tracemalloc.get_traced_memory()
    stop = time.time_ns()
    tracemalloc.stop()
    t = (stop - start) / 1000_000
    return t, pike, result


def manage_test(algo, row):
    t, pike, result = measure(algo.find_cycle)
    row.append(t)
    row.append(pike)
    if result:
        row.append(1)
    else:
        row.append(0)
    return result


def save_graph_as_png(graph, result, n):
    GraphPlot(graph, result)
    plt.draw()
    plt.savefig(f"output/{n}n_graph.png", format="PNG")
    plt.close()


def test_case(case: TestCase, attempts=10):
    graph_drew = False
    graph, graph_dict = GraphGenerator.get_graph(case.nodes,
        case.min_vpn, case.max_vpn, directed=case.directed)
    rows = []

    for attempt in range(1, attempts+1):
        row = [case.nodes, attempt]
        genetic_algo = GeneticAlgo(graph_dict)
        result = manage_test(genetic_algo, row)
        if result and not graph_drew:
            save_graph_as_png(graph, result, case.nodes)
            graph_drew = True

        if case.nodes < 25:
            brute_algo = BruteForceAlgo(graph_dict)
            result = manage_test(brute_algo, row)
            if result and not graph_drew:
                save_graph_as_png(graph, result, case.nodes)
                graph_drew = True

        rows.append(row)
        if not graph_drew:
            save_graph_as_png(graph, False, case.nodes)
    return rows


if __name__ == "__main__":
    csvfile = open('output/output.csv', 'w', newline='')
    csv_writer = csv.writer(csvfile, delimiter='\t',
        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    header = "n", "Próba", "AG czas [ms]", "AG MP [kB]", "AG wynik", "AD czas [ms]", "AD MP [kB]", "AD wynik"
    csv_writer.writerow(header)

    cases = (13, 2, 2, False), (16, 2, 3, True), #(23, 4, 6, True), (24, 2, 4, False)
    test_cases = []
    for case in cases:
        test_cases.append(TestCase(*case))

    for i, case in enumerate(test_cases):
        output = test_case(case)
        csv_writer.writerows(output)
        print(f"Zakończono test dla n={case.nodes}")
        print(f"Przetestowano {i+1}/{len(test_cases)} przypadków")

    csvfile.close()
