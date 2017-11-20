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

class Config(object):
	def __init__(self):
		self.config={}
		print()
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

def getshebao(income):
	# if income < config.getShebaoL:
	return '{:.2f}'.format(100)

def getpersontax(income_shebao):
    taxable_part = income_shebao - INCOME_TAX_START_POINT

    if taxable_part <= 0:
        tax=0
    for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
        if taxable_part > item.start_point:
            tax = taxable_part * item.tax_rate - item.quick_subtractor
            break
    return '{:.2f}'.format(tax)
 
if __name__ == '__main__':
	args = sys.argv[1:]
	index = args.index('-c')
	CONFIGFILE = args[index+1]
	userindex = args.index('-d')
	USERFILE = args[userindex+1]
	gongziindex = args.index('-o')
	GONGZIFILE = args[gongziindex+1]

	configdict = Config()

	JiShuL = configdict.getconfig('JiShuL')
	JiShuH = configdict.getconfig('JiShuH')

	socialRateSum = sum([
            configdict.getconfig('YangLao'),
            configdict.getconfig('YiLiao'),
            configdict.getconfig('ShiYe'),
            configdict.getconfig('GongShang'),
            configdict.getconfig('ShengYu'),
            configdict.getconfig('GongJiJin')
        ]) 


	with open(USERFILE,'r')	as lines:
		for line in lines:
			kvs = line.strip().split(",")
			user = kvs[0]
			income = kvs[1]
			income = revInt(income)
			#根据income计算社保金额，个税金额，税后工资
			if income < JiShuL:
				SocialSec = JiShuL* socialRateSum
			elif income < JiShuH:
				SocialSec = income * socialRateSum
			else:
				SocialSec = JiShuH * socialRateSum	
			# shebao = getshebao(income)
			income_noSocialSec = income - SocialSec
			persontax = getpersontax(income_noSocialSec)
			persontax = revFloat(persontax)
			aftincome = income_noSocialSec - persontax;
			gongzi = ('{},{},{:.2f},{:.2f},{:.2f}'.format(user,income,SocialSec,persontax,aftincome))
			#追加写入文件
			with open(GONGZIFILE,'a') as gongzis:
				gongzis.write(gongzi+'\n')
