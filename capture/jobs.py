#!/usr/bin/env python
# -*- coding: utf-8 -*-

import doit

from doit.doit_cmd import DoitMain
from doit.cmd_base import TaskLoader
from doit.task import clean_targets, dict_to_task

# def task_example():
#     return {
#         'actions': ['myscript'],
#         'file_dep': ['my_input_file'],
#         'targets': ['result_file'],
#     }


def run_tasks(tasks, args, config={'verbosity': 0}):
    '''Given a list of `Task` objects, a list of arguments,
    and a config dictionary, execute the tasks.
    Those task will be SPAdes and overlap layout
    '''

    if type(tasks) is not list:
        raise TypeError('tasks must be of type list.')

    class Loader(TaskLoader):
        @staticmethod
        def load_tasks(cmd, opt_values, pos_args):
            return tasks, config

    return DoitMain(Loader()).run(args)


def make_task(task_dict_func):
    '''Wrapper to decorate functions returning pydoit
    `Task` dictionaries and have them return pydoit `Task`
    objects
    '''
    def d_to_t(*args, **kwargs):
        ret_dict = task_dict_func(*args, **kwargs)
        return dict_to_task(ret_dict)
    return d_to_t


@make_task
def task_spades(num, type_r, output, mem, thread):

    if type_r == "pe":
        cmd = f"""spades.py -1 {output}/subsample_forward{num}.fastq \
        -2 {output}/subsample_reverse{num}.fastq -t {thread} -m {mem} \
        -o {output}/spades{num} """
        file_input1 = f"{output}/subsample_forward{num}.fastq"
        file_input2 = f"{output}/subsample_reverse{num}.fastq"
        output_dir = f"{output}/spades{num}"
        return {
                'name': f"spades {num}",
                'file_dep': [file_input1, file_input2],
                'targets': [output_dir],
                'actions': [cmd],
            }
    elif type_r == "uniq":
        cmd = f"""spades.py -s {output}/subsample_uniq{num}.fastq \
         -t {thread} -m {mem} -o {output}/spades{num} """
        file_input1 = f"{output}/subsample_uniq{num}.fastq"
        output_dir = f"{output}/spades{num}"
        return {
                'name': f"spades {num}",
                'file_dep': [file_input1],
                'targets': [output_dir],
                'actions': [cmd],
            }
    elif type_r == "bam":
        cmd = f"""spades.py --only-assembler --iontorrent \
        -s {output}/subsample_{num}.bam \
        -t {thread} -m {mem} -o {output}/spades{num}"""
        file_input1 = f"{output}/subsample_{num}.bam"
        output_dir = f"{output}/spades{num}"
        return {
                'name': f"spades {num}",
                'file_dep': [file_input1],
                'targets': [output_dir],
                'actions': [cmd],
            }
    elif type_r == "test":
        cmd = f"""spades.py -s  data/20_reads_R1.fastq\
         -t {thread} -m {mem} -o {output} """
        file_input1 = "data/20_reads_R1.fastq"
        output_dir = f"{output}"
        return {
                'name': f"spades {num}",
                'file_dep': [file_input1],
                'targets': [output_dir],
                'actions': [cmd],
            }


@make_task
def task_minimap2(num_sub, output, mem, thread, PARAMETER):
    cmd = f"""minimap2 -x ava-pb/ava-ont
        {contig1} {contig2}
        -I {mem} or -K {mem}/thread
        -X ????
        -t {thread}
        >A.paf/overlap.paf
        """
    contig1 = "merge_of_half_contig"
    contig2 = "merge_of_half_contig"
    output_dir = f"{output}/temp"
    if parameter_preset == 1:
        param1 = "gap of 10"
        para2 = "lengh of X"
    elif parameter_preset == 2:
        param1 = "gap of 100"
        para2 = "lengh of Y"

    """ Do we consider them always nanopore, Pacbio or do I add an option
        Can we use more than 2 files at once (sub1.fa sub2.fa sub3.fa)
    or do I merge all the different contig in 2 file (contig1 and contig2)
    or do I repeat the minimap for every contig we have (1-2 then A-3 then B-4
    OR 1-2then 3-4 then A-B)
        Do I use more specific parameters (ask for all of them in command line
    or config file) or do it ask for presets parameter or do I keep it default
        Care the thread use up to thread+1 when mapping (+1 is for I/O)
    so do i tell him arg.thread - 1 or just arg.threads
    """
    return {
            'name': "Minimap2",
            'file_dep': [contig1, contig2],
            'targets': [output_dir],
            'actions': [cmd],
        }


@make_task
def task_miniasm(output, mem, thread, PARAMETER):
    cmd = """
        miniasm overlap.paf
        """
    file_input1 = "overlap.paf"
    output_dir = f"{output}/temp"
    return {
            'name': "miniasm",
            'file_dep': [file_input1],
            'targets': [output_dir],
            'actions': [cmd],
        }

    """ What type of parameter do I do here too and if there is similar
    parameter do I use the previous one in her
        Since both program need installation do I Wrote a install script for
    minimap,miniasm and spades or do I just ask for their PATH or do I assume
    they are in the overall
    """
