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
    session['pth'] = root
    folders, files = get_file_tree()
    
    
    return render_template("index.html", folders = folders, files = files, cur_pth = session['pth']  )

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
    return "/home" + pth[1:]
    session['pth'] = "/home" + pth[1:]
    folders, files = get_file_tree()
    print(session['pth'])
    return render_template("index.html", folders = folders, files = files, cur_pth = request.url[25:] )
    


@app.route('/<string:file>')
def send(file):
    
    return str(os.path.join(session['pth'], file))
    try:
        return send_file(os.path.join(app.config.get('STATIC_FOLDER'),file), as_attachment= True)
        
    except:
        
        return "Something went wrong"
        
 


if __name__ == '__main__':

    app.run("192.168.1.44",  port=5000)

    