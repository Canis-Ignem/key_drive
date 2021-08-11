from flask import Flask, render_template, request, session, url_for, redirect
import os
from flask.helpers import send_file
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from subprocess import Popen, list2cmdline
import re
import pandas as pd
import time
from werkzeug.routing import BaseConverter
import db
from md5 import md5

app = Flask(__name__, template_folder="./templates")

root = "/home/keystone/"
aux_root = "home"

app.secret_key = 'fat'


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route("/")
@app.route("/home")
def index():
    
    return render_template("login.html")

def get_file_tree():
    
    folders  = []
    files = []

    for f in os.listdir(session['pth']):
        
        if os.path.isdir(os.path.join( session['pth'],f)):
            
            folders.append(f)
        else:
            files.append(f)
                
    return folders, files


@app.route('/<path:pth>/<string:file>')
def goto(pth,file):
    pth = request.url.split('/home')
    session['pth'] = "/home" + str(pth[1:])[2:-2]
    folders, files = get_file_tree()
    print(session['pth'])
    return render_template("index.html", folders = folders, files = files, cur_pth = "/home"+str(pth[1:])[2:-2] )
    


@app.route('/<string:file>')
def send(file):
    
    try:
        return send_file(os.path.join(session['pth'], file), as_attachment= True)
        
    except:
        
        return "Something went wrong"
        

@app.route("/log", methods = ['POST'])
def login():
    if session['uname'] != None:
        folders, files = get_file_tree()
        return render_template("index.html", folders = folders, files = files, cur_pth = session['pth']  )
    else:
        try:
            
            if request.method == "POST":
                user = request.form["uname"].lower()
                if db.get_sum(user) == md5(request.form["psw"]):
                    
                    session['uname'] = user
                    session['email'] = db.get_email(user)
                    if os.path.isdir( os.path.join("/home", user) ):
                        session['pth'] = os.path.join("/home/", user)
                    else:
                        return "There is no such user"
                        
                    
                    folders, files = get_file_tree()
                    return render_template("index.html", folders = folders, files = files, cur_pth = session['pth']  )
                    
                else:
                    return "Pass missmatch"
                
                
        except:
            return "Something went wrong"

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/sign", methods = ['POST'])
def sign_in():
    
    try:
        
        if request.method == "POST":
            user = request.form["uname"].lower()
            request.form["psw"] == request.form["psw2"]
            email = request.form["email"].lower()
            DoB = request.form["age"]
            country = request.form["country"].lower()
            batch = request.form["batch"]
            gender = request.form["gender"]
            
            
            if db.add_user(user,request.form["psw"], email, DoB, country, batch, gender):
                session['uname'] = user
                session['email'] = email
                session['batch'] = batch
                if os.path.isdir( os.path.join("/home", user) ):
                    session['pth'] = os.path.join("/home/", user)
                else:
                    return "There is no such user"
                folders, files = get_file_tree()
                
                return render_template("index.html", folders = folders, files = files, cur_pth = session['pth']  )
            else:
                return "Some of the fields were not correct"
            
    except:
        return "Something went wrong"

if __name__ == '__main__':

    app.run("192.168.1.44",  port=5000)

    