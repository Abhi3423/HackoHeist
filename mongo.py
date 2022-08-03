# from fileinput import filename
# import pymongo
# import base64
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



# def write_new_pdf():
#     path = 'pyth.pdf'
#     print(path)
#     db = client.storagearea
#     fs = gridfs.GridFS(db)
#     # Note, open with the "rb" flag for "read bytes"
#     with open(path, "rb") as f:
#         encoded_string = base64.b64encode(f.read())
#     with fs.new_file(chunkSize=800000,filename=path) as fp:
#         fp.write(encoded_string)

# def try_read():
#     file_name = './Pdfs/Trial1.pdf'
#     grid_fs_file = grid_fs.find_one({'filename': file_name})
#     response = make_response(grid_fs_file.read())
#     response.headers['Content-Type'] = 'application/octet-stream'
#     response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
#     return response


# def read_pdf():
#     # Usual setup
#     # db = MongoClient('mongodb://localhost:27017/').myDB
#     filename = './Pdfs/Trial1.pdf'
#     fs = gridfs.GridFS(dbname)
#     # Standard query to Mongo
#     data = fs.find_one(filter=dict(filename=filename))
#     with open(filename, "wb") as f:
#         f.write(base64.b64decode(data.read()))
#     return data
        


 
# This is added so that many files can reuse the function get_database()
# if __name__ == "__main__":    

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
        # print(i)
        # print(type(i))
       
    # print(dict['_id'])  
    
    
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
    
    
    
    
    
# def downl():
#     file_name = 'pyimg.pdf'
#     grid_fs_file = grid_fs.find_one({'filename': file_name})
#     response = make_response(grid_fs_file.read())
#     response.headers['Content-Type'] = 'application/octet-stream'
#     response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
#     return response   