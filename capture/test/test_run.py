#!/usr/bin/env python
# -*- coding: utf-8 -*-

import doit
import logging

from capture.jobs import *
from doit.doit_cmd import DoitMain
from doit.cmd_base import TaskLoader
from doit.task import clean_targets, dict_to_task


def test_doit_spades():
    type_r = "test"
    output = "testing_spades"
    mem = 24
    thread = 6
    num = "test"
    tasks = []
    logger = logging.getLogger(__name__)
    tasks.append(task_spades(
                               num, type_r, output, mem, thread
                               ))  # add args later
    run_tasks(tasks, ['run'])


def test_doit_miniasm():
    output = "testing_miniasm"
    mem = 24
    thread = 6
    contig1 = "name_of_contig_test1"
    contig2 = "name_of_contig_test2"  # can be changed depending on the method
    PARAMETER = "preset1"
    tasks = []
    tasks.append(task_minimap2(num_sub, output, mem, thread, PARAMETER))
    task.append(task_miniasm(output, mem, thread, PARAMETER))
    run_tasks(tasks, ['run'])
    minimap = READ outfile.paf
    template_minimap = READ expected_template.paf
    assert minimap == template_minimap
    miniasm = READ outfile.gfa
    template_miniasm = READ expected_template.gfa
    assert miniasm == template_miniasm
