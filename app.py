import os
from werkzeug.utils import secure_filename
from datetime import datetime
import speech_recognition as sr
from flask import Flask,render_template,request,url_for,session,redirect
from flask_mysqldb import MySQL
from moviepy.editor import *
import json
with open('config.json','r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'qasystem'
mysql = MySQL(app)
app.config['UPLOAD_FOLDER'] = params['upload_folder_path']

#scret key is needed for session
app.secret_key = params['session_secret_key']

@app.route("/",methods=['GET', 'POST'])
def index_page():
    if request.method == "POST":
        username = request.form['name']
        topic = request.form['topic']
        video= request.files['inputfile']
        video.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(video.filename)))
        videoClip = VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(video.filename)))
        audiopath = os.path.splitext(video.filename)[0]
        audioclip = videoClip.audio.write_audiofile(os.path.join(app.config['UPLOAD_FOLDER'],audiopath+'.wav'))
        r = sr.Recognizer()
        audio_file = sr.AudioFile(os.path.join(app.config['UPLOAD_FOLDER'],audiopath+'.wav'))
        with audio_file as source:
            audio = r.record(source)
            result = r.recognize_google(audio)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Lectures(username,topic,videoname,videotext,date) VALUES(%s,%s,%s,%s,%s)",(username,topic,video.filename,result,datetime.now()))
        mysql.connection.commit()
        cur.close()
        session["result"] = result
        return render_template("session.html",result=result)

    return render_template("index.html",params=params)

@app.route("/session",methods=['GET', 'POST'])
def session_Page():
    if request.method == "POST":
        question = request.form['question']
        answer_text = session.get("result",None)
        from answer_extractor import get_answer
        Answer = get_answer(question,answer_text)
        answer_user= Answer['answer']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Lectures(username,topic,videoname,videotext,date) VALUES(%s,%s,%s,%s,%s)",
                    (username, topic, video.filename, result, datetime.now()))
        mysql.connection.commit()
        cur.close()
        return render_template("session.html",answer_user=answer_user,result=answer_text)

    return render_template("session.html")

@app.route("/login",methods=['GET','POST'])
def admin_login():
    if ('user' in session and session['user']== params['admin_username']):
        return render_template("admin.html")

    if request.method == "POST":
        username = request.form['usernmae']
        passward = request.form['passward']
        if (username== params['admin_username'] and passward==params['admin_password']):
            session['user'] = username
            return render_template("admin.html")
        else:
            return render_template("login.html",params=params)
    return render_template("login.html",params=params)

@app.route("/admin",methods=['GET','POST'])
def admin_dashboard():
    return render_template("admin.html")
@app.route("/logout",methods=['GET','POST'])
def logout():
    session.pop('user')
    return redirect(url_for('index_page',params=params))

if __name__=="__main__":
    app.run(debug=True)