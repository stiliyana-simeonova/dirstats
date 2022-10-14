import os
import sqlite3
import hashlib
import mimetypes
import datetime
from ast import Raise

conn = sqlite3.connect( "files.db" )
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT exists file_data (hash TEXT, file_name TEXT, file_path TEXT, file_type TEXT, file_size INTEGER, created TEXT, last_modified TEXT, author TEXT)")

def get_hash(filename, hash_function):
    hash_function = hash_function.lower()
 
    with open(filename, "rb") as f:
        bytes = f.read()  # read file as bytes
        if hash_function == "md5":
            readable_hash = hashlib.md5(bytes).hexdigest()
        elif hash_function == "sha256":
            readable_hash = hashlib.sha256(bytes).hexdigest()
        else:
            Raise("{} is an invalid hash function. Please Enter MD5 or SHA256")
 
    return readable_hash

def get_author (file):
    return ""

for file_root, dirs, files in os.walk(".", topdown=True):
    for file_name in files:
        file_path = os.path.join(file_root,file_name)
        file_md5_hash = get_hash(file_path,"md5")
        file_type = mimetypes.guess_type(file_path)
        file_stat = os.stat(file_path)
        file_size = file_stat.st_size
        file_c_time = file_stat.st_ctime
        file_lm_time = file_stat.st_mtime
        file_author = get_author(file_path)
        #print (file_md5_hash, file_name, file_root, file_type, file_size, datetime.datetime.fromtimestamp(file_c_time), datetime.datetime.fromtimestamp(file_lm_time),file_author)
        cursor.execute('''INSERT INTO file_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',(file_md5_hash, file_name, file_root, str(file_type), file_size, datetime.datetime.fromtimestamp(file_c_time), datetime.datetime.fromtimestamp(file_lm_time),file_author))
        conn.commit()