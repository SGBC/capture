#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import argparse

from capture.version import __version__


def assemble(args):
    """
    main function for the capture software

    Arguments:
    args (object): the argument dictionary from argparse
    """
    logger = logging.getLogger(__name__)
    print('hi from assemble')


def main():
    parser = argparse.ArgumentParser(
        prog="capture",
        usage="capture [arguments]",
        description="the capture-seq assembler"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="print version and exit"
    )
    parser.set_defaults(func=assemble)
    args = parser.parse_args()

    try:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        if args.version:
            logger.info("capture version %s" % __version__)
            sys.exit(0)
        args.func(args)
    except AttributeError as e:
        logger.debug(e)
        parser.print_help()
        # raise
