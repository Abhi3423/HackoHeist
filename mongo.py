import gridfs
import base64
from pymongo import MongoClient

def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://HACKSIH:4X7tqBNPeiuipcTm@cluster0.oyrk2.mongodb.net/myFirstDatabase"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['pdf_store']
  

def mongo_pdf(encoded_string, name): 
# Get the database
    dbname = get_database()  

    # path = 'Trial1.pdf'
    # db = client.storagearea
    fs = gridfs.GridFS(dbname)
    # Note, open with the "rb" flag for "read bytes"
    # with open(path, "rb") as f:
    #     encoded_string = base64.b64encode(f.read())
    with fs.new_file(chunkSize=800000, filename= name) as fp:
        fp.write(encoded_string)     

def download(name_of_pdf):
    db =  get_database()
    
    cursor = db.fs.files.find({'filename': name_of_pdf})
    
    for i in cursor:
        dict = i
     
    
    
    chunks_cursor = db.fs.chunks.find({'files_id': dict['_id'] })
    
    for j in chunks_cursor:
        dict1 = j
        # print(j)
        
    # print(dict1['data'])    
    # print(chunks_cursor)
    
    k = dict1['data'].decode('utf-8')
    
    data_pdf = k.split(",")[1]
    # print(data_pdf)
    
    # decode = open("Copy - Copy.pdf", 'wb')
    return base64.b64decode(data_pdf)
    
    
