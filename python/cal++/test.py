#!/usr/bin/pyhton3
import sys

import csv
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

class Config(object):
	def __init__(self):
		self.config={}
		with open(CONFIGFILE,'r') as lines:
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
if __name__ == '__main__':
	args = sys.argv[1:]
	index = args.index('-c')
	CONFIGFILE = args[index+1]
	userindex = args.index('-d') 
	USERFILE = args[userindex+1]
	gongziindex = args.index('-o')
	GONGZIFILE = args[gongziindex+1]

	configdict = Config()
	for k,v in configdict.config.items():
		print(k,v)

	print(configdict.config)
	configs = configdict.getconfig('YiLiao')
	print(configs)
 
