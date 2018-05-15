#!/usr/bin/env python
# -*- coding: utf-8 -*-


def is_gzip(file):
    logger = logging.getLogger(__name__)
    magic_number = b"\x1f\x8b\x08\x08"
    f = open(file, "rb")
    with f:
        try:
            assert f.read(4) == magic_number
        except AssertionError as e:
            logger.info(f"{file} is not gzipped")
            return false
        else:
            return true


def parse(file):
    if is_gzip(file):
        name = file.replace(".fastq.gz", "").replace(".fq.gz", "")
        with gzip.open(file, "rt") as handle:
            file_record = SeqIO.parse(handle, "fastq")
            return(file_record, name)
    else:
        with open(file, "rt") as handle:
            file_records = SeqIO.parse()
            name = file
            return(file_record, name)
