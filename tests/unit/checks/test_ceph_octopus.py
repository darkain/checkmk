#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from typing import List, Mapping, Tuple

import pytest

from tests.testlib import Check

octopus_info = [['---', 'RAW', 'STORAGE', '---'],
                ['CLASS', 'SIZE', 'AVAIL', 'USED', 'RAW', 'USED', '%RAW', 'USED'],
                ['ssd', '27', 'TiB', '21', 'TiB', '5.9', 'TiB', '5.9', 'TiB', '21.76'],
                ['TOTAL', '27', 'TiB', '21', 'TiB', '5.9', 'TiB', '5.9', 'TiB', '21.76'],
                ['---', 'POOLS', '---'],
                [
                    'POOL', 'ID', 'STORED', '(DATA)', '(OMAP)', 'OBJECTS', 'USED', '(DATA)',
                    '(OMAP)', '%USED', 'MAX', 'AVAIL', 'QUOTA', 'OBJECTS', 'QUOTA', 'BYTES',
                    'DIRTY', 'USED', 'COMPR', 'UNDER', 'COMPR'
                ],
                [
                    'ceph-customer', '1', '1.7', 'TiB', '1.7', 'TiB', '720', 'MiB', '540.44k',
                    '4.5', 'TiB', '4.5', 'TiB', '2.1', 'GiB', '18.92', '6.5', 'TiB', 'N/A', 'N/A',
                    '540.44k', '0', 'B', '0', 'B'
                ],
                [
                    'ceph-sb', '2', '472', 'GiB', '472', 'GiB', '249', 'MiB', '165.16k', '1.4',
                    'TiB', '1.4', 'TiB', '747', 'MiB', '6.51', '6.5', 'TiB', 'N/A', 'N/A',
                    '165.16k', '0', 'B', '0', 'B'
                ],
                [
                    'device_health_metrics', '4', '31', 'MiB', '0', 'B', '31', 'MiB', '32', '92',
                    'MiB', '0', 'B', '92', 'MiB', '0', '6.5', 'TiB', 'N/A', 'N/A', '32', '0', 'B',
                    '0', 'B'
                ],
                [
                    'ceph-customer-ec32', '6', '5.9', 'GiB', '5.9', 'GiB', '0', 'B', '1.59k', '9.3',
                    'GiB', '9.3', 'GiB', '0', 'B', '0.05', '12', 'TiB', 'N/A', 'N/A', '1.59k',
                    '1.3', 'GiB', '2.6', 'GiB'
                ],
                [
                    'rbd_ec32', '8', '6.1', 'MiB', '2.1', 'KiB', '6.1', 'MiB', '6', '18', 'MiB',
                    '144', 'KiB', '18', 'MiB', '0', '6.5', 'TiB', 'N/A', 'N/A', '6', '0', 'B', '0',
                    'B'
                ]]

discovery: List[Tuple[str, Mapping]] = [('SUMMARY', {}), ('ceph-customer', {}),
                                        ('ceph-customer-ec32', {}), ('ceph-sb', {}),
                                        ('device_health_metrics', {}), ('rbd_ec32', {})]


@pytest.mark.parametrize("info, result", [
    (octopus_info, discovery),
])
def test_ceph_df_octopus_discovery(info, result):
    check = Check("ceph_df")
    parsed = check.run_parse(info)
    assert sorted(check.run_discovery(parsed)) == result
