import MySQLdb
import MySQLdb.cursors
import os
import config

db=None

def openDB(dbname):
	global db
	db=MySQLdb.connect(host="localhost",
			   user=config.username,
			   passwd=config.password,
			   db=dbname,
			   cursorclass = MySQLdb.cursors.SSCursor)

def execute(cmd):
	global db
	c=db.cursor()
	c.execute(*cmd)
	rs=c.fetchall()
	db.commit()
	return rs


def closeDB():
	global db
	db.close()

def cleanDB():
	global db
	c=db.cursor()
	c.execute("drop table if exists follows,posts,users")
	db.commit()

def setupDB():
	global db
	c=db.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS users(uid INTEGER PRIMARY KEY AUTO_INCREMENT,uname TEXT NOT NULL) ENGINE=InnoDB")
	c.execute("CREATE TABLE IF NOT EXISTS follows(fid INTEGER PRIMARY KEY AUTO_INCREMENT,follower INT, followee INT, FOREIGN KEY(follower) REFERENCES users(uid), FOREIGN KEY(followee) REFERENCES users(uid)) ENGINE=InnoDB")
	c.execute("CREATE TABLE IF NOT EXISTS posts(pid INTEGER PRIMARY KEY AUTO_INCREMENT, uid INT, ptext TEXT NOT NULL, FOREIGN KEY(uid) REFERENCES users(uid)) ENGINE=InnoDB")

	db.commit()

def getDB():
	global db
	return db

