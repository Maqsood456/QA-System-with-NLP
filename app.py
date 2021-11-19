import os
from datetime import datetime
import speech_recognition as sr
from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
from moviepy.editor import *
UPLOAD_FOLDER = 'C:\\Users\\MUHAMMAD\\PycharmProjects\\myproject\\static'
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'qasystem'
mysql = MySQL(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/",methods=['GET', 'POST'])
def index_page():
    if request.method == "POST":
        username = request.form['name']
        topic = request.form['topic']
        video= request.files['inputfile']
        video.save(os.path.join(app.config['UPLOAD_FOLDER'],video.filename))
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
        return redirect(url_for('session_Page'))

    return render_template("index.html")

@app.route("/session",methods=['GET', 'POST'])
def session_Page():
    return render_template("session.html")

if __name__=="__main__":
    app.run(debug=True)