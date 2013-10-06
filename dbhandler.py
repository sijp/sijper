import sqlite3
import os

db=None

def openDB(dbname):
	global db
	if not os.path.isfile(dbname):
		db=sqlite3.connect(dbname)
		setupDB()
	else:
		db=sqlite3.connect(dbname)

def closeDB():
	global db
	db.close()

def setupDB():
	global db
	c=db.cursor()
	c.execute("CREATE TABLE users(uid INTEGER PRIMARY KEY AUTOINCREMENT,uname TEXT NOT NULL)")
	c.execute("CREATE TABLE follows(fid INTEGER PRIMARY KEY AUTOINCREMENT,follower INT, followee INT, FOREIGN KEY(follower) REFERENCES users(uid), FOREIGN KEY(followee) REFERENCES users(uid))")
	c.execute("CREATE TABLE posts(pid INTEGER PRIMARY KEY AUTOINCREMENT, uid INT, ptext TEXT NOT NULL, FOREIGN KEY(uid) REFERENCES users(uid))")

	db.commit()

def getDB():
	global db
	return db

