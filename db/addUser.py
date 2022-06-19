import sqlite3

def addUser(id, name, date, time, accessLevel):
    with sqlite3.connect('db\dbMeridian.db') as db:
        cursor = db.cursor()
        # id, name, date, time, accessLevel
        cursor.execute("""INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?, ?)""", 
        (id, name, date, time, accessLevel))
        db.commit()