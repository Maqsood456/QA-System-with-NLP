import os
from flask import Flask,render_template,request
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Lectures(username,topic,videoname) VALUES(%s,%s,%s)",(username,topic,video.filename))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)