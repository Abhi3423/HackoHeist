from flask import Flask, request,session,abort, redirect,render_template, jsonify
from flask_cors import CORS, cross_origin

from mongo import mongo_pdf, download
import base64
import json

from image_pdf import pdfToImg
from nlp import language_process, pdf_id_init
from plagarism import plager


import requests
import os
import pathlib

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests


app = Flask(__name__)
app.secret_key = "Bits-Space"
CORS(app)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

current_user = "not_defined"


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html', current_user_id=current_user)




@app.route('/show_projects', methods=['GET','POST'])
def show():
    if request.method == 'POST':
        pointer = request.get_data()
        
        pointer = pointer.decode('utf-8')
        with open('./static/json/pdf_name.json', 'r') as u:
            name_of_pdf = json.load(u)
            
        pdf_download_data = download(name_of_pdf[pointer])
        return pdf_download_data
    return render_template('index.html',current_user_id=current_user)
    
    
    
    
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
        pdf_id_init(current_user)
        plager(pdf_token, pdf_base64['pdf_name'])
        
    return render_template('upload_page.html',current_user_id=current_user)
    


GOOGLE_CLIENT_ID = "842363639124-useb2nft637f7petod0fqk68e101tbm2.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email","openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    global current_user
    
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    
    current_user = id_info.get("sub")
      
    with open('./static/json/user_id.json', 'r') as u:
        user_id_json_data = json.load(u)
        
    user_id_json_data[id_info.get("sub")] = { "user_name" : id_info.get("name") , "user_email" : id_info.get("email"), "user_dp": id_info.get("picture")}
    
    with open('./static/json/user_id.json', 'w') as y:
        json.dump(user_id_json_data, y)
        
    return redirect("/upload_pdf")


@app.route("/logout")
def logout():
     global current_user
     session.clear()
     current_user = "not_defined"
     return redirect("/")


if __name__ == '__main__':
    app.run()