import os
import time
from multiprocessing import Process
from threading import Thread
from typing import Callable, NoReturn

from hw_1.src.fibs_ast_drawer.main import gen_fibs

FIBS_N = 10_000
FIBS_ITERATIONS = 10


def measure(callable_task: Callable[[], NoReturn], measure_name: str) -> str:
    start = time.time()
    callable_task()
    end = time.time()
    return f"{measure_name}: {end - start:.4f}s"


def write_to_file(filename: str, content: str) -> NoReturn:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        file.write(content)


def synchronous_task() -> NoReturn:
    for _ in range(FIBS_ITERATIONS):
        gen_fibs(FIBS_N)


def threads_task(threads_cnt: int) -> NoReturn:
    threads = [Thread(target=gen_fibs, args=(FIBS_N,)) for _ in range(threads_cnt)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def multiprocessing_task(processes_cnt: int) -> NoReturn:
    processes = [Process(target=gen_fibs, args=(FIBS_N,)) for _ in range(processes_cnt)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()


if __name__ == '__main__':
    tasks = [
        (synchronous_task, "synchronous"),
        (lambda: threads_task(FIBS_ITERATIONS), f"threading with {FIBS_ITERATIONS} threads"),
        (lambda: multiprocessing_task(FIBS_ITERATIONS), f"multiprocessing with {FIBS_ITERATIONS} processes")
    ]
    res = "\n".join(map(lambda task: measure(*task), tasks))

    title = f"Run gen_fibs({FIBS_N}) for {FIBS_ITERATIONS} iterations.\n\n"
    write_to_file("../artifacts/easy_fibs.txt", title + res)
