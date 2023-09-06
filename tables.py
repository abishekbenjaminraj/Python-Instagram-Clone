import sqlite3
 
conn = sqlite3.connect("database.db")
 
cursor = conn.cursor()
 
 
cursor.execute("create table users(username text,email text)")
 
cursor.execute("create table usercontent(userid int,username text,imagelink text,caption text, foreign key(userid,username) references users(rowid,username))")
 
conn.commit()
 
conn.close()