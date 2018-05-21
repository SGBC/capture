#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import argparse

from capture import split
from capture.version import __version__


def assemble(args):
    """
    main function for the capture software

    Arguments:
    args (object): the argument dictionary from argparse
    """
    logger = logging.getLogger(__name__)
    genome_size = args.genome_size
    mean_size = args.mean
    output = args.output
    try:
        os.makedirs(args.output)
        if args.forward and args.reverse:
            split.split(
                genome_size, mean_size, output,
                args.forward, type_f="forward"
                )
            split.split(
                genome_size, mean_size, output,
                args.reverse, type_f="reverse"
             )
        elif args.uniq:
            split.split(
                genome_size, mean_size, output,
                args.uniq, type_f="uniq"
            )
        elif args.bam:
            split.split(
                genome_size, mean_size, output,
                args.bam, type_f="bam"
            )
        else:
            logger.error("Invalid combination of input files. Aborting")
            sys.exit(1)
    except OSError as e:
        logger.error(f"{args.output} already exists. Aborting.")
        sys.exit(1)
    else:
        pass


def main():
    parser = argparse.ArgumentParser(
        prog="capture",
        usage="capture [arguments]",
        description="the capture-seq assembler"
    )
    file_group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="print version and exit"
    )
    file_group.add_argument(
        "-u",
        "--uniq",
        help="Input reads file in format fastq fastq.gz",
        type=str
    )
    file_group.add_argument(
        "-f",
        "--forward",
        help="Input forward file in format fastq fastq.gz",
        type=str
    )
    parser.add_argument(
        "-r",
        "--reverse",
        help="Input reverse file in format fastq fastq.gz",
        type=str
    )
    file_group.add_argument(
        "-b",
        "--bam",
        help="Input the reads file in bam format"
    )
    parser.add_argument(
        "-g",
        "--genome_size",
        help="The size of the genome specific to your reads in numeric value",
        type=int
    )
    parser.add_argument(
        "-m",
        "--mean",
        help="The mean size of the reads present in the input file",
        type=float
    )
    parser.add_argument(
        "-o",
        "--output",
        help="The output directory"
    )
    parser.set_defaults(func=assemble)
    args = parser.parse_args()

    try:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        if args.version:
            logger.info(f"capture version {__version__}")
            sys.exit(0)
        args.func(args)
    except AttributeError as e:
        logger.debug(e)
        parser.print_help()
        raise
