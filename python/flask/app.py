#!/usr/bin/env python3

from flask import Flask
from flask import render_template,redirect,url_for
from flask import make_response,request
from flask import abort

app=Flask(__name__)

app.config.update({
    'SECRET_KEY':'a random string'
    })

@app.route('/')
def index():
    username = request.cookies.get('username')
    return 'hello, {}'.format(username) 


@app.route('/user/<username>')
def user(username):
    if username == 'invalid':
        abort(404)
    resp = make_response(render_template('user_index.html',username=username))
    resp.set_cookie('username',username)
    return resp

@app.route('/blog/<int:post_id>')
def blog(post_id):
    return 'blog {}'.format(post_id)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

if __name__=='__main__':
    app.run()
