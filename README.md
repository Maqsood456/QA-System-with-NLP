# NLP-Based Question Answering Engine from Videos

Final year project for BS Computer Science, Bahauddin Zakariya University, Multan (2022).

## About

A web application where a student uploads a lecture video and asks questions about it in plain English. The system converts the lecture speech to text and uses a BERT question answering model to find the answer inside the lecture text, as if the student were asking the instructor in the video.

**Category:** Artificial Intelligence, Natural Language Processing, Speech Recognition

## How It Works

1. **Upload:** On the home page the user enters a username, the lecture topic and uploads a video file.
2. **Audio extraction:** MoviePy pulls the audio out of the video and saves it as a `.wav` file.
3. **Speech to text:** Google Speech Recognition converts the audio into the lecture transcript.
4. **Save:** The username, topic, video file name, transcript and date are saved in a MySQL database.
5. **Ask questions:** The session page shows the transcript. The user types a question in English.
6. **Answer:** A BERT model (`deepset/bert-base-cased-squad2`, via Hugging Face Transformers) reads the question and the transcript and returns the answer, which is shown on the page.

## Features

- Video upload with username and lecture topic
- Automatic speech-to-text transcript of the lecture
- Question answering from the transcript using a pre-trained BERT model
- MySQL database to store lectures
- Admin login page and admin dashboard
- Responsive pages built with Bootstrap

## Technologies Used

| Area | Tools |
|------|-------|
| Language | Python |
| Web framework | Flask |
| NLP / Deep Learning | BERT question answering model (`deepset/bert-base-cased-squad2`), Hugging Face Transformers, PyTorch |
| Speech and video | SpeechRecognition (Google Speech Recognition), MoviePy |
| Database | MySQL (flask-mysqldb) |
| Frontend | HTML, CSS, Bootstrap, Jinja2 templates |
| Tools | Git, GitHub, PyCharm |

## Project Structure

```
QA-System-with-NLP/
├── app.py                # Flask app: routes, video upload, speech-to-text, database
├── answer_extractor.py   # Question answering with the BERT model
├── config.json           # Settings: upload folder, secret key, admin login, footer text
├── templates/            # base, index, session, login and admin pages
└── static/               # CSS, JavaScript, images and uploaded lecture files
```

## Installation

**Requirements:** Python 3, a MySQL server (for example XAMPP or MySQL Server), and an internet connection (needed for Google Speech Recognition and to download the BERT model on first use).

**1. Clone the repository**

```bash
git clone https://github.com/Maqsood456/QA-System-with-NLP.git
cd QA-System-with-NLP
```

**2. Install the libraries**

```bash
pip install flask flask-mysqldb moviepy SpeechRecognition transformers torch
```

**3. Create the database.** Start MySQL and run:

```sql
CREATE DATABASE qasystem;
USE qasystem;
CREATE TABLE Lectures (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100),
  lecture_topic VARCHAR(255),
  lecture_file VARCHAR(255),
  lecture_text LONGTEXT,
  qa_file TEXT,
  date_posted DATETIME
);
```

The database host, user and password are set at the top of `app.py` (default: `localhost`, `root`, empty password).

**4. Set the upload folder.** In `config.json`, change `upload_folder_path` to a folder on your computer where videos and audio files can be saved (for example the full path to the project's `static` folder).

**5. Run the app**

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Usage

1. Open the home page, enter your name and the lecture topic, and upload a short video.
2. Click **Start QA session** and wait while the transcript is created.
3. Type a question about the lecture and click **Send Question**.
4. The answer appears below the question box.
5. The admin pages are available at `/login`.

## Author

**Muhammad Maqsood**
Email: maqsood.codemaster@gmail.com
GitHub: [Maqsood456](https://github.com/Maqsood456)
LinkedIn: [maqsood-qureshi](https://www.linkedin.com/in/maqsood-qureshi)
