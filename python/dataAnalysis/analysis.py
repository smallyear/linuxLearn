#!/usr/bin/env python3
#-*- coding=utf-8 -*-

import json
import pandas as pd
import sys
import os

def analysis(file,user_id):
    times = 0
    minutes = 0
    
    if(os.path.isfile(file)):
        df = pd.read_json(file)
        try:
            user_id = int(user_id)
        except ValueError:
            print("user_id is wrong")
            times = 0
            minutes = 0
        
        df1 = df[df['user_id'] == user_id]
        minutes = df1['minutes'].sum()
        times = len(df1)
   
    else:
        times = 0
        minutes = 0
    print(times,minutes)
    return times,minutes

if __name__ == '__main__':
    args = sys.argv[1:]
    file = args[0]
    user_id = args[1]
    analysis(file,user_id)


