from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
# from werkzeug.utils import secure_filename
from mongo import mongo_pdf, download
import base64
import json

from image_pdf import pdfToImg
from nlp import language_process
from plagarism import plager

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pointer = request.get_data()
        
        pointer = pointer.decode('utf-8')
        with open('./static/json/pdf_name.json', 'r') as u:
            name_of_pdf = json.load(u)
            
        pdf_download_data = download(name_of_pdf[pointer])
        return pdf_download_data
    return render_template('index.html')
    
@app.route('/upload_pdf', methods=['GET', 'POST'])
def pdf():
    if request.method == 'POST':
        pdf_base64 = request.get_json()
        
        # decode = open(pdf_base64['pdf_name'], 'wb')
        # decode.write(base64.b64decode(pdf_base64['pdf']))
        
        encoded_pdf = 'data:application/pdf;base64,' + pdf_base64['pdf']
        # print(encoded_pdf)
        
        encoded_pdf_utf = encoded_pdf.encode('utf-8') 
        enc_pdf = pdf_base64['pdf'].encode('utf-8')
        
        mongo_pdf(encoded_pdf_utf, pdf_base64['pdf_name'])
        pdf_pages = pdfToImg(enc_pdf, pdf_base64['pdf_name'])
        pdf_token = language_process(pdf_pages, pdf_base64['pdf_name'])
        plager(pdf_token, pdf_base64['pdf_name'])
        
    return render_template('upload_page.html')
    

if __name__ == '__main__':
    app.run(debug=True)