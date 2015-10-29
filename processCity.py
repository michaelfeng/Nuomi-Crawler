#!/usr/bin/env  python
# This Python file uses the following encoding: utf-8

import json

if __name__ == '__main__':
    str = ""
    pname = "city.json"
    with open(pname) as f:
        for line in f:
            str = str + line.strip()
        #print str
        py_objs = json.loads(str)
        for obj in py_objs:
            print obj["pinyin"].lower()

