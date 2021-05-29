import resource
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import sys
import tracemalloc
import time


class MemoryMonitor:
    def __init__(self):
        self.keep_measuring = True

    def measure_usage(self):
        mem_usage = []
        initial_mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        while self.keep_measuring:
            mem_usage.append(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - initial_mem_usage)
            sleep(0.01)

        return mem_usage

    def trace_mem(self):
        tracemalloc.start()
        mem_usage = []
        times = []
        initial_mem, _ = tracemalloc.get_traced_memory()
        initial_time = time.time()
        while self.keep_measuring:
            current, _ = tracemalloc.get_traced_memory()
            current -= (sys.getsizeof(mem_usage) + sys.getsizeof(times) + initial_mem)
            mem_usage.append(current)
            times.append((time.time() - initial_time))
            sleep(0.01)

        tracemalloc.stop()
        return mem_usage, times


class Ivy:
    def __init__(self, i):
        self.egg = [100000*i for i in range(i)]


def test_func():
    egg = []
    for i in range(10000):
        Ivy(i)
        # egg.append(Ivy(i))

    return egg


# def measure_usage():
#     with ThreadPoolExecutor() as executor:
#         monitor = MemoryMonitor()
#         mem_thread = executor.submit(monitor.measure_usage)
#         try:
#             fn_thread = executor.submit(test_func)
#             result = fn_thread.result()
#         finally:
#             monitor.keep_measuring = False
#             mem_usage = mem_thread.result()
#
#     time = [i/100 for i in range(len(mem_usage))]
#     plt.plot(time, mem_usage)
#     plt.show()


def measure_mem_usage(func):
    with ThreadPoolExecutor() as executor:
        monitor = MemoryMonitor()
        mem_thread = executor.submit(monitor.trace_mem)
        try:
            fn_thread = executor.submit(func)
            result = fn_thread.result()
        finally:
            monitor.keep_measuring = False
            mem_usage, times = mem_thread.result()

    mem_usage = [m/1024 for m in mem_usage]
    return mem_usage, times, result


if __name__ == "__main__":
    mem_usage, times, result = measure_mem_usage(test_func)
    plt.plot(times, mem_usage)
    plt.show()
