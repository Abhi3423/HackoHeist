import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

from tesseract import ocr_image
import json

def language_process(pages, pdf_name):
    global data_length
    uploaded_token = []
    
    for i in range(0,pages):
        text_lo = ocr_image(f'./images/page{i}.jpg')

        tok_pdf = word_tokenize(text_lo)
        tok_pdf = [token.lower() for token in tok_pdf]

        stop_words = set(stopwords.words('english'))
        punctuations=['"','.','(',')',',','?',';',':',"''",'``','=']

        ref_tok_pdf = [w for w in tok_pdf if not w in stop_words and not w in punctuations]  
        uploaded_token = uploaded_token + ref_tok_pdf
        
        
    with open('./static/json/data.json', "r") as f:
        data = json.load(f)
        
    data_length = len(data)
    
    # data.append(token_data)
    data[data_length] = uploaded_token

    with open('./static/json/data.json', 'w') as t:
        json.dump(data, t)
        
    with open('./static/json/pdf_name.json', 'r') as v:
        data_name = json.load(v)
        
    data_name[data_length] = pdf_name
        
    with open('./static/json/pdf_name.json', 'w') as o:
        json.dump(data_name, o)
        
        
    return uploaded_token

def pdf_id_init(current_user):    
    with open('./static/json/pdf_id.json', 'r') as p:
        id_for_pdf = json.load(p)
    
    id_for_pdf[data_length] = current_user
    
    with open('./static/json/pdf_id.json', 'w') as x:
        json.dump(id_for_pdf, x)