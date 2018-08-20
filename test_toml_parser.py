#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os

from toml_parser import TOMLParser

class TestTOMLParser(object):

    def teardown_class(cls):
        os.remove('test.toml')

    @pytest.fixture()
    def conf(cls):
        str_toml = """
[all]
rootpath_in = '/work2/kenshi/'
rootpath_out = '/work/ando/detect_disturb'
year = [2010, 2011]
case = ['Case-0001', 'Case-0002']

[sub]
id = 101
ratio = 1.25
coord = -123
comment = "average"

[sub.arr1]
id = 101

[[sub.arr1.arr2]]
a = 1
b = 10

[[sub.arr1.arr2]]
a = 2
b = 20
"""[1:]

        with open('test.toml', 'w') as f:
            f.write(str_toml)

        parser = TOMLParser()
        parser.parse('test.toml')
        return parser.dict_root

    def test_parse(self, conf):
        assert conf['all']['rootpath_in'] == '/work2/kenshi/'
        assert conf['all']['year'][0] == 2010
        assert conf['all']['year'][1] == 2011
        assert conf['all']['case'][0] == 'Case-0001'
        assert conf['all']['case'][1] == 'Case-0002'
        assert conf['sub']['comment'] == 'average'
        assert conf['sub']['arr1']['id'] == 101
        assert conf['sub']['arr1']['arr2'][0]['a'] == 1
        assert conf['sub']['arr1']['arr2'][0]['b'] == 10
        assert conf['sub']['arr1']['arr2'][1]['a'] == 2
        assert conf['sub']['arr1']['arr2'][1]['b'] == 20
        
# pytest.main()
