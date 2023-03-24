# PROGRAMMER: EMMANUEL MAYOWA SAMUEL
# DATE CREATED: 21/03/2023
# REVISED DATE: 21/03/2023
# PURPOSE: Create an Audio Mood Finder app


from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from pathlib import Path
from speech-recognition import Recognizer, AudioFile
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# defines the recognizer method into a variable
recognizer = Recognizer()
# download the vader_lexicon
nltk.download('vader_lexicon')


# function for opening files
def open_files():
    global root_dir
    path = QFileDialog.getExistingDirectory(window, 'Select Folder')
    if path:
        root_dir = Path(path)
        message.setText(path)


# function for analyzing audio and finding mood
def find_mood():
    for path in root_dir.glob("*.wav"):
        with AudioFile(path) as audio_file:
            audio = recognizer.record(audio_file)
    text = recognizer.recognize_google(audio)
    nltk.download('vader_lexicon')
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    print(scores)
    # checks the score and prints mood
    if scores['compound'] > 0:
        message.setText('<font color="green">Positive Speech!</font>')
    else:
        message.setText('<font color="green">Negative Speech!</font>')


# App instance defined
app = QApplication([])
window = QWidget()
window.setWindowTitle('Audio Mood Finder App')
layout = QVBoxLayout()

# description to explain usage
description = QLabel('Select the folder containing the audio files in <font color="red">.wav format</font>')
layout.addWidget(description)

# button widget to open files
open_btn = QPushButton('Open Folder')
open_btn.setToolTip('Open File')
open_btn.setFixedWidth(100)
layout.addWidget(open_btn, alignment=Qt.AlignmentFlag.AlignCenter)
open_btn.clicked.connect(open_files)

# button widget to analyze audio file
destroy_btn = QPushButton('Find Mood')
destroy_btn.setFixedWidth(100)
layout.addWidget(destroy_btn, alignment=Qt.AlignmentFlag.AlignCenter)
destroy_btn.clicked.connect(find_mood)

# sets message output
message = QLabel('')
layout.addWidget(message, alignment=Qt.AlignmentFlag.AlignCenter)

# runs app
window.setLayout(layout)
window.show()
app.exec()
