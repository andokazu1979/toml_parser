#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from collections import OrderedDict


class TOMLParser:
    def __init__(self):

        ########################################
        # Standard expressions
        ########################################

        # Hash
        self.pat_hash = re.compile(u'([\w\d]+)\s*=\s*([\'\"\[]?[/\-\w\d.\s,\'\_\(\){}:ぁ-んァ-ンー一-龥：、。−「」=%]+[\'\"\]]?)\s*\n')

        # Table
        self.pat_table = re.compile(r'^\[([\-\w\d.]+)\]$')

        # Array of table
        self.pat_array_table = re.compile(r'^\[\[([\-\w\d.]+)\]\]$')

        # Integer
        self.pat_int = re.compile(r'^-?(\d+)$')

        # Float
        self.pat_float = re.compile(r'^([\d.]+)$')

        # String
        self.pat_string = re.compile(u'^([\'\"][/\-.\w\d\_\(\)\s{}:ぁ-んァ-ンー一-龥：、。−「」=%]+[\'\"])$')

        # Array
        self.pat_array = re.compile(u'^\[([/\-\w\d.\s,\'\_\(\)\s{}:ぁ-んァ-ンー一-龥：、。−「」=%]+)\]$')

        # Comment
        self.pat_comment = re.compile(r'^#.*')

        # self.dict_root = {}
        self.dict_root = OrderedDict()

        self.is_array_table = False
        self.index_array_table = 0

    def parse(self, path):

        ########################################
        # Parsing
        ########################################

        with open(path) as f:
            # table_name = ''
            for line in f:
                line = line.decode("utf-8")
                match_hash = self.pat_hash.search(line)
                match_table = self.pat_table.search(line)
                match_array_table = self.pat_array_table.search(line)
                match_comment = self.pat_comment.search(line)
                if match_comment:
                    # print "comment : {0}".format(line)
                    pass
                elif match_hash:
                    items_hash = match_hash.groups()
                    key = items_hash[0]
                    val = items_hash[1]
                    # print('key={0} val={1}'.format(key, val))
                    if self.pat_int.search(val):
                        # print('num: ' + val)
                        val = int(val)
                    elif self.pat_float.search(val):
                        # print('float: ' + val)
                        val = float(val)
                    elif self.pat_string.search(val):
                        # print('string: ' + val)
                        val = val[1:-1]
                    elif self.pat_array.search(val):
                        # print('array: ' + val)
                        val = val[1:-1].replace(' ', '').split(',')
                        for i, item in enumerate(val):
                            if self.pat_int.search(item):
                                val[i] = int(item)
                            elif self.pat_string.search(item):
                                val[i] = item[1:-1]
                    # self.dict_root[table_name][key] = val
                    self.set_hash(table_name, key, val)
                elif match_table:
                    table_name = match_table.groups()[0]
                    # self.dict_root[table_name] = {}
                    self.is_array_table = False
                elif match_array_table:
                    tmp = match_array_table.groups()[0]
                    if(tmp == table_name):
                        self.index_array_table += 1
                    else:
                        self.index_array_table = 0
                    table_name = tmp
                    self.is_array_table = True

    def set_hash(self, tname, key, val, d=None):
        if d is None:
            tname = tname.split(".")
            tname.reverse()
            d = self.dict_root
        tmp = tname.pop()
        if tmp not in d:
            if(self.is_array_table == True):
                d[tmp] = []
            else:
                d[tmp] = OrderedDict()
        if len(tname) == 0:
            if(self.is_array_table == True):
                if(len(d[tmp]) == self.index_array_table):
                    d[tmp].append(OrderedDict())
                d[tmp][self.index_array_table][key] = val
            else:
                d[tmp][key] = val
            return
        else:
            self.set_hash(tname, key, val, d[tmp])

    def show(self, d, tname=[]):
        if isinstance(d, OrderedDict):
            for item in d.items():
                if isinstance(item[1], OrderedDict):
                    tname.append(item[0])
                    print("[{0}]".format('.'.join(tname)))
                    self.show(item[1], tname)
                elif isinstance(item[1], list) and isinstance(item[1][0], OrderedDict):
                    tname.append(item[0])
                    print("[[{0}]]".format('.'.join(tname)))
                    for item_ in item[1]:
                        self.show(item_)
                else:
                    print "{0} : {1}".format(item[0], item[1])
            if len(tname) != 0:
                tname.pop()

if __name__ == '__main__':
    obj = TOMLParser()
    obj.parse(sys.argv[1])
    obj.show(obj.dict_root)
