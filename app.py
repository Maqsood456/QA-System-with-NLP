from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/qasystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Lectures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    topic = db.Column(db.String(120), nullable=False)
    videoname = db.Column(db.String(120), nullable=False)
    videotext = db.Column(db.String(120), nullable=False)

@app.route("/",methods=['GET', 'POST'])
def index_page():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)