#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from capture.jobs import *


def spades(num_sub, output, type_r, mem, thread):
    """ Call the execution of all the SPAdes tasks
        Arguments:
            num_sub = the sum of all the spades run
            type_r =  the type of spades run to execute (paired-end, bam,...)
            output = the path to the output directory
            mem =  the memory available spades can use
            thread = the number of threads available spades can use
    """
    num = 1
    tasks = []
    while num <= num_sub:
        tasks.append(task_spades(
                               num, type_r, output, mem, thread
                               ))  # add args later
        num += 1
    run_tasks(tasks, ['run'])


def canu(output, mem, thread, genome_size):
    """ Call the execution of Canu
        Arguments:
            output =  the path to the output directory
            mem =  the memory available spades can use
            thread = the number of threads available spades can use
            genome_size = the size of the wanted genome
    """
    os.makedirs(f"{output}/temp/canu")
    tasks = []
    tasks.append(task_canu(output, mem, thread, genome_size))
    run_tasks(tasks, ['run'])
