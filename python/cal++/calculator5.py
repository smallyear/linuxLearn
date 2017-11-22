#!/usr/bin/env python3


import getopt
import sys
import configparser
import csv
import queue
import os
from multiprocessing import Process, Queue,Pool
from collections import namedtuple
from datetime import date, datetime, timedelta
import time


IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
)

INCOME_TAX_START_POINT = 3500

INCOME_TAX_QUICK_LOOKUP_TABLE = [
    IncomeTaxQuickLookupItem(80000, 0.45, 13505),
    IncomeTaxQuickLookupItem(55000, 0.35, 5505),
    IncomeTaxQuickLookupItem(35000, 0.30, 2755),
    IncomeTaxQuickLookupItem(9000, 0.25, 1005),
    IncomeTaxQuickLookupItem(4500, 0.2, 555),
    IncomeTaxQuickLookupItem(1500, 0.1, 105),
    IncomeTaxQuickLookupItem(0, 0.03, 0)
]

incomequeue = Queue()
computequeue = Queue()

def revFloat(a):
    try:
        income = float(a)
    except ValueError:
        print("Parameter Error")
        exit()
    return income

def revInt(a):
    try:
        income = int(a)
    except ValueError:
        print("Parameter Error")
        exit()
    return income

def usage():
    print("Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata")

class Args(object):

    def __init__(self):
        self.city = self.getargs()
        self.args = sys.argv[1:]

    def getargs(self):
        opts,args = getopt.getopt(sys.argv[1:],'-hC:c:d:o:',['help','city='])
        city = ''
        for o,a in opts:
            if o in ("-h","--help"):
                usage()
                sys.exit()

            if o in ("-C","--city"):
                city = str.upper(a)
        
        if (city== ''):
            city = 'DEFAULT'
        return city

    def getoptargs(self,op):
        try:
            index = self.args.index(op)
            return self.args[index+1]
        except:
            print('Parameter error')
            exit()

    @property
    def getcity(self):
        return self.city
    @property
    def getConfigFile(self):
        return self.getoptargs('-c')    
    @property
    def getUserFile(self):
        return self.getoptargs('-d')    
    @property
    def getGongziFile(self):
        return self.getoptargs('-o')    

args = Args()
        



class Config(object):
    def __init__(self):
        self.config={}
        # print(args.getcity)
        configs = configparser.RawConfigParser()
        configs.read(args.getConfigFile)
        self.config = configs[args.getcity]
        # print(self.config['JiShuL'])

    def getconfig(self,key):
        return revFloat(self.config[key])
    
    @property
    def getJiShuL(self):
        return self.getconfig('JiShuL')
    @property
    def getJiShuH(self):
        return  self.getconfig('JiShuH')
    
    @property
    def getsocialRateSum(self):
        return sum([
            self.getconfig('YangLao'),
            self.getconfig('YiLiao'),
            self.getconfig('ShiYe'),
            self.getconfig('GongShang'),
            self.getconfig('ShengYu'),
            self.getconfig('GongJiJin')
        ]) 
configdict = Config()

def getpersontax(income_shebao):
    taxable_part = income_shebao - INCOME_TAX_START_POINT

    if taxable_part <= 0:
        tax=0
    for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
        if taxable_part > item.start_point:
            tax = taxable_part * item.tax_rate - item.quick_subtractor
            break
    return '{:.2f}'.format(tax)

def isFileExists(filename):
    if(os.path.isfile(filename)):
        pass
    else:
        print("file is not exists")
        exit()

def getincome():
    lists = []
    with open(args.getUserFile,'r')  as lines:
        for line in lines:
            try:    
                kvs = line.strip().split(",")
                user = revInt(kvs[0])
                income = kvs[1]
                income = revInt(income)
                list = [user,income]
                lists.append(list)
            except (ValueError):
                print("Prameter Error")
                exit()    
    incomequeue.put(lists)

def computetax():
    lists = incomequeue.get()
    JiShuL = configdict.getJiShuL
    JiShuH = configdict.getJiShuH
    socialRateSum = configdict.getsocialRateSum
    result = ''

    for list in lists:
        try:
            user = list[0]
            income = list[1]
            if income < JiShuL:
                SocialSec = JiShuL* socialRateSum
            elif income < JiShuH:
                SocialSec = income * socialRateSum
            else:
                SocialSec = JiShuH * socialRateSum   
            income_noSocialSec = income - SocialSec
            persontax = getpersontax(income_noSocialSec)
            persontax = revFloat(persontax)
            aftincome = income_noSocialSec - persontax
            # print(income_noSocialSec,aftincome)
            # t = datetime.utcnow()
            datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(datetime)
            gongzi = ('{},{},{:.2f},{:.2f},{:.2f},{}'.format(user,income,SocialSec,persontax,aftincome,datetime))
            result+=(gongzi+'\n')
        except :
            print("Prameter Error")
            exit()
    computequeue.put(result)

def writefile():
    gongzifile = args.getGongziFile
    result = computequeue.get()

    if (os.path.isfile(gongzifile)):
        os.remove(gongzifile)
    with open(gongzifile,'w') as f:
        f.write(result)





def main():
    # print(configdict.getJiShuL)
    getincome()
    computetax()
    writefile()

    # Process(target=getincome).start()
    # pool = Pool(processes=3) 
    # pool.apply(computetax) 
    # Process(target=writefile).start()

if __name__=='__main__':
    main()
