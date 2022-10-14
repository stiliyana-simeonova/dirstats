import os
import sqlite3
import hashlib
import mimetypes
import datetime

'''set some var so its not crazily hadcoded'''
db_file = "files.db" #change the name of the sqlite database as you see fit
dir_root = "." # define the root which would be itterated through. By default this is the current directory

'''get rid of the database if it exists'''
if os.path.exists(db_file):
    print("DB file exists. Deleting and will be recreating")
    os.remove(db_file)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT exists file_data (hash TEXT, file_name TEXT, file_path TEXT, file_type TEXT, file_size INTEGER, created TEXT, last_modified TEXT, author TEXT)")

'''simple funciton to calculate ether md5 or sha256 with default being md5'''
def get_hash(filename, hash_function = "md5"):
    hash_function = hash_function.lower()
 
    with open(filename, "rb") as f:
        bytes = f.read()  # read file as bytes
        if hash_function == "sha256":
            readable_hash = hashlib.sha256(bytes).hexdigest()
        else:
            hash_function = "md5"
            readable_hash = hashlib.md5(bytes).hexdigest()
 
    return readable_hash

'''todo - potentially implment this to extract data from specific files on authorship'''
def get_author (file):
    return ""

'''itterate recursively through files in a directory and shove some file metadata an sql lite table for quick query later'''
for file_root, dirs, files in os.walk(dir_root, topdown=True):
    for file_name in files:
        file_path = os.path.join(file_root,file_name)   #full path to the file required for the hashing function
        file_md5_hash = get_hash(file_path)             # calculate hash 
        file_type = mimetypes.guess_type(file_path)     # apture mime type if possibe - for further interrogation
        file_stat = os.stat(file_path)                  # get file os stats object
        file_size = file_stat.st_size                   # grab zie - in bytes
        file_c_time = file_stat.st_ctime                # grab create date 
        file_lm_time = file_stat.st_mtime               # grab last modificaiton date
        file_author = get_author(file_path)             # get autor if possible (NOT READY)
        #print(file_md5_hash, file_name, file_root.lstrip(dir_root), file_type, file_size, datetime.datetime.fromtimestamp(file_c_time), datetime.datetime.fromtimestamp(file_lm_time),file_author)
        cursor.execute('''INSERT INTO file_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',(file_md5_hash, file_name, file_root.lstrip(dir_root), str(file_type), file_size, datetime.datetime.fromtimestamp(file_c_time), datetime.datetime.fromtimestamp(file_lm_time),file_author))
        conn.commit()