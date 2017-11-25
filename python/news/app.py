#!/usr/bin/env python3

import os
from flask import render_template,Flask,abort
import json

app = Flask(__name__)

@app.route('/')
def index():
    artlist = []
    path = '/home/shiyanlou/files'
    files = os.listdir(path)
    print(files)
    for f in files:
        j=os.path.join(path,f)
        print(j)
        if(os.path.isfile(j)):
            with open(j,'r') as file:
                art = json.loads(file.read())
                title = art['title']
                print(title)
                artlist.append(title)
        else:
            print(f,"is not a file")

    return render_template('index.html',artlist=artlist)

@app.route('/files/<filename>')
def file(filename):
    path = '/home/shiyanlou/files/'
    filepath = path + filename + '.json'
    arts = []
    if(os.path.isfile(filepath)):
        with open(filepath,'r') as file:
            art = json.loads(file.read())
            arts.append(art)
    else:
        abort(404)

    return render_template('file.html',arts=arts)
         
         
@app.errorhandler(404)
def not_found(error): 
    return render_template('404.html'), 404

         
          
           




if __name__=='__main__':
    app.run()


