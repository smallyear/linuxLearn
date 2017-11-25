import os
from flask import render_template,Flask,abort
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String,Text
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/test'
db=SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

class File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category',backref=db.backref('files'))
    def __init__(self,title,created_time,category,content):
        self.title=title
        self.created_time=created_time
        self.category=category
        self.content=content

    def __repr__(self):
        return '<File %r>' % self.title

@app.route('/')
def index():
    artlist = []
    engine = create_engine('mysql://root:@localhost/test')
    artlist =  engine.execute('select * from file').fetchall()

    return render_template('index.html',artlist=artlist)

@app.route('/files/<file_id>')
def file(file_id):

    arts= []
    engine = create_engine('mysql://root:@localhost/test')
    arts =  engine.execute('select f.content,f.created_time,c.name from file f,category c where f.category_id = c.id and f.category_id  = ' + file_id).fetchall()
    if arts:
        return render_template('file.html',arts=arts)
    else:
        abort(404)
         
#    select f.content,f.created_time,c.name from file f  join category c on f.category_id = 1 and c.id = f.category_id     
@app.errorhandler(404)
def not_found(error): 
    return render_template('404.html'), 404

         
          
           




if __name__=='__main__':
    app.run()


