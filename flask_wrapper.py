#Flask
from flask import Flask, render_template, request, session, url_for, redirect
from flask.helpers import send_file
from flask_dropzone import Dropzone

#Utils
import os

#Drive Utils
from md5 import md5
import db



app = Flask(__name__, template_folder="./templates")

app.secret_key = 'fat'

@app.route("/")
@app.route("/home")
def index():
    
    return render_template("login.html")

def get_file_tree():
    
    folders  = []
    files = []

    for f in os.listdir(session['pth']):
        
        if os.path.isdir(os.path.join( session['pth'],f)):
            if f[0] != '.':
                folders.append(f)
            
        elif f[0] != '.':
            files.append(f)
                
    return folders, files


@app.route('/<path:pth>/<string:file>')
def goto(pth, file):
    pth = request.url.split('/home')
    session['pth'] = "/home" + str(pth[1:])[2:-2]
    folders, files = get_file_tree()
    print(session['pth'])
    return render_template("index.html", folders = folders, files = files, cur_pth = "/home"+str(pth[1:])[2:-2], cur_folder= session['pth'].split('/')[-1] ) 
    


@app.route('/<string:file>')
def send(file):
    
    try:
        return send_file(os.path.join(session['pth'], file), as_attachment= True)
        
    except:
        
        return "Something went wrong"
        

@app.route("/log", methods = ['POST'])
def login():

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
                
                app.config.update(
                    UPLOADED_PATH= session['pth'],
                    DROPZONE_MAX_FILE_SIZE=5120,
                    DROPZONE_MAX_FILES=5*60*1000,
                    DROPZONE_DEFAULT_MESSAGE ="",
                    DROPZONE_UPLOAD_ON_CLICK=False
                )
                dropzone = Dropzone(app)
                
                url = url_for('goto',pth = session['pth'], file = "")[:-1]
                return redirect(url)
                
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
                app.config.update(
                    UPLOADED_PATH= session['pth'],
                    DROPZONE_MAX_FILE_SIZE=5120,
                    DROPZONE_MAX_FILES=5*60*1000,
                    DROPZONE_DEFAULT_MESSAGE ="Drag and Drop",
                    DROPZONE_UPLOAD_ON_CLICK=False
                
                )
                
                dropzone = Dropzone(app)
                
                url = url_for('goto',pth = session['pth'], file = "")[:-1]
                return url
                return redirect(url)
            else:
                return "Some of the fields were not correct"
            
    except:
        return "Something went wrong!"

@app.route('/upload',methods=['POST','GET'])  
def upload(): 
    if request.method == 'POST':
        f = request.files.get('file')
        f.save( os.path.join(session['pth'], f.filename) )
        
    return render_template('index.html')

if __name__ == '__main__':

    app.run()

    