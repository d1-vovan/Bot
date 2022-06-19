import sqlite3

def getAllItems():
    items = []
    with sqlite3.connect('db\dbMeridian.db') as db:
        cursor = db.cursor()
        cursor.execute("""SELECT Name from Item """)
        items = cursor.fetchall()

    return items