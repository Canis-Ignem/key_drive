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

root = "home/"
aux_root = "home/"
app = Flask(__name__, template_folder="./templates")

app.config['STATIC_FOLDER'] = "home/"

uploads_dir = os.path.join(app.instance_path, 'uploads')

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route("/")
def index():
    folders, files = get_file_tree()
    
    session['pth'] = "/home/"
    return render_template("index.html", folders = folders, files = files, cur_pth = session['pth']  )

def get_file_tree():
    
    folders  = []
    files = []

    for f in os.listdir(app.config.get('STATIC_FOLDER')):
        
        if os.path.isdir(app.config.get('STATIC_FOLDER')+f):
            
            folders.append(f)
        else:
            files.append(f)
                
    return folders, files

@app.route('/<regex("[abcABC0-9]{4,6}"):uid>-<slug>/<string:file>')
def goto(filename):
    return str(request.url)
    app.config['STATIC_FOLDER'] = os.path.join(app.config.get('STATIC_FOLDER'), filename)
    folders, files = get_file_tree()
    
    return render_template("index.html", folders = folders, files = files)
    


@app.route('/<regex("[A-Z|a-z]*")/<string:file>')
def send(file):
    
    return os.path.join(session['pth'], request.url)
    try:
        return send_file(os.path.join(app.config.get('STATIC_FOLDER'),file), as_attachment= True)
        
    except:
        
        return "Something went wrong"
        
    


if __name__ == '__main__':

    app.run("192.168.11.1",  port=5000)

    