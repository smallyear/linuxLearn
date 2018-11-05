#!/usr/bin/env python3


import getopt
import sys
import configparser
import csv
import queue
from multiprocessing import Process, Queue
from collections import namedtuple

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

qu1 = Queue()
qu2 = Queue()

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
            index = self.args[op]
            return self.args[index+1]
        except:
            print('Parameter error')
            exit()

    @property
    def getcity(self):
        return self.city
    @property
    def getconfigpath(self):
        return self.getoptargs('-c')
    @property
    def getuserpath(self):
        return self.getoptargs('-d')
    @property
    def getgongzipath(self):
        return self.getoptargs('-o')

args = Args()
        



class Config(object):
    def __init__(self):
        self.config={}
        configs = configparser.RawConfigParser()
        configs.read('test.cfg')
        self.config = configs[args.getcity]

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
configs = Config()

class UserData(Process):

    def _read_users_data(self):
        with open(args.getuserpath) as f:
            for line in f.readlines():
                employee_id, income_string = line.strip().split(',')
                print(employee_id,income)
                try:
                    income = int(income_string)
                    
                except ValueError:
                    print('Parameter Error')
                    exit()
                yield (employee_id, income)

    def run(self):
        for data in self._read_users_data():
            qu1.put(data)


def compute():
    employee_id, income = qu1.get()

    print(employee_id, income)


def usage():
    print("Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata")

def main():
    workers = [
        UserData()
    ]
    for worker in workers:
        worker.run()

    compute()

if __name__=='__main__':
    main()
