#!/usr/bin/env python
# -*- coding: utf-8 -*-

from capture.run_doit import *


def spades(num_sub, output, type_r, mem, thread):  # more parameter later
    num = 1
    tasks = []
    while num <= num_sub:
        tasks.append(task_spades(
                               num, type_r, output, mem, thread
                               ))  # add args later
        num += 1
    run_tasks(tasks, ['run'])


# def overlap():
    # To do later
