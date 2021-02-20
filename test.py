#!/usr/bin/python

import queue
import threading
import time
import random

in_q = queue.Queue()
out_q = queue.Queue()

def worker():
    while True:
        x = in_q.get()
        if x is None:
            break
        do_stuff(x)
        in_q.task_done()

def do_stuff(x):
    out_q.put(x)


def main():
    threads = []
    thread_count = 3

    for x in range(0, thread_count):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for x in range(0,10):
        in_q.put(x)

    in_q.join()

    for _ in threads:
        in_q.put(None)

    for t in threads:
        t.join()

    results = list(out_q.queue)
    print(results)

if __name__ == '__main__':
    main()