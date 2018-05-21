#!/usr/bin/env python
# -*- coding: utf-8 -*-

from capture import parse


def test_is_gzip():
    gzipped = "data/20_reads_R1.fastq.gz"
    not_gzipped = "data/20_reads_R1.fastq"
    assert parse.is_gzip(gzipped) is True
    assert parse.is_gzip(not_gzipped) is False
