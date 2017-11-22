#!/usr/bin/env python3
import sys
import os
import csv
from collections import namedtuple
from multiprocessing import Process,Queue,Pool

incomequeue = Queue()
computequeue = Queue()
#writequeue =  Queue()


IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
)

INCOME_TAX_START_POINT = 3500

INCOME_TAX_QUICK_LOOKUP_TABLE =[
    IncomeTaxQuickLookupItem(80000, 0.45, 13505),
    IncomeTaxQuickLookupItem(55000, 0.35, 5505),
    IncomeTaxQuickLookupItem(35000, 0.30, 2755),
    IncomeTaxQuickLookupItem(9000, 0.25, 1005),
    IncomeTaxQuickLookupItem(4500, 0.2, 555),
    IncomeTaxQuickLookupItem(1500, 0.1, 105),
    IncomeTaxQuickLookupItem(0, 0.03, 0)
]

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
class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]

    def getargs(self,op):
        args = self.args
        try:
            index = args.index(op)
            return args[index+1]
        except:
            print("Parameter error")
            exit()
    @property
    def getConfigFile(self):
        return self.getargs('-c')    
    @property
    def getUserFile(self):
        return self.getargs('-d')    
    @property
    def getGongziFile(self):
        return self.getargs('-o')    

args = Args()

class Config(object):
    def __init__(self):
        self.config={}
        with open(args.getConfigFile,'r') as lines:
            for line in lines:
                kv = line.strip().split("=")
                key = kv[0].strip()
                value = kv[1]
                try: 
                    self.config[key] = float(value)
                except ValueError:
                    print('Parameter Error')
                    exit()

    def getconfig(self,key):
        return self.config[key]
    
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
                # print(line)
                kvs = line.strip().split(",")
                # print(kvs)
                user = revInt(kvs[0])
                income = kvs[1]
                income = revInt(income)
                list = [user,income]
                lists.append(list)
            except (ValueError):
                print("Prameter Error")
                exit()    
    # print(lists)    
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
            aftincome = income_noSocialSec - persontax;
            gongzi = ('{},{},{:.2f},{:.2f},{:.2f}'.format(user,income,SocialSec,persontax,aftincome))
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

    #getincome()
    #computetax()
    #writefile()
    Process(target=getincome).start()
    #Process(target=computetax).start()

    pool = Pool(processes=3) 
    pool.apply(computetax) 
    Process(target=writefile).start()
 
if __name__ == '__main__':
    main()
