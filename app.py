import torch
import os
from datetime import datetime
import speech_recognition as sr
from flask import Flask,render_template,request,url_for,session
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

#scret key is needed for session
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
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
        session["result"] = result
        return render_template("session.html",result=result)

    return render_template("index.html")

@app.route("/session",methods=['GET', 'POST'])
def session_Page():
    if request.method == "POST":
        question = request.form['question']
        answer_text = session.get("result",None)
        import torch
        from transformers import BertForQuestionAnswering
        model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        from transformers import BertTokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        input_ids = tokenizer.encode(question, answer_text)
        tokens = tokenizer.convert_ids_to_tokens(input_ids)
        # Search the input_ids for the first instance of the `[SEP]` token.
        sep_index = input_ids.index(tokenizer.sep_token_id)
        # The number of segment A tokens includes the [SEP] token istelf.
        num_seg_a = sep_index + 1
        # The remainder are segment B.
        num_seg_b = len(input_ids) - num_seg_a
        # Construct the list of 0s and 1s.
        segment_ids = [0] * num_seg_a + [1] * num_seg_b
        # There should be a segment_id for every input token.
        assert len(segment_ids) == len(input_ids)
        # Run our example through the model.
        outputs = model(torch.tensor([input_ids]),  # The tokens representing our input text.
                        token_type_ids=torch.tensor([segment_ids]),
                        # The segment IDs to differentiate question from answer_text
                        return_dict=True)
        start_scores = outputs.start_logits
        end_scores = outputs.end_logits
        # Find the tokens with the highest `start` and `end` scores.
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores)
        # Combine the tokens in the answer and print it out.
        answer = ' '.join(tokens[answer_start:answer_end + 1])
        return answer

    return render_template("session.html",result=result)

if __name__=="__main__":
    app.run(debug=True)