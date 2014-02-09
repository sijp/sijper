import MySQLdb
import MySQLdb.cursors
import os
import config
import sys

#disable mysql warnings
from warnings import filterwarnings
filterwarnings('ignore',category=MySQLdb.Warning)

#db - global MySQL connector
db=None

def openDB(dbname):
    ''' open the connection to the db with the params
        retrieved from config.py
    '''
    
    global db
    db=MySQLdb.connect(host="localhost",
                 user=config.username,
                 passwd=config.password,
                 db=dbname)

def execute(cmd):
    ''' execute the sql query 'cmd'
        returns the query result (list of tuples)
    '''
    global db
    try:
        c=db.cursor()
        c.execute(*cmd)
        rs=c.fetchall()
        c.close()
        db.commit()
        return rs
    except Exception as e:
        print e
        return tuple()

def closeDB():
    '''close the db connection
    
    '''
    global db
    db.close()

def cleanDB():
    '''reset the db - removes permenantly all the tables
    
    '''
    global db
    c=db.cursor()
    c.execute("drop table if exists follows,posts,users")
    db.commit()

def setupDB():
    '''recreates the tables if they do not exist
    
    '''
    
    global db
    c=db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users"
            "(uid INTEGER PRIMARY KEY AUTO_INCREMENT, uname TEXT NOT NULL) "
            "ENGINE=InnoDB")
    c.execute("CREATE TABLE IF NOT EXISTS follows"
            "(fid INTEGER PRIMARY KEY AUTO_INCREMENT, "
            "follower INT, "
            "followee INT, "
            "FOREIGN KEY(follower) REFERENCES users(uid), "
            "FOREIGN KEY(followee) REFERENCES users(uid)) "
            "ENGINE=InnoDB")
    c.execute("CREATE TABLE IF NOT EXISTS posts"
            "(pid INTEGER PRIMARY KEY AUTO_INCREMENT, "
            "uid INT, "
            "ptext TEXT NOT NULL, "
            "FOREIGN KEY(uid) REFERENCES users(uid)) "
            "ENGINE=InnoDB")

    db.commit()


