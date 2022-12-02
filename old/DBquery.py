import sqlite3

def connectToDB():
    return sqlite3.connect('DB.db')

def analyzeUser(conn, userID):
    cur = conn.cursor()
    cur.execute("select * from Users where ID = ?", (userID,))
    return cur.fetchone()

def createNewUser(conn, userID, name, phone=''):
    cur = conn.cursor()
    cur.execute('insert into Users values(?,?,?)', (userID, name, phone))
    conn.commit()

