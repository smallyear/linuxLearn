# -*- coding:utf-8 -*_

import sys
from pymongo import MongoClient

def get_rank(user_id):
    client = MongoClient('127.0.0.1',27017)
    db = client.shiyanlou
    contests = db.contests

    res = {}

    list = contests.aggregate( [{"$group" : {"_id" : "$user_id", "score" : {"$sum" : "$score"}, "submit_time" : {"$sum" : "$submit_time"}}},{"$sort":{"score":-1}}])

    for index,raw in enumerate(list):
        res[raw['_id']] = [index+1,raw['score'],raw['submit_time']]

    reslist = res[user_id]
    rank = reslist[0]
    score = reslist[1]
    submit_time = reslist[2]

    return rank, score, submit_time

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            user_id = int(sys.argv[1])
            userdata = get_rank(user_id)
            print(userdata)
        except:
            print('Parameter Error')
            exit()
    else:
        print('Parameter Error')
