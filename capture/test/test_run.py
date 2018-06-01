#!/usr/bin/env python
# -*- coding: utf-8 -*-

import doit
import logging

from capture.run_doit import *
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
