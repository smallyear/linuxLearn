#!/usr/bin/env python3

import os
import json


def file(filename):
    path = '/home/shiyanlou/files/'
    filepath = path + filename + '.json'
    print(filepath)
    if(os.path.isfile(filepath)):
        with open(filepath,'r') as file:
            arts = json.loads(file.read())
    return arts
if __name__=='__main__':
    print(file('helloshiyanlou'))


