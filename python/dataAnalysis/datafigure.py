#!/usr/bin/env python3
#-*- coding=utf-8 -*-

import json
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def datafigure(file):
    if(os.path.isfile(file)):
        df = pd.read_json(file)
        res = df[['user_id','minutes']].groupby('user_id').sum() 
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_title('StudyData')
        ax.set_xlabel('User ID')
        ax.set_ylabel('Study Time')
        ax.plot(res.index,res.minutes)
        plt.show()
        #res.plot() 
        #plt.show()

   
    else:
        print("file error")
if __name__ == '__main__':
    datafigure('/home/shiyanlou/Code/user_study.json')


