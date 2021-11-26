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
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
@app.route("/",methods=['GET', 'POST'])
def index_page():
    if request.method == "POST":
        username = request.form['name']
        topic = request.form['topic']
        video= request.files['inputfile']
        video.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(video.filename)))
        videoClip = VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'],video.filename))
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

    return render_template("index.html")

@app.route("/session",methods=['GET', 'POST'])
def session_Page():
    if request.method == "POST":
        question = request.form['question']
        answer_text = session.get("result",None)
        from answer_extractor import find_answer
        answer = find_answer(question,answer_text)
        return redirect(url_for('session_Page',answer_user=answer))

    return render_template("session.html")

if __name__=="__main__":
    app.run(debug=True)