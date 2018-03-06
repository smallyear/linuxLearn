#!/usr/bin/env python3
# coding=utf-8

import sys
import telnetlib
import os
import time

enter='\n'
#filehead="D:\\file\\"
filehead="test"
filetail=".txt"

def getfile(filename):
    f=open(filename,'w+')
    while(1):
        ret = tn.read_until('#',1)
        f.write(ret)
        if '#' in ret:
            break
        else:
            for i in range(10):
                tn.write(' ')
                time.sleep(0.1)
    f.close()

def get(string):
    tn.write(string+enter)
    filename=filehead+string.replace(' ','-')+filetail
    getfile(filename)
    print(string+' infomation is in '+filename)
    print('Router#')

def login():
    password = sys.argv[2]
    tn.read_until("Password: ",1)
    tn.write(password + enter)

    tn.read_until("Router>",1)
    tn.write('en'+enter)

    tn.read_until("Password: ",1)
    tn.write(password + enter)

    print(tn.read_until("Router#",1))

def options():
    showstrings=["show version",
                 "show arp",
                 "show run",
                 "show running-config",
                 "show startup-config",
                 "show ip interface brief",
                 "show ip route",
                 "ifconfig"]
    string=raw_input()
    string=string.lower()
    if string=='exit':
        tn.write('exit'+enter)
        print('exit success')
        exit()
    elif string in showstrings:
        get(string)
    else:
        print('wrong input')

if __name__ == '__main__':
    Host = sys.argv[1]
    tn = telnetlib.Telnet(Host)
    login()
    options()
