#!/usr/bin/env python3
#-*-coding=utf-8 -*-


import pandas as pd

def quarter_volume():
    data = pd.read_csv('apple.csv',header=0)

    timeindex = pd.to_datetime(data['Date'])
    res = pd.Series(data['Volume'].as_matrix(),index=timeindex)
    la = res.resample('Q').sum().sort_values()
    second_volume = la[len(la)-2]

    return second_volume

if __name__=='__main__':
    print(quarter_volume())
