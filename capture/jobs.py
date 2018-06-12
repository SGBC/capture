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
def task_minimap2(num_sub, output, mem, thread):
    contig_dir = f"{output}/temp"
    output_dir = f"{output}/temp/minimap2"
    contig1 = f"{contig_dir}/all_contigs.fasta"
    memory_per_thread = mem // thread
    cmd = f"""minimap2 \
        {contig1} {contig1}\
        -K {memory_per_thread} \
        -t {thread} \
        |gzip -1 > {output_dir}/overlap.paf.gz"""
    """
        TO DO: add possibility to give a configuration file
        !!!!! Care the thread use up to thread+1 when mapping (+1 is for I/O)
    so do i tell him (arg.thread - 1) or just (arg.threads)
    """
    return {
            'name': "Minimap2",
            'file_dep': [contig1],
            'targets': [output_dir],
            'actions': [cmd],
            'uptodate': [False],
        }


@make_task
def task_miniasm(output, mem, thread):
    file_input1 = f"{output}/temp/minimap2/overlap.paf.gz"
    file_input2 = f"{output}/temp/all_contigs.fasta"
    output_dir = f"{output}/temp/miniasm"
    cmd = """miniasm -f {file_input2} {file_input1} > resu.gfa """
    return {
            'name': "miniasm",
            'file_dep': [file_input1],
            'targets': [output_dir],
            'actions': [cmd],
        }

    """
        TO DO: add possibility to give a configuration file
        Since both program need installation do I Wrote a install script for
    minimap,miniasm and spades or do I just ask for their PATH or do I assume
    they are in the overall
    """
