#!/usr/bin/env python
# -*- coding: utf-8 -*-

from capture.jobs import *


def spades(num_sub, output, type_r, mem, thread):  # more parameter later
    num = 1
    tasks = []
    while num <= num_sub:
        tasks.append(task_spades(
                               num, type_r, output, mem, thread
                               ))  # add args later
        num += 1
    run_tasks(tasks, ['run'])


def miniasm(num_sub, output, mem, thread, PARAMETER):
    tasks = []
    tasks.append(task_minimap2(num_sub, output, mem, thread, PARAMETER))
    task.append(task_miniasm(output, mem, thread, PARAMETER))
    """ PARAMETER can be a PATH to a parameter file or can be a preset
        number or a list of parameter Args
    """
    run_tasks(tasks, ['run'])
