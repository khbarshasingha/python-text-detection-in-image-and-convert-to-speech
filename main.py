from flask import Flask , render_template, request, send_file

import cv2
import pytesseract
import numpy as np
import speech_recognition as sr 
from gtts import gTTS
from playsound import playsound

from PIL import Image
import secrets
import os
# ----------------------------------------------------------------------------------------------------
app=Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


@app.route('/',methods = ['GET','POST'])
def index():
	temp="default"
	if request.method == 'POST':
		f = request.files['file']

		temp = find_text(f)   #calling the text detection function
		temp=temp.replace('_',' ')
		audio_filename = convert_to_audio(temp)  # this saves the mp3 and returns it's file name
		# audio_filename = audio_filename+'.mp3'

		return render_template('index.html',temp=temp, audio_filename=audio_filename)
	return render_template('index.html')

def save_picture(form_picture):
    # name collision can occur, we will change the name of the file using secret module
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_filename =random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'images/', picture_filename)


	i = Image.open(form_picture)
	i.save(picture_path) 

	# after saving we will process using the cv2, convet to gray, apply threshold and blur and save the image
	img = cv2.imread('images/'+picture_filename)
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	blur=cv2.medianBlur(gray,3)
	cv2.imwrite(picture_filename,blur)

	return picture_filename

def find_text(f):
	# add full code
	filename = save_picture(f)
	# img=Image.open(f)

	mtext = pytesseract.image_to_string(Image.open('images/'+filename))
	# return mtext
	return mtext

# ------------------------------------------------------------------------------------------
def convert_to_audio(temp):
	tts=gTTS(text=temp,lang="en")
	random_hex = secrets.token_hex(8)

	filename='static/'+random_hex + ".mp3"
	tts.save(filename)
	return filename

if __name__=='__main__':
	app.run(debug=True)
